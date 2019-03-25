DELIMITER ;;

CREATE  PROCEDURE GetTableData_Hotel_Avail_Last_Result (
	p_intBatchId OUT INT 
	,p_vcrBatchName VARCHAR(500)
	,p_FileName OUT VARCHAR(500) 
	,p_sdtmDiPBagDynamicRecordDT VARCHAR(50)
	,p_Status VARCHAR(50)
	,p_intDipBagDynamicId INT
	,p_intSourceMDM_BatchesId INT
	,p_dtmTimestamp datetime(3) 
    ,p_bitRenameFlag tinyint
    ,p_nvcrSupplierID NVARCHAR (500)
    ,p_BitIsPNFStopper NVARCHAR(50)      
    ,p_intpartialuploadid int       
	)
sp_lbl:

*/




		DECLARE v_id INT;
		DECLARE v_Start VARCHAR(50) DEFAULT 'Start';
		DECLARE v_Stop VARCHAR(50) DEFAULT 'Stop'; -- ------------------Yogesh
		Declare v_Continue varchar (50) Default 'Continue'; -- -----Yogesh
		DECLARE v_intStatusId INT DEFAULT 6; -- - statusid  6 for Started
		-- DECLARE v_DipbagDynamicDT DATETIME(3) DEFAULT LEFT(p_sdtmDiPBagDynamicRecordDT,  position('.' in p_sdtmDiPBagDynamicRecordDT) - 1); 

		IF p_Status = 8 THEN -- Manually Update 
			SET v_intStatusId = p_Status;
		END IF;
		
		-- insert into mdmBatch after truncate 
		-- Truncate table MDM_Batches_Hotel_Avail
	/* print 'mess' */	
	/*
   */
   
    

  
    
    
	INSERT INTO MDM_Batches_Hotel_Avail (
			intBatchId
			,vcrBatchName
			,intStatusId
			-- ,sdtmDiPBagDynamicRecordDT
			,intDipBagDynamicId
			,intSourceMDM_BatchesId
			,isComplete
			-- ,dtmTimestamp
            ,bitRenameFlag
            ,IntWorkFlowID
            -- ,nvcrSupplierID
			)
		VALUES (
			'101' -- p_intBatchId
			,'ABC '-- ,p_vcrBatchName
			,1 -- v_intStatusId
			-- ,v_DipbagDynamicDT
			,'777' -- ,p_intDipBagDynamicId
			,'11' -- ,p_intSourceMDM_BatchesId
			,0
			--  ,p_dtmTimestamp
            ,0  -- p_bitRenameFlag
             ,1
             -- ,p_nvcrSupplierID
			);
		SET v_id = LAST_INSERT_ID();
	

		
CALL SendMail_Hotel_Avail_Initiate (@p_intMDM_BatchesId = v_id
		   ,@p_vcrStatus = v_Start);		
		

		UPDATE MDM_Batches_Hotel_Avail	SET intStatusId = 7 WHERE intMDM_BatchesId = v_id and IntWorkFlowID=1;

	
		TRUNCATE TABLE BatchCrawlDataStag_Hotel_Avail_Last_R_SEC;
		TRUNCATE TABLE BatchCrawlDatafinal_Hotel_Avail_Last_R_SEC;

	/*
		DROP TEMPORARY TABLE IF EXISTS BatchCrawlData_Avail;
		CREATE TEMPORARY TABLE BatchCrawlData_Avail (
			TIMESTAMP VARCHAR(500)
			,Company VARCHAR(500)
			,Dates VARCHAR(500)
			,Nights VARCHAR(500)
			,Hotel nvarchar(500)
			,HotelId VARCHAR(500)
			,PointOfSale VARCHAR(500)
			,City VARCHAR(500)
			,STATE VARCHAR(500)
			,Country VARCHAR(500)
			,DailyRate VARCHAR(500)
			,Rcode VARCHAR(500)
			,Tax VARCHAR(500)
			,RoomType VARCHAR(500)
			,RoomCode VARCHAR(500)
			,Supplier VARCHAR(500)
			,CancellationPolicy VARCHAR(500)
			,StarRating VARCHAR(500)
			,star VARCHAR(500)
			,Price VARCHAR(500)
			,Currency VARCHAR(500)
			,BreakFast VARCHAR(500)
			,Availability VARCHAR(500)
			,Board VARCHAR(500)
			,Uniquecode VARCHAR(500)
			,STATUS VARCHAR(500)
			,PageURL VARCHAR(500)
			,HotelCode VARCHAR(500)
			,ContractName VARCHAR(500)
			,Classification VARCHAR(500)
			,Integration VARCHAR(500)
			,B2B VARCHAR(500)
			,ComOfici VARCHAR(500)
			,ComCanal VARCHAR(500)
			,ComNeta VARCHAR(500)
			,nvcrHotelCode VARCHAR(500)
			,ReportType VARCHAR(500)
			,NetPrice VARCHAR(500)
			,SellingPrice VARCHAR(500)
			,Commission VARCHAR(500) -- nvcr
			,DirectPayment VARCHAR(500)
			,SellingPriceMandatory VARCHAR(500)
			,nvcrPromotion VARCHAR(500)
			,nvcrPromotionDescription VARCHAR(500)
			,nvcrHotelCount VARCHAR(500)
			,nvcrEventType VARCHAR(500)
			,strSupplier VARCHAR(255)
			,nvcrRoomAvailability varchar(255)       -- -column was removed 		,nvcrtaxdesc varchar(500) --added by yogesh 21-01-2016 
			,nvcrAdult nvarchar(100) -- Added by Yogesh 21-01-2016  
           ,nvcrOpaqueRate nvarchar(100)        -- Added by Yogesh 21-01-2016 
           ,nvcrLeadTime longtext         -- Added by Yogesh 21-01-2016
           ,nvcrAccountName nvarchar(255) -- added by anirudha tate   
           ,nvcrDynamicProperty nvarchar(50)-- --Added by Yogesh 21-01-2016
           ,HMHotelID int   -- ---Add new column on 19022016 REQID--50890
           ,HotelAddress nvarchar(500) -- -----Add new column on 16032016 REQ ID --51430
           ,nvcrSupplierHotelURL longtext
           ,nvcrCompetitorHotelID nvarchar (50)
           ,nvcrLongitude nvarchar(50)
           ,nvcrLatitude nvarchar(50)
		   ,nvcrYieldManager longtext
		   ,nvcrContractManager longtext
		   ,nvcrDemandGroup longtext
		   ,nvcrSegmentation longtext
			,nvcrHotelChain  longtext
			,nvcrHotelContractingType  longtext
			,nvcrTPS longtext
			,nvcrHotelStatus longtext
		  			);
			
	*/
	
	truncate table `TempQA_ECUBE_MDM_Hotel_Avail`;
					  
-- CALL GetBatchDataAfterErrorCheck_New_Avail (0,p_intDipBagDynamicId,p_nvcrSupplierID); -- -25756


	
	truncate table  `Hotel_Count_Hotel_Avail`; 

	
		-- insert into `MDM_HotelBeds_PROD`.dbo (Ch_Date,Night,Supplier,Hotel_Count,Previous_Crawl_Count,Previous_Crawl_Diff,CurrentMatchCount,PreviousMatchCount,MatchingPercent)
	call GetHotelCount_Avail (p_intBatchId,p_intDipBagDynamicId);
	




	truncate table `TempQAStop_Hotel_Avail`;


IF p_BitIsPNFStopper='T'

Then 	
	-- insert into `MDM_HotelBeds_PROD`.dbo
	CALL GetReportUploadUpdate_Avail (p_intBatchId,p_intDipBagDynamicId,p_nvcrSupplierID);


 IF EXISTS (select  * from TempQAStop_Hotel_Avail limit 1)

THEN

	CALL `SendMail_STOP_Hotel_Avail` (p_intMDM_BatchesId = v_id
		   ,@vcrStatus = v_Stop	);

	
	CALL Batch_SuccesFullExecution_Hotel_Avail( 0, 105);
	

	-- LEAVE This_SP;
END IF;	
	
END IF;


IF p_BitIsPNFStopper='F'

Then 	



	CALL GetReportUploadUpdate_Avail (p_intBatchId,p_intDipBagDynamicId,p_nvcrSupplierID);



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

	
	
		CALL LastResult_Avail ( p_intBatchId,-1,1,p_nvcrSupplierID);
		
/*
		INSERT INTO BatchCrawlDataStag_Hotel_Avail_Last_R_SEC
		SELECT TIMESTAMP 
			,Company 
			,Dates 
			,Nights 
			,Hotel 
			,HotelId 
			,PointOfSale 
			,City 
			,STATE 
			,Country 
			,DailyRate 
			,Rcode 
			,Tax 
			,RoomType 
			,RoomCode 
			,Supplier 
			,CancellationPolicy 
			,StarRating 
			,star 
			,Price 
			,Currency 
			,BreakFast 
			,Availability 
			,Board 
			,Uniquecode 
			,STATUS 
			,PageURL 
			,HotelCode 
			,ContractName 
			,Classification 
			,Integration 
			,B2B 
			,ComOfici 
			,ComCanal 
			,ComNeta 
			,nvcrHotelCode 
			,ReportType 
			,NetPrice 
			,SellingPrice 
			,Commission 
			,DirectPayment 
			,SellingPriceMandatory 
			,nvcrPromotion 
			,nvcrPromotionDescription 
			,nvcrHotelCount 
			,nvcrEventType 
			,strSupplier 
			,p_intBatchId
			,p_intDipBagDynamicId
			,0
			,nvcrRoomAvailability 
			,nvcrAdult   -- -----Added by Yogesh 21-01-2016  
           ,nvcrOpaqueRate       -- Added by Yogesh 21-01-2016
           ,nvcrLeadTime        -- Added by Yogesh 21-01-2016
            ,nvcrAccountName  -- added by anirudha tate   
           ,nvcrDynamicProperty -- --Added by Yogesh 21-01-2016
           ,HMHotelID     -- ---Add new column on 19022016 REQID--50890
           ,HotelAddress  -- -----Add new column on 16032016 REQ ID --51430
           ,nvcrSupplierHotelURL  -- Add new column on 03-06-2016 REQ ID --51430
           ,nvcrCompetitorHotelID -- Add new column on 03-06-2016 REQ ID --51430
           ,nvcrLongitude           -- Add new column on 03-06-2016 REQ ID --51430
           ,nvcrLatitude        -- Add new column on 03-06-2016 REQ ID --51430
           ,p_intSourceMDM_BatchesId
           ,p_vcrBatchName
		    ,nvcrYieldManager 
		   ,nvcrContractManager
		   ,nvcrDemandGroup 
			,nvcrSegmentation
			,nvcrHotelChain 
			,nvcrHotelContractingType 
			,nvcrTPS 
			,nvcrHotelStatus
           	FROM BatchCrawlData_Avail ; 
            
           */ 
 -- print; '100'
		-- If no data present then send mail and exit sp
		IF NOT EXISTS (
				SELECT *
				FROM BatchCrawlDataStag_Hotel_Avail_Last_R_SEC
				)
		THEN
			-- EXEC SENDMAIL @intMDM_BatchesId  = @id , @vcrStatus ='NoData'
			UPDATE MDM_Batches_Hotel_Avail	SET intStatusId = 9	WHERE intMDM_BatchesId = v_id and IntWorkFlowID=1;
/* print '101' */
			-- LEAVE This_SP;
		END IF;


/*		-- EXEC BATCHCRAWLDATA_UPDATE
/* print 'insert_UPDATE_TEMP'; */
/*
		CALL UpdateTempTable_Hotel_Avail( v_intBatchid -- ----Pending
			,v_vcrBatchName
			,v_intDipBagDynamicId
			,v_id);
*/
/* print 'insert_UPDATE_TEMP_END' */
		/*set @FileName = CONVERT(VARCHAR,@intBatchid) + '_'+ @vcrBatchName + '_'+
					REPLACE(CONVERT(VARCHAR(15), GETDATE(), 103), '/', '') + REPLACE(CONVERT(VARCHAR(8), GETDATE(), 108), ':', '')  + '.csv' */
				/* print p_bitRenameFlag */
		
	
	
		 INSERT INTO BatchCrawlDatafinal_Hotel_Avail_Last_R_SEC ( 
		nvcrTimestamp,
		nvcrCompany,
		nvcrDates,
		Nights,
		nvcrHotel,
		HotelId,
		nvcrPointOfSale,
		nvcrCity,
		nvcrState,
		nvcrCountry,
		nvcrDailyRate,
		Rcode,
		nvcrTax,
		nvcrRoomType,
		nvcrRoomCode,
		nvcrSupplier,
		nvcrCancellationPolicy,
		StarRating,
		nvcrstar,
		nvcrPrice,
		nvcrCurrency,
		nvcrBreakFast,
		nvcrAvailability,
		nvcrBoard,
		nvcrUniquecode,
		nvcrStatus,
		nvcrPageURL,
		HotelCode,
		nvcrContractName,
		nvcrClassification,
		nvcrIntegration,
		nvcrB2B,
		nvcrComOfici,
		nvcrComCanal,
		nvcrComNeta,
		nvcrnvcrHotelCode,
		ReportType,
		nvcrNetPrice,
		nvcrSellingPrice,
		nvcrCommission,
		nvcrDirectPayment,
		nvcrSellingPriceMandatory,
		nvcrPromotion,
		nvcrPromotionDescription,
		nvcrHotelCount,
		nvcrEventType,
		strSupplier,
		intBatchId,
		intDipBagDynamicId,
		nvcrRoomAvailability,	
		nvcrAdult,   -- -----Added by Yogesh 21-01-2016  
        nvcrOpaqueRate,       -- Added by Yogesh 21-01-2016
        nvcrLeadTime,     -- Added by Yogesh 21-01-2016
        nvcrAccountName, -- added by anirudha tate   
        nvcrDynamicProperty, -- --Added by Yogesh 21-01-2016
        HMHotelID,   -- -----ADDED NEW column reqid ----50890
        HotelAddress  -- -----Add new column on 16032016 REQ ID --51430
        ,nvcrSupplierHotelURL  -- Add new column on 03-06-2016 REQ ID --51430
           ,nvcrCompetitorHotelID -- Add new column on 03-06-2016 REQ ID --51430
           ,nvcrLongitude           -- Add new column on 03-06-2016 REQ ID --51430
           ,nvcrLatitude        -- Add new column on 03-06-2016 REQ ID --51430
           ,MasterID
           ,Batch_Name
		   ,nvcrYieldManager 
		   ,nvcrContractManager
		   ,nvcrDemandGroup 
		   	,nvcrSegmentation
			,nvcrHotelChain 
			,nvcrHotelContractingType 
			,nvcrTPS 
			,nvcrHotelStatus
				)
        SELECT 
        nvcrTimestamp,
		nvcrCompany,
		nvcrDates,
		Nights,
		nvcrHotel,
		HotelId,
		nvcrPointOfSale,
		nvcrCity,
		nvcrState,
		nvcrCountry,
		nvcrDailyRate,
		Rcode,
		nvcrTax,
		nvcrRoomType,
		nvcrRoomCode,
		nvcrSupplier,
		nvcrCancellationPolicy,
		StarRating,
		nvcrstar,
		nvcrPrice,
		nvcrCurrency,
		nvcrBreakFast,
		nvcrAvailability,
		nvcrBoard,
		nvcrUniquecode,
		nvcrStatus,
		nvcrPageURL,
		HotelCode,
		nvcrContractName,
		nvcrClassification,
		nvcrIntegration,
		nvcrB2B,
		nvcrComOfici,
		nvcrComCanal,
		nvcrComNeta,
		nvcrnvcrHotelCode,
		ReportType,
		nvcrNetPrice,
		nvcrSellingPrice,
		nvcrCommission,
		nvcrDirectPayment,
		nvcrSellingPriceMandatory,
		nvcrPromotion,
		nvcrPromotionDescription,
		nvcrHotelCount,
		nvcrEventType,
		strSupplier,
		intBatchId,
		@intDipBagDynamicId,
		nvcrRoomAvailability,
		nvcrAdult,   -- -----Added by Yogesh 21-01-2016  
        nvcrOpaqueRate,       -- Added by Yogesh 21-01-2016
        nvcrLeadTime,     -- Added by Yogesh 21-01-2016
        nvcrAccountName, -- added by anirudha tate   
        nvcrDynamicProperty, -- --Added by Yogesh 21-01-2016
        HMHotelID,    -- -----ADDED NEW column reqid ----50890
        HotelAddress  -- -----Add new column on 16032016 REQ ID --51430
        ,nvcrSupplierHotelURL  -- Add new column on 03-06-2016 REQ ID --51430
           ,nvcrCompetitorHotelID -- Add new column on 03-06-2016 REQ ID --51430
           ,nvcrLongitude           -- Add new column on 03-06-2016 REQ ID --51430
           ,nvcrLatitude        -- Add new column on 03-06-2016 REQ ID --51430
           ,MasterID
           ,Batch_Name
		    ,nvcrYieldManager 
		   ,nvcrContractManager
		   ,nvcrDemandGroup 
		   ,nvcrSegmentation
			,nvcrHotelChain 
			,nvcrHotelContractingType 
			,nvcrTPS 
			,nvcrHotelStatus
	FROM   BatchCrawlDataStag_Hotel_Avail_Last_R_SEC;
        
        
        
		IF p_bitRenameFlag = 0
		

		then
		
		/* print 'hiii' */
		SET p_FileName = Concat(CAST(@intBatchid As unsigned) , '_' , concat(cast(@intSourceMDM_BatchesId As unsigned)),  '_' ,concat(@vcrBatchName , '_') ,concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  concat( case @intpartialuploadid when 0 then '' else cast(@intpartialuploadid as unsigned) end) ,concat( '.csv')));	
		-- SET p_FileName = CONCAT(CONVERT(VARCHAR, p_intBatchId) , '_' , p_vcrBatchName , '_' , REPLACE(DATE_FORMAT (p_dtmTimestamp, '%d/%m/%Y'), '/', '') + REPLACE(DATE_FORMAT (p_dtmTimestamp, '%T'), ':', '') + case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as varchar(1)) end , '.csv');
		
		
		 ELSE
		SET p_FileName = Concat(CAST(@intBatchid As unsigned) , '_' , concat(cast(@intSourceMDM_BatchesId As unsigned)),  '_' ,concat(@vcrBatchName , '_') ,concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  concat( case @intpartialuploadid when 0 then '' else cast(@intpartialuploadid as unsigned) end) ,concat( 'bis.csv')));		  

	    -- SET p_FileName = CONCAT(CONVERT(VARCHAR, p_intBatchId) , '_' , p_vcrBatchName , '_' , REPLACE(DATE_FORMAT (p_dtmTimestamp, '%d/%m/%Y'), '/', '') + REPLACE(DATE_FORMAT (p_dtmTimestamp, '%T'), ':', '') + case p_intpartialuploadid when 0 then '' else CONVERT(VARCHAR, p_intpartialuploadid)  end ,'bis.csv'); 	

		 end if; 
	

		UPDATE MDM_Batches_Hotel_Avail 	SET vcrFileName = p_FileName WHERE intMDM_BatchesId = v_id and IntWorkFlowID=1;
	END ;;
