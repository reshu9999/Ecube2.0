DELIMITER ;;

CREATE PROCEDURE `GetTableData_Hotel_Avail_Last_Result_SEC`(
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
    -- ,OUT p_FileName VARCHAR(500) 
    )
This_SP:BEGIN

 Declare p_FileName nvarchar (50);


		DECLARE v_id INT;
		DECLARE v_Start VARCHAR(50) DEFAULT 'Start';
		DECLARE v_Stop VARCHAR(50) DEFAULT 'Stop'; -- ------------------Yogesh
		Declare v_Continue varchar (50) Default 'Continue'; -- -----Yogesh
		DECLARE v_intStatusId INT DEFAULT 6; -- - statusid  6 for Started
		-- DECLARE v_DipbagDynamicDT DATETIME(3) DEFAULT LEFT(p_sdtmDiPBagDynamicRecordDT,  position('.' in p_sdtmDiPBagDynamicRecordDT) - 1); 

		IF p_Status = 8 THEN -- Manually Update 
			SET v_intStatusId = p_Status;
		END IF;
		
	  
    
    
	INSERT INTO MDM_Batches_Hotel_Avail (
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
			 p_intBatchId
			,p_vcrBatchName
			,v_intStatusId
            -- ,p_sdtmDiPBagDynamicRecordDT
			,p_intDipBagDynamicId
			,p_intSourceMDM_BatchesId
			,0
			,p_dtmTimestamp
            ,p_bitRenameFlag
             ,2
             ,p_nvcrSupplierID
			);
		SET v_id = LAST_INSERT_ID();
	

		
		-- CALL SendMail_Hotel_Avail_Initiate (@p_intMDM_BatchesId = v_id
		  -- ,@p_vcrStatus = v_Start);		
		

		UPDATE MDM_Batches_Hotel_Avail	SET intStatusId = 7 WHERE intMDM_BatchesId = v_id and IntWorkFlowID=2;

	
		-- TRUNCATE TABLE BatchCrawlDataStag_Hotel_Avail_Last_R_SEC;
		TRUNCATE TABLE BatchCrawlDatafinal_Hotel_Avail_Last_R_SEC;

		truncate table `TempQA_ECUBE_MDM_Hotel_Avail`;
					  
	    CALL sp_GetBatchDataAfterErrorCheck_HBA (p_intDipBagDynamicId,p_nvcrSupplierID); -- -25756


	
	truncate table  `Hotel_Count_Hotel_Avail`; 

	
		-- insert into `MDM_HotelBeds_PROD`.dbo (Ch_Date,Night,Supplier,Hotel_Count,Previous_Crawl_Count,Previous_Crawl_Diff,CurrentMatchCount,PreviousMatchCount,MatchingPercent)
	-- call GetHotelCount_Avail (p_intBatchId,p_intDipBagDynamicId);
	




	truncate table `TempQAStop_Hotel_Avail`;


IF p_BitIsPNFStopper='T'

Then 	
	-- insert into `MDM_HotelBeds_PROD`.dbo
	-- CALL GetReportUploadUpdate_Avail (p_intBatchId,p_intDipBagDynamicId,p_nvcrSupplierID);


 IF EXISTS (select  * from TempQAStop_Hotel_Avail limit 1)

THEN

	CALL `SendMail_STOP_Hotel_Avail` (p_intMDM_BatchesId = v_id
		   ,@vcrStatus = v_Stop	);

	
	CALL Batch_SuccesFullExecution_Hotel_Avail( 0, 105);
	

	-- LEAVE This_SP;
END IF;	
	
END IF;

/* --code is commented as in live 301 returnss top0 at301 for HBA


IF p_BitIsPNFStopper='F'

Then 	



	-- CALL GetReportUploadUpdate_Avail (p_intBatchId,p_intDipBagDynamicId,p_nvcrSupplierID);



 IF EXISTS (select  * from TempQAStop_Hotel_Avail limit 1)

THEN
	CALL `SendMail_STOP_Hotel_Avail` (p_intMDM_BatchesId = v_id
		   ,p_vcrStatus = v_Continue);
	
	
END IF;	



		
		IF EXISTS (select  * from TempQAStop_Hotel_Avail where intstatus=1)
		THEN 
		-- select  * from TempQAStop_ECUBE_MDM_2
			-- Select * into #Temp From `MDM_HotelBeds_PROD`.dbo Where intstatus = 1;
			
        Create temporary table TempQAStop_Hotel_Avail_TEMP(
	`id` int  NULL,
	`QA_Checks` Longtext NULL,
	`Status` nvarchar(50) NULL,
	`nvcrComment` Longtext NULL,
	`intstatus` int NULL
);
            
   insert into TempQAStop_Hotel_Avail_TEMP
   select * From TempQAStop_Hotel_Avail Where intstatus = 1; 
            
            Truncate Table `TempQAStop_Hotel_Avail`;
			
			Insert Into TempQAStop_Hotel_Avail (QA_Checks, Status, nvcrComment, intstatus)
			Select QA_Checks, `Status`, nvcrComment, intstatus From TempQAStop_Hotel_Avail;
			
		-- print; '4'
			CALL `SendMail_STOP_Hotel_Avail` (p_intMDM_BatchesId = v_id
			,p_vcrStatus = p_Stop	);
		

		
			CALL Batch_SuccesFullExecution_Hotel_Avail( 0, 105);
			
			drop table TempQAStop_Hotel_Avail;
	
			-- Leave This_SP;
		END IF;	
END IF;

	*/
    IF p_bitRenameFlag = 0
		

		then
		
		/* print 'hiii' */
		SET p_FileName = Concat(CAST(p_intBatchid As unsigned) , '_' , concat(cast(p_intSourceMDM_BatchesId As unsigned)),  '_' ,concat(p_vcrBatchName , '_') ,concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  concat( case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as unsigned) end) ,concat( '.csv')));	
		-- SET p_FileName = CONCAT(CONVERT(VARCHAR, p_intBatchId) , '_' , p_vcrBatchName , '_' , REPLACE(DATE_FORMAT (p_dtmTimestamp, '%d/%m/%Y'), '/', '') + REPLACE(DATE_FORMAT (p_dtmTimestamp, '%T'), ':', '') + case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as varchar(1)) end , '.csv');
		
		
		 ELSE
		SET p_FileName = Concat(CAST(p_intBatchid As unsigned) , '_' , concat(cast(p_intSourceMDM_BatchesId As unsigned)),  '_' ,concat(p_vcrBatchName , '_') ,concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  concat( case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as unsigned) end) ,concat( 'bis.csv')));		  

	    -- SET p_FileName = CONCAT(CONVERT(VARCHAR, p_intBatchId) , '_' , p_vcrBatchName , '_' , REPLACE(DATE_FORMAT (p_dtmTimestamp, '%d/%m/%Y'), '/', '') + REPLACE(DATE_FORMAT (p_dtmTimestamp, '%T'), ':', '') + case p_intpartialuploadid when 0 then '' else CONVERT(VARCHAR, p_intpartialuploadid)  end ,'bis.csv'); 	

		 end if; 
    
    
	
		CALL sp_LastResult_HBA ( p_intBatchId,p_intDipBagDynamicId,p_nvcrSupplierID,p_intSourceMDM_BatchesId,p_FileName,p_vcrBatchName);
		
/*
		
		IF NOT EXISTS (
				SELECT *
				FROM BatchCrawlDataStag_Hotel_Avail_Last_R_SEC
				)
		THEN
			-- EXEC SENDMAIL @intMDM_BatchesId  = @id , @vcrStatus ='NoData'
			UPDATE MDM_Batches_Hotel_Avail	SET intStatusId = 9	WHERE intMDM_BatchesId = v_id and IntWorkFlowID=2;
/* print '101' */
			-- LEAVE This_SP;

	
   /*     
        
		IF p_bitRenameFlag = 0
		

		then
		
		/* print 'hiii' */
/*
		SET p_FileName = Concat(CAST(p_intBatchid As unsigned) , '_' , concat(cast(p_intSourceMDM_BatchesId As unsigned)),  '_' ,concat(p_vcrBatchName , '_') ,concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  concat( case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as unsigned) end) ,concat( '.csv')));	
		-- SET p_FileName = CONCAT(CONVERT(VARCHAR, p_intBatchId) , '_' , p_vcrBatchName , '_' , REPLACE(DATE_FORMAT (p_dtmTimestamp, '%d/%m/%Y'), '/', '') + REPLACE(DATE_FORMAT (p_dtmTimestamp, '%T'), ':', '') + case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as varchar(1)) end , '.csv');
		
		
		 ELSE
		SET p_FileName = Concat(CAST(p_intBatchid As unsigned) , '_' , concat(cast(p_intSourceMDM_BatchesId As unsigned)),  '_' ,concat(p_vcrBatchName , '_') ,concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  concat( case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as unsigned) end) ,concat( 'bis.csv')));		  

	    -- SET p_FileName = CONCAT(CONVERT(VARCHAR, p_intBatchId) , '_' , p_vcrBatchName , '_' , REPLACE(DATE_FORMAT (p_dtmTimestamp, '%d/%m/%Y'), '/', '') + REPLACE(DATE_FORMAT (p_dtmTimestamp, '%T'), ':', '') + case p_intpartialuploadid when 0 then '' else CONVERT(VARCHAR, p_intpartialuploadid)  end ,'bis.csv'); 	

		 end if; 
	
    select p_FileName;
*/
		UPDATE MDM_Batches_Hotel_Avail 	SET vcrFileName = p_FileName WHERE intMDM_BatchesId = v_id and IntWorkFlowID=1;
	END ;;
