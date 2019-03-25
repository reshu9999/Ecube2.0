DELIMITER ;;

CREATE PROCEDURE `GetTableData_ECUBE_MDM_5_WithOUT_Link`( 
	p_intBatchId INT 
	,p_vcrBatchName VARCHAR(500)
	,p_sdtmDiPBagDynamicRecordDT VARCHAR(50)
	,p_Status VARCHAR(50)
	,p_intDipBagDynamicId INT
	,p_intSourceMDM_BatchesId INT
	,p_dtmTimestamp datetime 
    ,p_bitRenameFlag int
    ,p_nvcrSupplierID NVARCHAR (500)
    ,p_BitIsPNFStopper NVARCHAR(50)   
    ,p_intpartialuploadid int      

)
ThisSP:Begin   
 
 
		declare p_FileName nvarchar(50);
 
		DECLARE v_id INT;
		DECLARE v_Start VARCHAR(50) DEFAULT 'Start';
		DECLARE v_Stop VARCHAR(50) DEFAULT 'Stop'; -- ------------------Yogesh
		Declare v_Continue varchar (50) Default 'Continue'; -- -----Yogesh
		DECLARE v_intStatusId INT DEFAULT 6; -- - statusid  6 for Started
	-- DECLARE v_DipbagDynamicDT DATETIME(3) DEFAULT LEFT(p_sdtmDiPBagDynamicRecordDT, position('.' in p_sdtmDiPBagDynamicRecordDT) - 1); 

		set p_FileName = '' ;
			
            
		INSERT INTO MDM_Batches_MDM (
			intBatchId
			,vcrBatchName
			,intStatusId
			-- ,sdtmDiPBagDynamicRecordDT
			,intDipBagDynamicId
			,intSourceMDM_BatchesId
			,isComplete
			,dtmTimestamp
            ,bitRenameFlag
            ,IntWorkFlowID
            ,nvcrSupplierID
			)
		VALUES (
			  p_intBatchId -- 101
			,p_vcrBatchName -- 'ABC'
			,v_intStatusId
			-- ,''-- ,v_DipbagDynamicDT
			,p_intDipBagDynamicId
			 ,p_intSourceMDM_BatchesId
			,0
			 ,p_dtmTimestamp
            ,p_bitRenameFlag
             ,5
             ,p_nvcrSupplierID
			);
		SET v_id = LAST_INSERT_ID();
		
	  
    
		CALL SendMail_BatchInitiate_5 (@intMDM_BatchesId = v_id
		   ,@vcrStatus = v_Start);	
		

		UPDATE MDM_Batches_MDM	SET intStatusId = 7 WHERE intMDM_BatchesId = v_id and IntWorkFlowID=5;

		-- truncate table batchCrawlDataStag	
		TRUNCATE TABLE BatchCrawlDataStag_ECUBE_MDM_5;
		TRUNCATE TABLE BatchCrawlDatafinal_ECUBE_MDM_5;
      

		truncate table `TempQA_ECUBE_MDM_5`;
 	                      
		CALL sp_GetBatchDataAfterErrorCheck (p_intDipBagDynamicId,p_nvcrSupplierID); -- -25756

		truncate table  `Hotel_Count_Ecube_MDM_5` ;

	
	/*	insert into Hotel_Count_Ecube_MDM_5 Change(Ch_Date,Night,Supplier,Hotel_Count,Previous_Crawl_Count,Previous_Crawl_Diff,CurrentMatchCount,PreviousMatchCount,MatchingPercent)*/
	
		call sp_GetHotelCount (@intBatchId,@intDipBagDynamicId);

		IF p_BitIsPNFStopper='T'
		Then 
			
	   CALL sp_GetReportUploadUpdate (p_intBatchId,p_intDipBagDynamicId,p_nvcrSupplierID);

		IF EXISTS (select * from TempQAStop_ECUBE_MDM_5  where `Status` like '%Fail%' limit 1)
		THEN
		
        CALL `SendMail_STOP_ECUBE_MDM_5` (@intMDM_BatchesId = v_id
		   ,@vcrStatus = v_Stop	);
		CALL Batch_SuccesFullExecution_ECUBE_MDM_5( 0, 105);
	  -- LEAVE ThisSP;
   
		else 
	
		CALL `SendMail_STOP_ECUBE_MDM_5` (@intMDM_BatchesId = v_id
			   ,@vcrStatus = v_Stop	);
		end if; 
	
		END IF;

IF p_BitIsPNFStopper='F'

Then 	
			
        CALL sp_GetReportUploadUpdate (p_intBatchId,p_intDipBagDynamicId,p_nvcrSupplierID);

		IF EXISTS (select  * from TempQAStop_ECUBE_MDM_5 limit 1)

		THEN
			CALL `SendMail_STOP_ECUBE_MDM_5` (@intMDM_BatchesId = v_id
				   ,@vcrStatus = v_Continue	);
			
	    END IF;	

		IF EXISTS (select  * from TempQAStop_ECUBE_MDM_5 where intstatus=1)
		THEN 
        drop table if EXISTS  TempQAStop_ECUBE_MDM_5_TEMP;
        
        create temporary table TempQAStop_ECUBE_MDM_5_TEMP (
				id	int(11) Unique Key Auto_increment,
				QA_Checks	longtext ,
				`Status`	varchar(50) ,
				nvcrComment	longtext ,
				intstatus	int(11) 
		);
        
		-- select  * from TempQAStop_ECUBE_MDM_2
			insert into TempQAStop_ECUBE_MDM_5_TEMP 
			select QA_Checks, `Status`, nvcrComment, intstatus 
            From TempQAStop_ECUBE_MDM_5 Where intstatus = 1;
            
			Truncate Table TempQAStop_ECUBE_MDM_5;
			
			Insert Into TempQAStop_ECUBE_MDM_5 (QA_Checks, Status, nvcrComment, intstatus)
			Select QA_Checks, `Status`, nvcrComment, intstatus 
            From TempQAStop_ECUBE_MDM_5_TEMP;

       
			CALL `SendMail_STOP_ECUBE_MDM_5` (@intMDM_BatchesId = v_id
			,@vcrStatus = v_Stop);	
      
			drop table TempQAStop_ECUBE_MDM_5_TEMP;
		
			CALL Batch_SuccesFullExecution_ECUBE_MDM_5( 0, 105);
			/*leave sp_lbl;*/
			END IF;	
			END IF;


			IF p_bitRenameFlag = 0
			then
			SET p_FileName = Concat(CAST(p_intBatchId As unsigned) , '_' , concat(cast(p_intSourceMDM_BatchesId As unsigned)),  '_' ,concat(p_vcrBatchName , '_') ,concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  concat( case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as unsigned) end) ,concat( '.csv')));	
			   /*SET p_FileName = CONCAT(CONVERT(VARCHAR, p_intBatchId) , '_' , convert(varchar,p_intSourceMDM_BatchesId) , '_' , p_vcrBatchName , '_' , REPLACE(DATE_FORMAT (p_dtmTimestamp, '%d/%m/%Y'), '/', '') + REPLACE(DATE_FORMAT (p_dtmTimestamp, '%T'), ':', '') + case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as varchar(1)) end , '.csv');*/
			ELSE
			SET p_FileName = Concat(CAST(p_intBatchId As unsigned) , '_' , concat(cast(p_intSourceMDM_BatchesId As unsigned)),  '_' ,concat(p_vcrBatchName , '_') ,concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  concat( case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as unsigned) end) ,concat( 'bis.csv')));	
            -- SET p_FileName = Concat(CAST(@intBatchid As unsigned) , '_' , concat(cast(@intSourceMDM_BatchesId As unsigned)),  '_' ,concat(@vcrBatchName , '_') ,concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  concat( case @intpartialuploadid when 0 then '' else cast(@intpartialuploadid as unsigned) end) ,concat( 'bis.csv')));		 
				/*SET p_FileName = CONCAT(CONVERT(VARCHAR, p_intBatchId) , '_' , convert(varchar,p_intSourceMDM_BatchesId) , '_' , p_vcrBatchName , '_' , REPLACE(DATE_FORMAT (p_dtmTimestamp, '%d/%m/%Y'), '/', '') + REPLACE(DATE_FORMAT (p_dtmTimestamp, '%T'), ':', '')  +  case p_intpartialuploadid when 0 then '' else CONVERT(VARCHAR, p_intpartialuploadid)  end , 'bis.csv'); */ 	
			end if;

 INsert into DebugDetails 
    Select p_FileName;
			-- select p_FileName;

			 CALL sp_LastResult_Report (p_intDipBagDynamicId,p_intBatchId,p_intSourceMDM_BatchesId,p_FileName);
		

			IF NOT EXISTS (
						SELECT *
						FROM BatchCrawlDatafinal_ECUBE_MDM_5
						)
			THEN
			-- EXEC SENDMAIL @intMDM_BatchesId  = @id , @vcrStatus ='NoData'
			UPDATE MDM_Batches_MDM	SET intStatusId = 9	WHERE intMDM_BatchesId = v_id and IntWorkFlowID=5;
			/*LEAVE sp_lbl;*/
			END IF;
		
        UPDATE MDM_Batches_MDM 	SET vcrFileName = p_FileName WHERE intMDM_BatchesId = v_id and IntWorkFlowID=5;


	/*
	IF p_bitRenameFlag = 0
	then
	SET p_FileName = Concat(CAST(p_intBatchId As unsigned) , '_' , concat(cast(p_intSourceMDM_BatchesId As unsigned)),  '_' ,concat(p_vcrBatchName , '_') ,concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  concat( case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as unsigned) end) ,concat( '.csv')));	
       /*SET p_FileName = CONCAT(CONVERT(VARCHAR, p_intBatchId) , '_' , convert(varchar,p_intSourceMDM_BatchesId) , '_' , p_vcrBatchName , '_' , REPLACE(DATE_FORMAT (p_dtmTimestamp, '%d/%m/%Y'), '/', '') + REPLACE(DATE_FORMAT (p_dtmTimestamp, '%T'), ':', '') + case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as varchar(1)) end , '.csv');*/
	/*
    ELSE
	SET p_FileName = Concat(CAST(@intBatchid As unsigned) , '_' , concat(cast(@intSourceMDM_BatchesId As unsigned)),  '_' ,concat(@vcrBatchName , '_') ,concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  concat( case @intpartialuploadid when 0 then '' else cast(@intpartialuploadid as unsigned) end) ,concat( 'bis.csv')));		 
	    /*SET p_FileName = CONCAT(CONVERT(VARCHAR, p_intBatchId) , '_' , convert(varchar,p_intSourceMDM_BatchesId) , '_' , p_vcrBatchName , '_' , REPLACE(DATE_FORMAT (p_dtmTimestamp, '%d/%m/%Y'), '/', '') + REPLACE(DATE_FORMAT (p_dtmTimestamp, '%T'), ':', '')  +  case p_intpartialuploadid when 0 then '' else CONVERT(VARCHAR, p_intpartialuploadid)  end , 'bis.csv'); */ 	
	-- end if;
		-- print @Filename
		
        
	   UPDATE BatchCrawlDatafinal_ECUBE_MDM_5 set FILENAME = p_FileName;
    END ;;
