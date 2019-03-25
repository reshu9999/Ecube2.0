DELIMITER ;;

CREATE PROCEDURE `GetTableData_Hotel_Avail_DETAIL_R`(
	OUT p_intBatchId  INT 
	,p_vcrBatchName VARCHAR(500)
	,OUT p_FileName VARCHAR(500) 
	,p_sdtmDiPBagDynamicRecordDT VARCHAR(50)
	,p_Status VARCHAR(50)
	,p_intDipBagDynamicId INT
	,p_intSourceMDM_BatchesId INT
	,p_dtmTimestamp datetime(3) 
    ,p_bitRenameFlag tinyint
    ,p_nvcrSupplierID NVARCHAR (500)
    ,p_BitIsPNFStopper NVARCHAR(50)      
    ,p_intpartialuploadid int       
    ,p_intDetailsReport int
	)
ThisSP:BEGIN 

-- exec [GetTableData_ECUBE_MDM_2] 3287,'Prachi_batch_1','','2016-10-20 17:05:00.000',1,25948,419,'2016-10-20 17:05:00.000',1,'25,20','T'
-- abc
	
		DECLARE v_id INT;
		DECLARE v_Start VARCHAR(50) DEFAULT 'Start';
		DECLARE v_Stop VARCHAR(50) DEFAULT 'Stop'; -- ------------------Yogesh
		Declare v_Continue varchar (50) Default 'Continue'; -- -----Yogesh
		DECLARE v_intStatusId INT DEFAULT 6; -- - statusid  6 for Started
		DECLARE v_DipbagDynamicDT DATETIME(3) DEFAULT LEFT(p_sdtmDiPBagDynamicRecordDT, position('.' in p_sdtmDiPBagDynamicRecordDT) - 1); 

		IF p_Status = 8 THEN -- Manually Update 
			SET v_intStatusId = p_Status;
		END IF;
		
		-- insert into mdmBatch after truncate 
		-- Truncate table MDM_Batches_Hotel_Avail
	/* print 'mess' */	

		SET v_id = LAST_INSERT_ID();
		
	
		UPDATE MDM_Batches_Hotel_Avail	SET `intstatusDETAIL_R` = 7 WHERE intMDM_BatchesId = v_id; -- -and IntWorkFlowID=2

		-- truncate table batchCrawlDataStag	
		TRUNCATE TABLE `BatchCrawlDatafinal_Hotel_Avail_DETAIL_R`;


		-- Create temp table 
		DROP TEMPORARY TABLE IF EXISTS BatchCrawlData_detail;
		CREATE TEMPORARY TABLE BatchCrawlData_detail (
			ReportDelivery VARCHAR(500)
			,Hotel nvarchar(2000)
			,HotelCode VARCHAR(1000)
			,ContractManager nvarchar(500)
			,YieldManager nvarchar(500)
			,DemandGroup VARCHAR(500)
			,Segmentation VARCHAR(500)
			,ChainName nvarchar (4000)
			,Status nvarchar (500)
			,HotelContractingType nvarchar(1000) 
			,TPS nvarchar(500) 
			,Dates nvarchar(1000) 
			,leadtime nvarchar(1000) 
			,PointOfSale nvarchar(4000) 
			,Currency nvarchar(4000) 
			,BedsonlinePrice nvarchar(4000) 
			,BedsonlineRoomType nvarchar(4000) 
			,BedsonlineBoardType nvarchar(2000) 
			,ContractName nvarchar(500) 
			,RoomAvailability nvarchar(4000) 
			,BedsOnlinePageURL nvarchar(4000) 
			,CompetitorName nvarchar(500) 
			,CompetitorPrice nvarchar(500) 
           ,CompetitorRoomType  nvarchar(500) 
           ,CompetitorBoardType nvarchar(500) 
           ,CompetitorPageURL nvarchar(4000) 
           ,Destination nvarchar(500) 
           ,DestinationCode nvarchar(500) 
			
			);
			

		CALL DetailsSection (v_intDipBagDynamicId);
		
		
		


/*
		-- insert data into BatchCrawlDataStage from temptable 
		INSERT INTO BatchCrawlDatafinal_Hotel_Avail_DETAIL_R
					Select * From (
			SELECT 
				ROW_NUMBER() Over(Partition By [ReportDelivery] Order by Cast(`HotelCode` As Int)  Desc ,convert(date, Dates, 103)) As SR_No
			, ReportDelivery
			  ,Hotel
			  ,HotelCode
			  ,ContractManager
			  ,YieldManager
			  ,DemandGroup
			  ,Segmentation
			  ,ChainName
			  ,Status
			  ,HotelContractingType
			  ,TPS
			  ,Dates
			  ,leadtime
			  ,PointOfSale
			  ,Currency
			  ,BedsonlinePrice
			  ,BedsonlineRoomType
			  ,BedsonlineBoardType
			  ,ContractName
			  ,RoomAvailability
			  ,BedsOnlinePageURL
			  ,CompetitorName
			  ,CompetitorPrice
			  ,CompetitorRoomType
			  ,CompetitorBoardType
			  ,CompetitorPageURL
  				,@intBatchid  intBatchid
				,@intSourceMDM_BatchesId intSourceMDM_BatchesId
				,@intDipBagDynamicId intDipBagDynamicId
				,@vcrBatchName vcrBatchName
				,Destination
				,DestinationCode
           	FROM BatchCrawlData_detail  
           	)A Order by 1 desc


*/

		IF NOT EXISTS (
				SELECT *
				FROM BatchCrawlDatafinal_Hotel_Avail_DETAIL_R
				)
		THEN
			-- EXEC SENDMAIL @intMDM_BatchesId  = @id , @vcrStatus ='NoData'
			UPDATE MDM_Batches_Hotel_Avail	SET `intstatusDETAIL_R` = 9	WHERE intMDM_BatchesId = v_id; -- -and IntWorkFlowID=2
/* print '101' */
			LEAVE ThisSP;
		END IF;



		IF p_bitRenameFlag = 0
		

		then
		
		-- print 'hiii'
		SET p_FileName = Concat(CAST(@intBatchid As unsigned) , '_' , concat(cast(@intSourceMDM_BatchesId As unsigned)),  '_' ,concat(@vcrBatchName , '_') ,concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  concat( case @intpartialuploadid when 0 then '' else cast(@intpartialuploadid as unsigned) end) ,concat('.xls')));	
	-- SET p_FileName = CONCAT(CONVERT(VARCHAR, p_intBatchId) , '_' , p_vcrBatchName , '_' , REPLACE(DATE_FORMAT (p_dtmTimestamp, '%d/%m/%Y'), '/', '') + REPLACE(DATE_FORMAT (p_dtmTimestamp, '%T'), ':', '') + case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as varchar(1)) end , '.xls');
		
		
		 ELSE
		 -- , concat(cast(@intSourceMDM_BatchesId As unsigned))
           SET p_FileName = Concat(CAST(@intBatchid As unsigned) , '_' ,concat(@vcrBatchName , '_') ,concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  concat( case @intpartialuploadid when 0 then '' else cast(@intpartialuploadid as unsigned) end) ,concat('.xls')));
	    -- SET p_FileName = CONCAT(CONVERT(VARCHAR, p_intBatchId) , '_' , p_vcrBatchName , '_' , REPLACE(DATE_FORMAT (p_dtmTimestamp, '%d/%m/%Y'), '/', '') + REPLACE(DATE_FORMAT (p_dtmTimestamp, '%T'), ':', '') + case p_intpartialuploadid when 0 then '' else CONVERT(VARCHAR, p_intpartialuploadid)  end ,'.xls'); 	

		 end if; 
	

		UPDATE MDM_Batches_Hotel_Avail 	SET vcrFileName = p_FileName WHERE intMDM_BatchesId = v_id; -- and IntWorkFlowID=2
	END ;;
