DELIMITER ;;

CREATE PROCEDURE `GetTableData_ECUBE_MDM_5_WithOUT_Link_TEST`( 
	p_intBatchId INT 
	,p_vcrBatchName VARCHAR(500)
	,p_sdtmDiPBagDynamicRecordDT VARCHAR(50)
	,p_Status VARCHAR(50)
	,p_intDipBagDynamicId INT
	,p_intSourceMDM_BatchesId INT
	,p_dtmTimestamp datetime 
    ,p_bitRenameFlag bit
    ,p_nvcrSupplierID NVARCHAR (500)
    ,p_BitIsPNFStopper NVARCHAR(50)   
    ,p_intpartialuploadid int        
	-- ,p_FileName VARCHAR(500) = '' OUTPUT
)
ThisSP:Begin   
 
 
  /*
 -- declare  p_FileName nvarchar (50) default Null;
 
 declare p_intpartialuploadid int default 201;
 -- declare p_FileName nvarchar(50) default 'Yogesh'; 
 declare p_bitRenameFlag int default 0;
declare p_vcrBatchName nvarchar(50) default 'Yogesh' ;
declare p_intDipBagDynamicId int; 
declare p_intSourceMDM_BatchesId int default 14234; 
declare p_intBatchId int default 101;
Declare p_sdtmDiPBagDynamicRecordDT nvarchar(50);
DECLARE v_Start VARCHAR(50) DEFAULT 'Start';
declare v_intDipBagDynamicId int DEFAULT 101;
DECLARE v_DipbagDynamicDT DATETIME(3) DEFAULT LEFT(p_sdtmDiPBagDynamicRecordDT, position('.' in p_sdtmDiPBagDynamicRecordDT) - 1); 
Declare v_nvcrSupplierID nvarchar(50) default '';	
declare p_BitIsPNFStopper    tinyint(4) default 0;
 declare v_intBatchId int default 101; 
 declare v_intMDM_BatchesId int;
 declare v_stop nvarchar(50);
 
*/
      declare p_FileName nvarchar(50);
		DECLARE v_id INT;
		
		DECLARE v_Stop VARCHAR(50) DEFAULT 'Stop'; -- ------------------Yogesh
		Declare v_Continue varchar (50) Default 'Continue'; -- -----Yogesh
		DECLARE v_intStatusId INT DEFAULT 6; -- - statusid  6 for Started
		DECLARE v_DipbagDynamicDT DATETIME(3) DEFAULT LEFT(p_sdtmDiPBagDynamicRecordDT, position('.' in p_sdtmDiPBagDynamicRecordDT) - 1);
/*
		IF p_Status = 8 THEN -- Manually Update 
			SET v_intStatusId = p_Status;
		END IF;
		
		-- insert into mdmBatch after truncate 
		-- Truncate table MDM_Batches
	/* print 'mess' */	
    /*
    */
    


   
   
    set p_FileName = '' ;
		INSERT INTO MDM_Batches_MDM (
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
            ,nvcrSupplierID
			)
		VALUES (
			101 -- p_intBatchId
			,'ABC'  -- ,p_vcrBatchName
			,1   -- v_intStatusId
			-- ,''-- ,v_DipbagDynamicDT
			,777   -- ,p_intDipBagDynamicId
			,111  -- ,p_intSourceMDM_BatchesId
			,0
			-- ,''-- ,p_dtmTimestamp
             ,0   -- ,p_bitRenameFlag
             ,5
            ,''-- ,p_nvcrSupplierID
			);
		SET v_id = LAST_INSERT_ID();
		
		
        

    
    
CALL SendMail_BatchInitiate_5 (@intMDM_BatchesId = v_id
		   ,@vcrStatus = v_Start);	
		



		UPDATE MDM_Batches_MDM	SET intStatusId = 7 WHERE intMDM_BatchesId = v_id and IntWorkFlowID=5;

		-- truncate table batchCrawlDataStag	
		TRUNCATE TABLE BatchCrawlDataStag_ECUBE_MDM_5;
		TRUNCATE TABLE BatchCrawlDatafinal_ECUBE_MDM_5;

		-- Create temp table 
		DROP TEMPORARY TABLE IF EXISTS BatchCrawlData;
		CREATE TEMPORARY TABLE BatchCrawlData (
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
            ,nvcrCost     nvarchar(500)
		   ,nvcrCostCurrency nvarchar(500)
			,nvcrTaxIncluded nvarchar(500)
			,nvcrIncluded1 nvarchar(500)
			,nvcrTAXNotIncluded nvarchar(500)
			,nvcrNotIncluded1 nvarchar(500)
			,nvcrTAX$Included nvarchar(500)
			,nvcrCurrencyIncluded nvarchar(500)
			,nvcrIncluded2 nvarchar(500)
			,nvcrTAX$NotIncluded nvarchar(500)
			,nvcrCurrencyNotIncluded nvarchar(500)
			,nvcrNotincluded2 nvarchar(500)
			,nvcrRoomChar nvarchar(1000)
			,nvcrMultipleZoneCheck nvarchar(2000)
			);
			
/*
Insert into tbl_LogDetails (IntBatchID, IntdipbagdynamicID, nvcrMessageDescription)
 Values(p_intBatchId,p_intDipBagDynamicId,'Start Error Check new');
 */
	
	truncate table `TempQA_ECUBE_MDM_5`;
					   /*insert into 	TempQA_ECUBE_MDM_5 Change*/
                       
CALL GetBatchDataAfterErrorCheck_New (0,v_intDipBagDynamicId,v_nvcrSupplierID); -- -25756


	/*	
Insert into tbl_LogDetails (IntBatchID, IntdipbagdynamicID, nvcrMessageDescription)
 Values(p_intBatchId,p_intDipBagDynamicId,'END Error Check new');
 

 
 Insert into tbl_LogDetails (IntBatchID, IntdipbagdynamicID, nvcrMessageDescription)
 Values(p_intBatchId,p_intDipBagDynamicId,'Start Hotel count');
	
*/
	
	truncate table  `Hotel_Count_Ecube_MDM_5` ;

	
	/*	insert into Hotel_Count_Ecube_MDM_5 Change(Ch_Date,Night,Supplier,Hotel_Count,Previous_Crawl_Count,Previous_Crawl_Diff,CurrentMatchCount,PreviousMatchCount,MatchingPercent)*/
	
    call GetHotelCount (@intBatchId,@intDipBagDynamicId);
	

 /*
 Insert into tbl_LogDetails (IntBatchID, IntdipbagdynamicID, nvcrMessageDescription)
 Values(p_intBatchId,p_intDipBagDynamicId,'End Hotel count');
	*/




	truncate table `TempQAStop_ECUBE_MDM_5`;


IF p_BitIsPNFStopper='T'
Then 
/*	
 Insert into tbl_LogDetails (IntBatchID, IntdipbagdynamicID, nvcrMessageDescription)
 Values(p_intBatchId,p_intDipBagDynamicId,'Start Upload update');
*/
	/*insert into TempQAStop_ECUBE_MDM_5* Change*/
	
    CALL GetReportUploadUpdate (v_intBatchId,v_intDipBagDynamicId,v_nvcrSupplierID);

/*
 Insert into tbl_LogDetails (IntBatchID, IntdipbagdynamicID, nvcrMessageDescription)
 Values(p_intBatchId,p_intDipBagDynamicId,'END Upload update');
*/

-- select  * from TempQAStop_ECUBE_MDM_2 --where [Status] like '%Failed%'


 IF EXISTS (select * from TempQAStop_ECUBE_MDM_5  where `Status` like '%Fail%' limit 1)
THEN
 

	CALL `SendMail_STOP_ECUBE_MDM_5` (v_intMDM_BatchesId = v_id
		   ,@vcrStatus = v_Stop	);
	CALL Batch_SuccesFullExecution_ECUBE_MDM_5( 0, 105);
	  -- LEAVE ThisSP;
    /*'leave sp_lbl;'*/
	else 
	
	
	/* print 'START 3' */

			CALL `SendMail_STOP_ECUBE_MDM_5` (v_intMDM_BatchesId = v_id
			   ,@vcrStatus = v_Stop	);
		end if; 
	
END IF;

/* print 'GOO' */


IF p_BitIsPNFStopper='F'

Then 	

/* print '11' */

/*
 Insert into tbl_LogDetails (IntBatchID, IntdipbagdynamicID, nvcrMessageDescription)
 Values(p_intBatchId,p_intDipBagDynamicId,'Start Upload update Falsee');
*/



	/*insert into TempQAStop_ECUBE_MDM_5 change */ 
	CALL GetReportUploadUpdate (v_intBatchId,v_intDipBagDynamicId,v_nvcrSupplierID);

/*
 Insert into tbl_LogDetails (IntBatchID, IntdipbagdynamicID, nvcrMessageDescription)
 Values(p_intBatchId,p_intDipBagDynamicId,'END Upload update Falsee');
*/

/* print '2' */



 IF EXISTS (select  * from TempQAStop_ECUBE_MDM_5 limit 1)

THEN
	CALL `SendMail_STOP_ECUBE_MDM_5` (v_intMDM_BatchesId = v_id
		   ,@vcrStatus = v_Continue	);
	
	
END IF;	


/* print '3 Bhushan' */
	

		IF EXISTS (select  * from TempQAStop_ECUBE_MDM_5 where intstatus=1)
		THEN 
        drop table if EXISTS  TempQAStop_ECUBE_MDM_5_TEMP;
        
         create temporary table TempQAStop_ECUBE_MDM_5_TEMP (
				id	int(11)  ,
				QA_Checks	longtext ,
				Status	varchar(50) ,
				nvcrComment	longtext ,
				intstatus	int(11) 
);
        
		-- select  * from TempQAStop_ECUBE_MDM_2
			insert into TempQAStop_ECUBE_MDM_5_TEMP select * From TempQAStop_ECUBE_MDM_5 Where intstatus = 1;
			Truncate Table TempQAStop_ECUBE_MDM_5;
			
			Insert Into TempQAStop_ECUBE_MDM_5 (QA_Checks, Status, nvcrComment, intstatus)
			Select QA_Checks, `Status`, nvcrComment, intstatus From TempQAStop_ECUBE_MDM_5_TEMP;
			
		/*--print '4';*/
        
			CALL `SendMail_STOP_ECUBE_MDM_5` (v_intMDM_BatchesId = v_id
			,@vcrStatus = v_Stop);	
		
		/* print '4.1' */
        
     drop table TempQAStop_ECUBE_MDM_5_TEMP;
		
			CALL Batch_SuccesFullExecution_ECUBE_MDM_5( 0, 105);
			/*leave sp_lbl;*/
		END IF;	
END IF;




	/*
		 Insert into tbl_LogDetails (IntBatchID, IntdipbagdynamicID, nvcrMessageDescription)
 Values(p_intBatchId,p_intDipBagDynamicId,'Start Last result');
	*/
		-- insert into temp table
		/*INSERT INTO BatchCrawlData Change  */
		CALL LastResult_Report ( v_intBatchId,-1,1,v_nvcrSupplierID);
		



		-- insert data into BatchCrawlDataStage from temptable 
		INSERT INTO BatchCrawlDataStag_ECUBE_MDM_5
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
           ,nvcrCost
			,nvcrCostCurrency
			,nvcrTaxIncluded
			,nvcrIncluded1
			,nvcrTAXNotIncluded
			,nvcrNotIncluded1
			,nvcrTAX$Included
			,nvcrCurrencyIncluded
			,nvcrIncluded2
			,nvcrTAX$NotIncluded
			,nvcrCurrencyNotIncluded
			,nvcrNotincluded2
			,nvcrRoomChar
			,nvcrMultipleZoneCheck
           	FROM BatchCrawlData ; 
/*print; '100'*/
		-- If no data present then send mail and exit sp
		IF NOT EXISTS (
				SELECT *
				FROM BatchCrawlDataStag_ECUBE_MDM_5
				)
		THEN
			-- EXEC SENDMAIL @intMDM_BatchesId  = @id , @vcrStatus ='NoData'
			UPDATE MDM_Batches_MDM	SET intStatusId = 9	WHERE intMDM_BatchesId = v_id and IntWorkFlowID=5;
/* print '101' */


			/*LEAVE sp_lbl;*/
		END IF;





INSERT INTO BatchCrawlDatafinal_ECUBE_MDM_5 ( 
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
            ,nvcrCost
			,nvcrCostCurrency
			,nvcrTaxIncluded
			,nvcrIncluded1
			,nvcrTAXNotIncluded
			,nvcrNotIncluded1
			,nvcrTAX$Included
			,nvcrCurrencyIncluded
			,nvcrIncluded2
			,nvcrTAX$NotIncluded
			,nvcrCurrencyNotIncluded
			,nvcrNotincluded2
			,nvcrRoomChar
			,nvcrMultipleZoneCheck
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
		p_intDipBagDynamicId,
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
           ,nvcrCost
			,nvcrCostCurrency
			,nvcrTaxIncluded
			,nvcrIncluded1
			,nvcrTAXNotIncluded
			,nvcrNotIncluded1
			,nvcrTAX$Included
			,nvcrCurrencyIncluded
			,nvcrIncluded2
			,nvcrTAX$NotIncluded
			,nvcrCurrencyNotIncluded
			,nvcrNotincluded2
			,nvcrRoomChar
			,nvcrMultipleZoneCheck
	FROM   BatchCrawlDataStag_ECUBE_MDM_5;
        







	
		-- set p_FileName = Concat(CAST(@intBatchid As unsigned) , '_', @vcrBatchName , '_', Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  '.csv'); 
	-- 
	IF p_bitRenameFlag = 0
		
		then
		
	SET p_FileName = Concat(CAST(p_intBatchId As unsigned) , '_' , concat(cast(p_intSourceMDM_BatchesId As unsigned)),  '_' ,concat(p_vcrBatchName , '_') ,concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  concat( case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as unsigned) end) ,concat( '.csv')));	
        /*SET p_FileName = CONCAT(CONVERT(VARCHAR, p_intBatchId) , '_' , convert(varchar,p_intSourceMDM_BatchesId) , '_' , p_vcrBatchName , '_' , REPLACE(DATE_FORMAT (p_dtmTimestamp, '%d/%m/%Y'), '/', '') + REPLACE(DATE_FORMAT (p_dtmTimestamp, '%T'), ':', '') + case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as varchar(1)) end , '.csv');*/
		
		 
		 ELSE
		 
	SET p_FileName = Concat(CAST(@intBatchid As unsigned) , '_' , concat(cast(@intSourceMDM_BatchesId As unsigned)),  '_' ,concat(@vcrBatchName , '_') ,concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  concat( case @intpartialuploadid when 0 then '' else cast(@intpartialuploadid as unsigned) end) ,concat( 'bis.csv')));		 
	    /*SET p_FileName = CONCAT(CONVERT(VARCHAR, p_intBatchId) , '_' , convert(varchar,p_intSourceMDM_BatchesId) , '_' , p_vcrBatchName , '_' , REPLACE(DATE_FORMAT (p_dtmTimestamp, '%d/%m/%Y'), '/', '') + REPLACE(DATE_FORMAT (p_dtmTimestamp, '%T'), ':', '')  +  case p_intpartialuploadid when 0 then '' else CONVERT(VARCHAR, p_intpartialuploadid)  end , 'bis.csv'); */ 	
		
		end if;
		-- print @Filename
 select p_FileName;
		UPDATE MDM_Batches_MDM 	SET vcrFileName = p_FileName WHERE intMDM_BatchesId = v_id and IntWorkFlowID=5;
	end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetTableData_Hotel_Avail_DETAIL_R` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
