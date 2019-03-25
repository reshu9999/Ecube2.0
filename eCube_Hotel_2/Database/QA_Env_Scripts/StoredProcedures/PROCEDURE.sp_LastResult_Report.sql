DELIMITER ;;

CREATE PROCEDURE `sp_LastResult_Report`(
In p_intDiPBagDynamicId Int,
In p_intBatchID Int,
In p_intSourceMDM_BatchesId Int,
In p_FileName varchar(300)

)
BEGIN


 
	Declare v_vcrBatchName Varchar(1000);
    
    
    INsert into DebugDetails 
    Select p_FileName;
    
	Select vcrBatchName into v_vcrBatchName From MDM_Batches_MDM 
		WHere intSourceMDM_BatchesId = p_intSourceMDM_BatchesId
        order by intSourceMDM_BatchesId desc limit 1 ;

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
        nvcrRoomAvailability,	
		nvcrAdult,    
        nvcrOpaqueRate,        
        nvcrLeadTime,
        nvcrAccountName,    
        nvcrDynamicProperty,  
        HMHotelID,    
        HotelAddress ,  
		intBatchId,
		intDipBagDynamicId,
        nvcrSupplierHotelURL  -- Add new column on 03-06-2016 REQ ID --51430
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
            , FILENAME  
				)
	Select 
	Timestamp,Company,Dates,Nights,Hotel,HotelId,PointOfSale,City,State
    ,Country,DailyRate,Rcode,Tax,RoomType,RoomCode,Supplier,
		CancellationPolicy,StarRating,Star,Price,Currency,BreakFast,Availability,Board,Uniquecode,Status,PageURL,HotelCode,ContractName,
		Classification,Integration,B2B,ComOfici,ComCanal,ComNeta,nvcrHotelCode,tintReportType,
		nvcrNetPrice,nvcrSellingPrice,nvcrCommision,nvcrDirectPayment,nvcrSellingPriceMandatory,nvcrPromotion,
		nvcrPromotionDescription,nvcrHotelCount,nvcrEventType,strSupplier,nvcrRoomAvailability,nvcrAdult,nvcrOpaqueRate,nvcrLeadTime,
		nvcrAccountName,nvcrDynamicProperty,intMSTHotelId,nvcrHotelAddress1,
        p_intBatchID, intDiPBagDynamicId, nvcrSupplierHotelURL,
		nvcrCompetitorHotelID,nvcrLongitude,nvcrLatitude,
         p_intSourceMDM_BatchesId,v_vcrBatchName, NvcrCost
			 ,NvcrCostCurrency
			,NvcrTaxIncluded
			,NvcrIncluded1
			,NvcrTAXNotIncluded
			,NvcrNotIncluded1
			,nvcrTAX$Included
			,NvcrCurrencyIncluded
			,NvcrIncluded2
			,NvcrTAX$NotIncluded
			,NvcrCurrencyNotIncluded
			,nvcrNotincluded2
			,nvcrRoomChar 
			,nvcrMultipleZoneCheck  
            ,p_FileName
			 
		From LastResultQACheck Where intDiPBagDynamicId =p_intDiPBagDynamicId;	
        
       -- select p_FileName; 
       
       -- set sql_safe_updates=0;
       
	   UPDATE BatchCrawlDatafinal_ECUBE_MDM_5 set FILENAME=p_FileName;

	 Delete From LastResultQACheck Where intDiPBagDynamicId = p_intDiPBagDynamicId;

END ;;
