DELIMITER ;;

CREATE PROCEDURE `sp_LastResult_BK_18June2018`(            
  p_intBatchId  int,        
  p_intDipBagDynId int ,
  p_nvcrSupplierID varchar(4000) 
)
BEGIN                  
  

	DECLARE  v_intDiPBagDynamicId int;            
	DECLARE v_nvcrPointofsalsecode nvarchar(100);            
	DECLARE v_intUserId int;            
	DECLARE v_tintReportType tinyint unsigned; 
    DECLARE v_nvcrSupplierIDExcludeSavePageUrl Varchar(500);
	Declare v_intDiPBagDynamicId_LeadTime Int Default 0;
	Declare v_nvcrBatchName nvarchar(100) Default '';
    DECLARE v_adhocbatchcount int;
    Declare v_NvcrAccountName Longtext Default '';
	Declare v_NvcrPrimarySupplier Longtext Default '';
    declare rows int;
	declare rows_deleted int;
    
	select RequestName into v_nvcrBatchName from tbl_RequestMaster where  RequestId = p_intBatchId;
        
	SET   v_tintReportType = 2;            
 
	Drop Temporary Table If exists MstPrimarySupplier;        
	CREATE TEMPORARY TABLE MstPrimarySupplier        
	(        
		intUkID int unique auto_increment ,        
		intSupplierId int NOT NULL,        
		nvcrSupplierName nvarchar(50) NOT NULL                  
	);        
	
    
	INSERT INTO MstPrimarySupplier(intSupplierId, nvcrSupplierName)        
	SELECT Id, name        
	FROM tbl_Competitor
	WHERE Id in (6,25,37,46,70,71,72,73,74,75,76,1);          
       
          
         
	Drop Temporary Table If exists TEMP_BCD;
	CREATE TEMPORARY TABLE TEMP_BCD            
	(            
	Timestamp   NVARCHAR(100) ,  Company    NVARCHAR(100) ,            
	Dates    NVARCHAR(100) ,  Nights    INT ,            
	Hotel    NVARCHAR(1000) ,  HotelId    BIGINT ,            
	PointOfSale   NVARCHAR(100) ,  City    NVARCHAR(100) ,            
	State    NVARCHAR(100) ,  Country    NVARCHAR(100) ,            
	DailyRate   NVARCHAR(100) ,  Rcode    NVARCHAR(100) ,            
	Tax     NVARCHAR(100) ,  RoomType   NVARCHAR(256) ,            
	RoomCode   NVARCHAR(100) ,  Supplier   NVARCHAR(1000) ,            
	CancellationPolicy NVARCHAR(100) ,  StarRating   NVARCHAR(100) ,            
	Star    NVARCHAR(100) ,  Price    DECIMAL(15,4) ,            
	Currency   NVARCHAR(100) ,  BreakFast   NVARCHAR(100) ,            
	Availability  NVARCHAR(100) ,  Board    NVARCHAR(100) ,            
	Uniquecode   NVARCHAR(100) ,  Status    NVARCHAR(200) ,            
	PageURL    LONGTEXT,  HotelCode   NVARCHAR(100) ,            
	ContractName  NVARCHAR(100) ,  Classification  NVARCHAR(100) ,            
	Integration NVARCHAR(100) ,         
	B2B     NVARCHAR(100) ,  ComOfici   NVARCHAR(100) ,            
	ComCanal   NVARCHAR(100) ,  ComNeta    NVARCHAR(100) ,            
	nvcrHotelCode  NVARCHAR(100) ,  tintReportType  TINYINT UNSIGNED ,            
	intMSTHotelId  BIGINT,    intSupplierId  INT,nvcrHotelName  NVARCHAR(1000),        
	nvcrNetPrice   NVARCHAR(255),          
	nvcrSellingPrice  NVARCHAR(255),          
	nvcrCommision   NVARCHAR(255),          
	nvcrDirectPayment  NVARCHAR(255),          
	nvcrSellingPriceMandatory NVARCHAR(255),        
	nvcrXmlroomtypecode nvarchar(50),        
	nvcrPromotion  nvarchar(255),        
	nvcrPromotionDescription nvarchar(255),nvcrHotelCount nvarchar(255),nvcrTotalHotel nvarchar(255)        
	, nvcrEventType nvarchar(20)        
	,Unq_HotelID BIGINT           
	,strSupplier nvarchar(255)     
	,nvcrRoomAvailability nvarchar(255)     
	,nvcrAdult nvarchar(100)  
	,nvcrOpaqueRate nvarchar(100)
	,nvcrLeadTime longtext
	,nvcrAccountName nvarchar(255)  
	,nvcrDynamicProperty nvarchar(50)
	, nvcrHotelAddress1 Longtext 
	,dtmCrawlDateTime DateTime(3)  
	,sdtmCheckinDate DATETIME 
	,intDiPBagDynamicId int 
	,nvcrCity Longtext 
	,sdtmCheckoutDate DATETIME  	 
	,nvcrSupplierHotelURL LONGTEXT 
	,nvcrCompetitorHotelID NVARCHAR(50) 
	,nvcrLongitude NVARCHAR(50)
	,nvcrLatitude NVARCHAR(50)    	 
	,NvcrCost NVARCHAR(50)
	,NvcrCostCurrency NVARCHAR(50)
	,NvcrTaxIncluded NVARCHAR(50)
	,NvcrIncluded1 NVARCHAR(50)
	,NvcrTAXNotIncluded NVARCHAR(50)
	,NvcrNotIncluded1 NVARCHAR(50)
	,nvcrTAX$Included NVARCHAR(50)
	,NvcrCurrencyIncluded NVARCHAR(50)
	,NvcrIncluded2 NVARCHAR(50)
	,NvcrTAX$NotIncluded NVARCHAR(50)
	,NvcrCurrencyNotIncluded NVARCHAR(50)
	,nvcrNotincluded2 NVARCHAR(50)
	,nvcrRoomChar NVARCHAR(500) 
	,nvcrMultipleZoneCheck NVARCHAR(500) 
	,nvcrCheckinDates nvarchar(100)
	);  


	 
	IF p_nvcrSupplierID = '' THEN	 
		SELECT Group_Concat(intSupplierId) INTO p_nvcrSupplierID 
		FROM (SELECT DISTINCT intSupplierId FROM BatchCrawlData   
			where intDiPBagDynamicId = p_intDipBagDynId) t ;
	END IF;


	Call sp_split(p_nvcrSupplierID,',');
    
	Drop Temporary Table If exists Temp_SupplierID;        
	CREATE TEMPORARY TABLE Temp_SupplierID        
	(intSupplierId int NOT NULL);

	Truncate Table Temp_SupplierID;
	Insert into Temp_SupplierID
	Select items from SplitValue;
    
	 
	Drop Temporary Table If Exists Temp_BatchCrawlData;
    Create Temporary Table Temp_BatchCrawlData
    As
    Select * From BatchCrawlData bcrDt Where bcrDt.intDipbagDynamicId = p_intDipBagDynId 
    And IntsupplierID in (Select intSupplierId From Temp_SupplierID);

	SELECT  nvcrSupplierIDExcludeSavePageUrl INTO v_nvcrSupplierIDExcludeSavePageUrl 
		FROM MDM_Batches 
	WHERE intDipBagDynamicId=v_intDiPBagDynamicId ORDER BY intMDM_BatchesId DESC Limit 1;

	Call sp_split(v_nvcrSupplierIDExcludeSavePageUrl,',');
    
	Truncate Table Temp_SupplierID;
	Insert into Temp_SupplierID
	Select items from SplitValue Where IfNull(items,"") != "";

  
	
	UPDATE Temp_BatchCrawlData B Inner Join Temp_SupplierID T
		On B.intSupplierId = T.intSupplierId
	SET nvcrPagePath=NULL
	WHERE intDiPBagDynamicId=v_intDiPBagDynamicId; 

	Drop Temporary Table If exists Temp_BatchCrawlData_2;
	CREATE TEMPORARY TABLE Temp_BatchCrawlData_2 LIKE Temp_BatchCrawlData;
	INSERT INTO Temp_BatchCrawlData_2 SELECT * FROM Temp_BatchCrawlData;

	
	Drop Temporary Table If exists MstPrimarySupplier_2;
	CREATE TEMPORARY TABLE MstPrimarySupplier_2 LIKE MstPrimarySupplier;
	INSERT INTO MstPrimarySupplier_2 SELECT * FROM MstPrimarySupplier;

  
	INSERT INTO  TEMP_BCD              
		(Timestamp,Company,Dates,Nights,Hotel,HotelId,PointOfSale,City,State,Country,DailyRate,Rcode,          
		Tax,RoomType,RoomCode,Supplier,CancellationPolicy,StarRating,Star,Price,          
		Currency,BreakFast,Availability,Board,Uniquecode,Status,PageURL,HotelCode,ContractName,          
		Classification,Integration, B2B,ComOfici,ComCanal,ComNeta,nvcrHotelCode,tintReportType,intMSTHotelId,intSupplierId,nvcrHotelName        
		,nvcrNetPrice, nvcrSellingPrice, nvcrCommision, nvcrDirectPayment, nvcrSellingPriceMandatory, nvcrXmlroomtypecode        
		,nvcrPromotion, nvcrPromotionDescription, nvcrHotelCount, nvcrTotalHotel, nvcrEventType        
		,Unq_HotelID,strSupplier,nvcrRoomAvailability,nvcrAdult,nvcrOpaqueRate,nvcrLeadTime,nvcrAccountName,nvcrDynamicProperty
		, nvcrHotelAddress1 
		,dtmCrawlDateTime    
		,sdtmCheckinDate   
		,intDiPBagDynamicId   
		,nvcrCity  
		,sdtmCheckoutDate 
		,nvcrSupplierHotelURL 
		,nvcrCompetitorHotelID  
		,nvcrLongitude 
		,nvcrLatitude 
		,NvcrCost
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
		,nvcrCheckinDates 
		)         
	  
	SELECT          
		(Concat(Date_format(dtmCrawlDateTime, '%d/%m/%Y') , ' ' , Date_format(dtmCrawlDateTime,'%T'))) `Timestamp`,               
        
		mstSupp.DisplayName Company, 
		sdtmCheckinDate Dates,         
		Timestampdiff(day,sdtmCheckinDate,sdtmCheckoutDate) Nights,               
		'' Hotel,            
		0  HotelId,                 
		MSTPosCode.CountryCode PointOfSale,                      
		mstC.CityCode City,            
		'' State,            
		MC.CountryCode Country,            
		replace(Convert(Replace(nvcrDailyRate,',',''), decimal(14,2)),'','.') As `DailyRate`, 
		nvcrRcode Rcode,            
		nvcrtax Tax,            
		nvcrroomtype `RoomType`,            
		-- (select Max(nvcrroomtypematch) from vw_HotelStandardization where nvcrroomtype like   CONCAT(bcrDt.NVCRROOMTYPE ,'%') ) `RoomCode`,
        '' `RoomCode`,
		bcrDt.nvcrHotelName  Supplier,            
		'' as `CancellationPolicy`,
		-- ifnull((select StarRatingCode from StarRatings where StarRating=Substring(bcrDt.nvcrhotelstar,PatIndex('/',bcrDt.nvcrhotelstar)+1,char_length(rtrim(bcrDt.nvcrhotelstar))-PatIndex('/',bcrDt.nvcrhotelstar)+1)) ,'PENDI') `StarRating` ,            
        "" `StarRating` ,
		SUBSTRING(bcrDt.nvcrHotelStar,CHAR_LENGTH(RTRIM(bcrDt.nvcrHotelStar)),1) Star,            
		Convert(mnyRate,decimal(14,2)) Price,            
		nvcrCurrency as Currency,            
		Case nvcrBreakFast When '0' Then 'No' When '1' Then 'Yes' End BreakFast,            
		nvcrAvailabilty as Availability,            
		nvcrBoard  as Board,            
		nvcrUniqueCode as `Uniquecode`,            
		nvcrCrawlDescription  as Status,            
		CONCAT('=HYPERLINK("' , nvcrPagePath , '","info")')PageURL,        
		'' as `HotelCode`,            
		nvcrContractName as `ContractName`,            
		case when nvcrClassification like '%~%' then SPLIT_STR(nvcrClassification,'~',1) else nvcrClassification end As `Classification`,        
		case when nvcrClassification like '%~%' then SPLIT_STR(nvcrClassification,'~',2) else '' end As `Integration`,        
        SupplierCode  as B2B,            
		null  as `ComOfici`,   
		null as `ComCanal`,   
		null as `ComNeta`,    
		nvcrHotelCode as nvcrHotelCode,            
		2 as tintReportType,            
		MH.HotelId as HotelId,            
		bcrDt.intSupplierId as intSupplierId,            
		MH.HotelName  as nvcrHotelName,        
		bcrDt.nvcrNetPrice     `NetPrice`,          
		bcrDt.nvcrSellingPrice    `SellingPrice`,          
		bcrDt.nvcrCommision     `Commission`,          
		bcrDt.nvcrDirectPayment    `DirectPayment`,          
		bcrDt.nvcrSellingPriceMandatory  `SellingPriceMandatory`,        
		bcrDt.nvcrXmlroomtypecode `Xmlroomtypecode`,        
		bcrDt.nvcrPromotion as nvcrPromotion,         
		bcrDt.nvcrPromotionDescription as nvcrPromotionDescription,        
		bcrDt.nvcrHotelCount as nvcrHotelCount,         
		bcrDt.nvcrTotalHotel as nvcrTotalHotel,        
		'' as nvcrEventType, 
		MH.HotelId 
		,bcrDt.strSupplier as strSupplier 
		,bcrDt.nvcrRoomAvailability as nvcrRoomAvailability     
		,bcrDt.nvcrAdult as nvcrAdult ,bcrDt.nvcrOpaqueRate,bcrDt.nvcrLeadTime         
		,AC.nvcrAccName as nvcrAccountName
		,bcrDt.nvcrDynamicProperty as nvcrDynamicProperty
		, MH.HotelAddress1 
		,dtmCrawlDateTime    
		,sdtmCheckinDate   
		,bcrDt.intDiPBagDynamicId   
		,bcrDt.nvcrCity  
		,sdtmCheckoutDate 	
		,bcrDt.nvcrSupplierHotelURL 
		,bcrDt.nvcrCompetitorHotelID  
		,MH.Longitude 
		,MH.Latitude 
		,bcrDt.NvcrCost
		,bcrDt.NvcrCostCurrency
		,bcrDt.NvcrTaxIncluded
		,bcrDt.NvcrIncluded1
		,bcrDt.NvcrTAXNotIncluded
		,bcrDt.NvcrNotIncluded1
		,bcrDt.nvcrTAX$Included
		,bcrDt.NvcrCurrencyIncluded
		,bcrDt.NvcrIncluded2
		,bcrDt.NvcrTAX$NotIncluded
		,bcrDt.NvcrCurrencyNotIncluded
		,bcrDt.nvcrNotincluded2
		,bcrDt.nvcrRoomChar 
		,bcrDt.nvcrMultipleZoneCheck 
		,DATE_FORMAT(sdtmCheckinDate,'%d/%m/%Y')          
		FROM  tbl_CountryMaster as MSTPosCode   
		RIGHT OUTER JOIN Temp_BatchCrawlData bcrDt          
		on bcrDt.nvcrCancellationPolicy = MSTPosCode.CountryName  
		LEFT JOIN tbl_Competitor mstSupp             
		ON   bcrDt.intSupplierId = mstSupp.Id             
		INNER JOIN tbl_CountryMaster MC                 
		ON MC.CountryName= bcrDt.nvcrHotelAddress         
		LEFT JOIN Cities mstC             
		ON   bcrDt.nvcrCity = mstC.CityName        
		and mstC.CountryId = MC.CountryId        
		LEFT OUTER JOIN Hotels MH             
		ON   MH.HotelName = bcrDt.nvcrHotelName            
		AND   MH.CityId = mstC.CityId            
		AND   MH.CompetitorId = bcrDt.intSupplierId   	 
		And  Case WHen bcrDt.intSupplierId not in (1,6,25)
		Then Ifnull(MH.WebSiteHotelId,'') 
		Else '1' End = Case when  bcrDt.intSupplierId not in (1,6,25)
		Then Ifnull(bcrDt.nvcrCompetitorHotelID,'')
		Else '1' End
		LEFT JOIN MstPrimarySupplier MP           
		ON   bcrDt.intSupplierId=MP.intSupplierId           
		LEFT JOIN  MSTAccount AC 
		ON bcrDt.nvcrCancellationPolicy= AC.nvcrPos 
		AND mstSupp.`name`=AC.nvcrSupplier                   
		WHERE MP.intSupplierId IS NULL
        

	 UNION ALL        

	SELECT          
		(Concat(Date_format(dtmCrawlDateTime, '%d/%m/%Y') , ' ' , Date_format(dtmCrawlDateTime,'%T'))) Timestamp,               
		mstSupp.DisplayName Company, 
		sdtmCheckinDate Dates,
		Timestampdiff(day,sdtmCheckinDate,sdtmCheckoutDate)   Nights,               
		''                 Hotel,            
		0                 HotelId,                 
		MSTPosCode.CountryCode            PointOfSale,                      
		mstC.CityCode               City,            
		''                 State,            
		MC.CountryCode              Country,            
		replace(Convert(Replace(nvcrDailyRate,',',''), decimal(14,2)),'','.') As `DailyRate`, 
		nvcrRcode                Rcode,            
		nvcrtax                 Tax,            
		nvcrroomtype             `RoomType`,            
		-- (select Max(nvcrroomtypematch) from vw_HotelStandardization  where nvcrroomtype like CONCAT(bcrDt1.NVCRROOMTYPE ,'%') ) `RoomCode`,            
        "" `RoomCode`,
		bcrDt1.nvcrHotelName  Supplier,            
		''         as      `CancellationPolicy`,
		-- ifnull((select StarRatingCode from StarRatings where StarRating=Substring(bcrDt1.nvcrhotelstar,PatIndex('/',bcrDt1.nvcrhotelstar)+1,char_length(rtrim(bcrDt1.nvcrhotelstar))-PatIndex('/',bcrDt1.nvcrhotelstar)+1)) ,'PENDI') `StarRating`,             
        "" `StarRating`,
		SUBSTRING(bcrDt1.nvcrHotelStar,CHAR_LENGTH(RTRIM(bcrDt1.nvcrHotelStar)),1) Star,            
		Convert(mnyRate,decimal(14,2))        Price,            
		nvcrCurrency as Currency,            
		Case nvcrBreakFast When '0' Then 'No' When '1' Then 'Yes' End BreakFast,            
		nvcrAvailabilty as Availability,            
		nvcrBoard  as Board,            
		nvcrUniqueCode as `Uniquecode`,            
		nvcrCrawlDescription  as Status,            
		CONCAT('=HYPERLINK("' , nvcrPagePath , '","info")')PageURL,        
		'' as `HotelCode`,            
		nvcrContractName as `ContractName`,            
		case when nvcrClassification like '%~%' then SPLIT_STR(nvcrClassification,'~',0) else nvcrClassification end As `Classification`,        
		case when nvcrClassification like '%~%' then SPLIT_STR(nvcrClassification,'~',1) else '' end As `Integration`,        
         
		SupplierCode  as B2B,            
		null  as `ComOfici`,    
		null as `ComCanal`,    
		null as `ComNeta`,    
		nvcrHotelCode as nvcrHotelCode,            
		2 as tintReportType,            
		MH.HotelId as HotelId,            
		bcrDt1.intSupplierId as intSupplierId,            
		MH.HotelName  as nvcrHotelName,        
		bcrDt1.nvcrNetPrice     `NetPrice`,          
		bcrDt1.nvcrSellingPrice    `SellingPrice`,          
		bcrDt1.nvcrCommision     `Commission`,          
		bcrDt1.nvcrDirectPayment    `DirectPayment`,          
		bcrDt1.nvcrSellingPriceMandatory  `SellingPriceMandatory`,        
		bcrDt1.nvcrXmlroomtypecode `Xmlroomtypecode`,        
		bcrDt1.nvcrPromotion as nvcrPromotion,         
		bcrDt1.nvcrPromotionDescription as nvcrPromotionDescription,        
		bcrDt1.nvcrHotelCount as nvcrHotelCount,         
		bcrDt1.nvcrTotalHotel as nvcrTotalHotel,        
		'' as nvcrEventType,	       
		MH.HotelId 
		,bcrDt1.strSupplier as strSupplier 
		,bcrDt1.nvcrRoomAvailability as nvcrRoomAvailability       
		,bcrDt1.nvcrAdult as nvcrAdult,bcrDt1.nvcrOpaqueRate,bcrDt1.nvcrLeadTime        
		,AC.nvcrAccName as nvcrAccountName
		,bcrDt1.nvcrDynamicProperty as nvcrDynamicProperty
		, MH.HotelAddress1 
		,dtmCrawlDateTime    
		,sdtmCheckinDate   
		,bcrDt1.intDiPBagDynamicId   
		,bcrDt1.nvcrCity  
		,sdtmCheckoutDate 	
		,bcrDt1.nvcrSupplierHotelURL 
		,bcrDt1.nvcrCompetitorHotelID  
		,MH.Longitude 
		,MH.Latitude 
		,bcrDt1.NvcrCost
		,bcrDt1.NvcrCostCurrency
		,bcrDt1.NvcrTaxIncluded
		,bcrDt1.NvcrIncluded1
		,bcrDt1.NvcrTAXNotIncluded
		,bcrDt1.NvcrNotIncluded1
		,bcrDt1.nvcrTAX$Included
		,bcrDt1.NvcrCurrencyIncluded
		,bcrDt1.NvcrIncluded2
		,bcrDt1.NvcrTAX$NotIncluded
		,bcrDt1.NvcrCurrencyNotIncluded
		,bcrDt1.nvcrNotincluded2

		,bcrDt1.nvcrRoomChar 
		,bcrDt1.nvcrMultipleZoneCheck 
		,DATE_FORMAT(sdtmCheckinDate,'%d/%m/%Y') 
		FROM  tbl_CountryMaster as MSTPosCode               
		RIGHT OUTER JOIN  Temp_BatchCrawlData_2 bcrDt1          
		on bcrDt1.nvcrCancellationPolicy = MSTPosCode.CountryName  
		LEFT JOIN tbl_Competitor mstSupp             
		ON   bcrDt1.intSupplierId = mstSupp.Id             
		INNER JOIN tbl_CountryMaster MC                 
		ON MC.CountryName= bcrDt1.nvcrHotelAddress         
		LEFT JOIN Cities mstC             
		ON   bcrDt1.nvcrCity = mstC.CityName        
		and mstC.CountryId = MC.CountryId        
		LEFT OUTER JOIN Hotels MH             
		ON   MH.WebSiteHotelId = bcrDt1.nvcrHotelCode              
		AND   MH.CityId = mstC.CityId            
		AND   MH.CompetitorId = bcrDt1.intSupplierId     
		And  Case WHen bcrDt1.intSupplierId not in (1,6,25) 
		Then Ifnull(MH.WebSiteHotelId,'') 
		Else '1' End = Case when  bcrDt1.intSupplierId not in (1,6,25)
		Then Ifnull(bcrDt1.nvcrCompetitorHotelID,'')
		Else '1' End
		INNER JOIN MstPrimarySupplier_2 MP           
		ON   bcrDt1.intSupplierId=MP.intSupplierId          
		LEFT JOIN  MSTAccount AC 
		ON bcrDt1.nvcrCancellationPolicy= AC.nvcrPos 
		AND mstSupp.`name`=AC.nvcrSupplier;          
		 



	Update TEMP_BCD T Inner Join HotelRelation HR1
	On T.intMSTHotelId != HR1.HotelRelationComHotelId Inner Join Hotels MH
	On T.intMSTHotelId = MH.HotelId Inner Join Hotels MH1
	On MH.WebSiteHotelId = MH1.WebSiteHotelId 
		And MH.CompetitorId = MH1.CompetitorId
		And MH.CityId = MH1.CityId Inner Join  HotelRelation HR2
	On MH1.HotelId = HR1.HotelRelationComHotelId  
    Set 
		T.intMSTHotelId = MH1.HotelId,
		T.Unq_HotelID = MH1.HotelId;

	-- change Yogesh 
	-- select  count(1) into v_adhocbatchcount from AdhocLeadTime where `Batch_Name` = v_nvcrBatchName;

	 
	if(v_adhocbatchcount = 0) THEN
    
		Drop Temporary Table If Exists temp_Table;
		Create Temporary Table temp_Table
		As
		select p_intDipBagDynId intDiPBagDynamicId, RequestId, LT.intMstLeadTime, LT.nvcrBookingDate, LT.nvcrBatchName, LT.nvcrDestination, 
			LT.nvcrLeadTime, LT.smdtUpdatedDate, LT.intUpdatedUser, LT.intLTime, LT.nvcrType, 
            LT.smdtCheckindate, LT.intNights 
		from MstLeadTimeTemplate LT inner join tbl_RequestMaster BT on LT.nvcrBatchName=BT.RequestName
		where RequestId = p_intBatchId;
		
		Update TEMP_BCD bcrDt LEFT JOIN Cities CT  
			ON bcrDt.nvcrCity = CT.CityName
			left join temp_Table LT
			ON Convert(bcrDt.dtmCrawlDateTime, date)=convert(LT.nvcrBookingDate, Date) 
            set bcrDt.nvcrLeadTime=LT.nvcrLeadTime and CT.CityCode=LT.nvcrDestination 
			and bcrDt.intDiPBagDynamicId=LT.intDiPBagDynamicId  
            and Timestampdiff(day,dtmCrawlDateTime,sdtmCheckinDate)=LT.intLTime
			and Timestampdiff(day,sdtmCheckinDate,sdtmCheckoutDate)=LT.intNights    
			where bcrDt.intDiPBagDynamicId= p_intDipBagDynId and LT.nvcrType='Fixed'; 
     
      
		Update TEMP_BCD bcrDt LEFT JOIN Cities CT  
			ON bcrDt.nvcrCity = CT.CityName LEFT JOIN temp_Table LT 
			ON convert(bcrDt.dtmCrawlDateTime, date)=convert(LT.nvcrBookingDate, date) 
		set bcrDt.nvcrLeadTime=LT.nvcrLeadTime and CT.CityCode=LT.nvcrDestination
			and bcrDt.intDiPBagDynamicId=LT.intDiPBagDynamicId 
            and Convert(bcrDt.sdtmCheckinDate, date) = Convert(LT.smdtCheckindate, date)   
			and Timestampdiff(day,bcrDt.sdtmCheckinDate,bcrDt.sdtmCheckoutDate) = LT.intNights    
		where bcrDt.intDiPBagDynamicId= p_intDipBagDynId and LT.nvcrType='Free';
	
    
  		Update TEMP_BCD bcrDt LEFT JOIN  MstEventTypeTemplate ET 
			on bcrDt.nvcrLeadTime = ET.nvcrLeadTime 
        set bcrDt.nvcrEventType = ET.nvcrEventType 
        where bcrDt.intDiPBagDynamicId=p_intDipBagDynId;
	
		Update TEMP_BCD Set nvcrEventType = 'Free' WHere Ifnull(nvcrEventType,'') = '';
		 			
	ELSE
	 
		Drop Temporary Table If Exists tempAdhocTable;
		Create Temporary Table tempAdhocTable
		As
		select  p_intDipBagDynId intDiPBagDynamicId,LT.intMstAdhocLeadTime,LT.nvcrBookingDate,LT.nvcrBatchName,LT.nvcrDestination,
			   LT.nvcrLeadTime,LT.smdtUpdatedDate,LT.intUpdatedUser,LT.intLTime,LT.nvcrType,LT.smdtCheckindate,
			   LT.intNights,LT.nvcrEventType			  
		from  MstAdhocLeadTimeTemplate LT inner join tbl_RequestMaster BT on LT.nvcrBatchName=BT.RequestName
		where RequestId = p_intBatchId;
 
		 
        
        Update TEMP_BCD bcrDt LEFT JOIN Cities CT  
			ON bcrDt.nvcrCity = CT.CityName
			left join tempAdhocTable LT
			ON convert(bcrDt.dtmCrawlDateTime, date)=convert(LT.nvcrBookingDate, date) 
            and CT.CityCode=LT.nvcrDestination 
			and Timestampdiff(day,dtmCrawlDateTime,sdtmCheckinDate)=LT.intLTime
			and Timestampdiff(day,sdtmCheckinDate,sdtmCheckoutDate)=LT.intNights    
            set bcrDt.nvcrLeadTime=LT.nvcrLeadTime, bcrDt.nvcrEventType=LT.nvcrEventType			
			where bcrDt.intDiPBagDynamicId=p_intDipBagDynId and LT.nvcrType='Fixed';  
      
      
      
       
		Update TEMP_BCD bcrDt   
			LEFT JOIN Cities CT  
			ON bcrDt.nvcrCity = CT.CityName
			LEFT JOIN tempAdhocTable LT 
			ON convert(bcrDt.dtmCrawlDateTime, date)=convert(LT.nvcrBookingDate, date) 
            and CT.CityCode=LT.nvcrDestination
			and bcrDt.intDiPBagDynamicId=LT.intDiPBagDynamicId 
            and Convert(bcrDt.sdtmCheckinDate, date)=Convert(LT.smdtCheckindate, date)   
			and Timestampdiff(day,bcrDt.sdtmCheckinDate,bcrDt.sdtmCheckoutDate)=LT.intNights    
            set	bcrDt.nvcrLeadTime=LT.nvcrLeadTime, bcrDt.nvcrEventType=LT.nvcrEventType			
			where bcrDt.intDiPBagDynamicId=p_intDipBagDynId and LT.nvcrType='Free';		
	 
     
     
		Update TEMP_BCD bcrDt  
		LEFT JOIN  MstEventTypeTemplate ET 
		on bcrDt.nvcrLeadTime=ET.nvcrLeadTime set bcrDt.nvcrEventType = ET.nvcrEventType 
        where bcrDt.intDiPBagDynamicId=p_intDipBagDynId AND Ifnull(bcrDt.nvcrEventType,'') = '';
		
		 
		Update TEMP_BCD Set nvcrEventType = 'Free' WHere Ifnull(nvcrEventType,'') = '';
	END IF;
		
      
	
	Select NvcrAccountName, NvcrPrimarySupplier Into v_NvcrAccountName, v_NvcrPrimarySupplier 
		From  MstLeadTimeTemplate Where nvcrBatchName = v_nvcrBatchName;
 
	Set v_NvcrAccountName = "123";
    Set v_NvcrPrimarySupplier = "1";
    
	If(Ifnull(Ltrim(Rtrim(v_NvcrAccountName)),'') != '' and Ifnull(Ltrim(Rtrim(v_NvcrPrimarySupplier)),'') != '') Then
		
		Call sp_split(v_NvcrAccountName,'/');
		
		Drop Temporary Table If Exists Temp_AccountName; 
		Create Temporary Table Temp_AccountName (ID Int Unique Key Auto_increment, nvcrAccountName Varchar(500), nvcrBatchName Varchar(500));
		Insert Into Temp_AccountName (nvcrAccountName, nvcrBatchName)
		Select items, v_nvcrBatchName From SplitValue;
		
		Call sp_split(v_NvcrPrimarySupplier,'/');
		Drop Temporary Table If Exists Temp_PrimarySupplier;
		Create Temporary Table Temp_PrimarySupplier (ID Int unique key Auto_increment, nvcrPrimarySupplier Varchar(500), nvcrBatchName Varchar(500));
		Insert Into Temp_PrimarySupplier (nvcrPrimarySupplier, nvcrBatchName) 
		Select items, v_nvcrBatchName From SplitValue;
			
					
		Update TEMP_BCD bcrDt Inner JOIN  MstLeadTimeTemplate ET 
			on ET.nvcrBatchName=v_nvcrBatchName Inner Join Temp_AccountName TA
			On ET.nvcrBatchName = TA.nvcrBatchName Inner Join Temp_PrimarySupplier TP
			On ET.nvcrBatchName = TP.nvcrBatchName And TA.ID = TP.ID
			And TP.nvcrPrimarySupplier = bcrDt.Company 
		set bcrDt.nvcrAccountName = TA.NvcrAccountName
			where bcrDt.intDiPBagDynamicId=p_intDipBagDynId;	
			
		Drop Table Temp_AccountName;
		Drop Table Temp_PrimarySupplier;
	End if;
		
	 
   
  
	-- need to discuss with prachi for mentioned column Hotel, HotelId, nvcrHotelCode,   

	    
    UPDATE TEMP_BCD SET Hotel = ifnull(            
		(            
		SELECT  IFNULL(MAX(nvcrHotelName), TEMP_BCD.Supplier)            
		FROM Hotels MH INNER JOIN  HotelRelation HR              
		ON   MH.HotelId = HR.HotelId             
		WHERE  (HotelRelationComHotelId =  TEMP_BCD.intMSTHotelId OR HR.HotelId =  TEMP_BCD.HotelId)            
		),TEMP_BCD.Supplier)              
		WHERE EXISTS            
		(            
			SELECT  HotelRelationID             
			FROM   HotelRelation              
			WHERE  HotelRelationComHotelId = TEMP_BCD.intMSTHotelId
		);            
             
            
          
       
        
        UPDATE TEMP_BCD SET Hotel = IFNULL(            
		(            
		 SELECT  IFNULL(MAX(nvcrHotelName),TEMP_BCD.Supplier)            
		 FROM    Hotels MH               
		 INNER JOIN  HotelRelation HR              
		  ON   MH.HotelId = HR.HotelId             
		  WHERE  (HR.HotelId =  TEMP_BCD.HotelId)            
		 ),TEMP_BCD.Supplier)
		 WHERE NOT EXISTS            
		(             
		 SELECT  HotelRelationID             
		 FROM   HotelRelation              
		 WHERE  HotelRelationComHotelId = TEMP_BCD.intMSTHotelId            		  
		);        
		
                    
		UPDATE TEMP_BCD A12 
		left outer join (
		Select  HR.HotelId HotelId, HotelRelationComHotelId -- ,bitIsManualUnmatch  decide toremoved 01jun18
		From   HotelRelation HR  
			-- where bitIsManualUnmatch = 0  
			order by HotelRelationId desc
		) rel
		on ( rel.HotelRelationComHotelId = A12.HotelId )  
        SET A12.`HotelId` = COALESCE(rel.HotelId, (-1 * A12.HotelId)) 
		WHERE A12.intSupplierId <>  1;  
			        	
		UPDATE TEMP_BCD             
		SET  `HotelCode`  = IFNULL(TEMP_BCD.nvcrHotelCode, (-1 * TEMP_BCD.Unq_HotelID))  -- Added  by Vikas Shukla on 13-Nov-2014 PMS#40388        
		WHERE TEMP_BCD.intSupplierId =1 ;            
		
             
            
  		Update TEMP_BCD T    Inner Join Hotels H
		On H.HotelId = T.HotelId Set T.HotelCode = H.WebSiteHotelId 
		Where T.intSupplierId <>  1;      
		  
		Update TEMP_BCD T  Inner Join Hotels H 
		On H.HotelID = T.HotelId Set T.HotelCode = H.WebSiteHotelId 
		Where T.intSupplierId <> 1;       
		       
		Update TEMP_BCD Set HotelCode = HotelId Where HotelId <0;
		 
		Update TEMP_BCD Set nvcrHotelCode = HotelCode; 
			 
		Update TEMP_BCD T  Inner Join  Hotels H
		On H.HotelId = T.HotelId Set   T.Hotel = H.HotelName
		WHERE T.intSupplierId <>  1;      
				 
		Update TEMP_BCD T   Inner Join Hotels H
		On H.HotelID = T.HotelId Set   T.Hotel = H.HotelName
		WHERE T.intSupplierId <>  1;       
             
 
	if exists(select * from TEMP_BCD where Company= 'Global Market H1' Limit 1) Then 
		
        /*
        Delete A From 
		( 
		select Dense_rank() Over(Partition by country, city, Supplier Order by abs(Cast(HotelID As Integer)) desc) Sr_No,  *  
		from TEMP_BCD  where Company= 'Global Market H1' and hotelid<0
		) A Where SR_no > 1;
        */

		
        
		Set @rn1 = 1;
		Set @Country = 0;
		Set @City = 0;
		Set @Supplier = 0;
						  
		Delete B From 
		(
			Select 
			@rn1 := 
				if(@Country = A.Country && @City = A.City && @Supplier = A.Supplier, 
								If(@HotelId = A.HotelId,@rn1,@rn1 +1)
				,  1) As Rank,  
				
				@Country = A.Country,
				@City = A.City, 
				@Supplier = A.Supplier,
				@HotelId = A.HotelId
			From (
			SELECT  Country, city, Supplier, HotelId
				FROM TEMP_BCD P 
				where Company= 'Global Market H1' and HotelId<0
				Order by abs(Cast(HotelID As Unsigned)) desc  
			) A
		) B  Where Rank > 1;
        
        
        Set @rn1 = 1;
		Set @Country = 0;
		Set @City = 0;
		Set @Supplier = 0;
        /*
		Delete A From 
		( 
		select Dense_rank() Over(Partition by country, city, Supplier Order by Cast(int Hotelsid As Integer) desc) Sr_No,  *  
		from TEMP_BCD  where Company= 'Global Market H1' and hotelid>0
		) A Where SR_no > 1
		*/
		Delete B From 
		(
			Select 
			@rn1 := 
				if(@Country = A.Country && @City = A.City && @Supplier = A.Supplier, 
								If(@HotelId = A.HotelId,@rn1,@rn1 +1)
				,  1) As Rank,  
				
				@Country = A.Country,
				@City = A.City, 
				@Supplier = A.Supplier,
				@HotelId = A.HotelId
			From (
			SELECT  Country, city, Supplier, HotelId
				FROM TEMP_BCD P 
				where Company= 'Global Market H1' and HotelId>0
				Order by abs(Cast(HotelID As Unsigned)) desc  
			) A
		) B  Where Rank > 1;
        
		/*
		Delete A From 
		( 
		select Dense_rank() Over(Partition by country, city, Supplier Order by Cast(HotelID As Integer) desc) Sr_No,  *  
		from TEMP_BCD  where Company= 'Global Market H1'
		) A Where SR_no > 1
        */
        
        
		Set @rn1 = 1;
		Set @Country = 0;
		Set @City = 0;
		Set @Supplier = 0;
						  
		Select * From 
		(
			Select 
			@rn1 := 
				if(@Country = A.Country && @City = A.City && @Supplier = A.Supplier, 
								If(@HotelId = A.HotelId,@rn1+1,@rn1)
				,  @rn1+1) As Rank,  
				
				@Country = A.Country,
				@City = A.City, 
				@Supplier = A.Supplier,
				@HotelId = A.HotelId
			From (
			SELECT  Country, city, Supplier, HotelId
				FROM TEMP_BCD P 
				where Company= 'Global Market H1'  
				Order by Cast(HotelID As Unsigned) desc  
			) A
		) B; 
        
	END IF;
  CALL  sp_LastResult_GeneralRules();           
  
  
 
	/*
	set Rows_Cnt = 1;
	while Rows_Cnt > 0 do
		DELETE Trans from  LastResultQACheck Trans Where intDiPBagDynamicId = p_intDipBagDynId Limit 10000;
		set Rows_Cnt = row_count();
	end while;
  */
  
		DELETE Trans from  LastResultQACheck Trans Where intDiPBagDynamicId = p_intDipBagDynId;
        
 
 Insert INto  LastResultQACheck
	(Timestamp,Company,Dates,Nights,Hotel,HotelId,PointOfSale,City,State,Country,DailyRate,Rcode,Tax,RoomType,RoomCode,Supplier,
		CancellationPolicy,StarRating,Star,Price,Currency,BreakFast,Availability,Board,Uniquecode,Status,PageURL,HotelCode,ContractName,
		Classification,Integration,B2B,ComOfici,ComCanal,ComNeta,nvcrHotelCode,tintReportType,
		nvcrNetPrice,nvcrSellingPrice,nvcrCommision,nvcrDirectPayment,nvcrSellingPriceMandatory,nvcrPromotion,
		nvcrPromotionDescription,nvcrHotelCount,nvcrEventType,strSupplier,nvcrRoomAvailability,nvcrAdult,nvcrOpaqueRate,nvcrLeadTime,
		nvcrAccountName,nvcrDynamicProperty,intMSTHotelId,nvcrHotelAddress1,intDiPBagDynamicId,nvcrCity,nvcrSupplierHotelURL,
		nvcrCompetitorHotelID,nvcrLongitude,nvcrLatitude,NvcrCost
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
			,nvcrCheckinDates 
			)        
   SELECT  `Timestamp`, Substring(Company,1,50) as Company, Dates,            
   Nights, Substring(Hotel,1,250) as Hotel, HotelId,            
   Substring(PointOfSale,1,2) as PointOfSale, Substring(City,1,3) as City, Substring(State,1,50) as State, Substring(Country,1,50) as Country,        
   DailyRate,
   Substring(IFNULL(Rcode,0),1,10) as Rcode, Substring(Tax,1,20) as Tax, Substring(RoomType,1,250)as RoomType,            
   Substring(RoomCode,1,3) as RoomCode, Substring(Supplier,1,250) as Supplier, Substring(CancellationPolicy,1,10) as CancellationPolicy,            
   Substring(StarRating,1,5) as StarRating,     Star,            
   CONVERT(Price, DECIMAL(14,2)) AS Price,         
   Substring(Currency,1,3) as Currency, Substring(BreakFast,1,5) as BreakFast, Substring(Availability,1,50) as Availability,               
   Substring(Board,1,2) as Board, Substring(Uniquecode,1,20) as Uniquecode, Substring(Status,1,50) as Status,              
   case LTRIM(rTrim(intSupplierId))        
    when '8' then  '' 
    when '63' then  '' 
    when '21' then  '' 
    when '60' then  '' 
    when '38' then  '' 
    when '47' then  '' 
    when '68' then  '' 
    when '69' then  '' 
    when '35' then  '' 
    when '57' then  '' 
    when '19' then  '' 
    when '56' then  '' 
    when '42' then  '' 
   else Substring(PageURL,1,250)        
   END as `PageURL`,        
   Substring(HotelCode,1,20) as HotelCode, Substring(ContractName,1,50) as ContractName,            
   Substring(Classification,1,5) as Classification,         
   Substring(Integration,1,10) as Integration, Substring(B2B,1,2) as B2B, 
   CONVERT(ComOfici, DECIMAL(14,2)) AS ComOfici,          
   CONVERT(ComCanal , DECIMAL(14,2)) AS ComCanal,  
   CONVERT(ComNeta, DECIMAL(14,2)) AS ComNeta, nvcrHotelCode,            
   tintReportType   ReportType,        
   CONVERT(nvcrNetPrice, DECIMAL(14,2)) AS `NetPrice`,          
   CONVERT(nvcrSellingPrice, DECIMAL(14,2)) AS `SellingPrice`,        
   CONVERT(nvcrCommision, DECIMAL(14,2)) AS `Commission`,          
   case ltrim(rtrim(Company))         
    when 'Alpharooms' then Substring(nvcrDirectPayment,1,1)        
    when 'Global Market B1' then Substring(nvcrDirectPayment,1,1) 
    when 'Hotelbeds' then Substring(nvcrDirectPayment,1,1)        
    when 'Hotelopia' then Substring(nvcrDirectPayment,1,1)        
    when 'TUI' then Substring(nvcrDirectPayment,1,1)        
    when 'Hotelscom' then Substring(nvcrDirectPayment,1,1)        
    when 'OpaqueRetailPrice' then 'N' 
    when 'Bedsonline'  then Substring(nvcrDirectPayment,1,1)        
    when 'Rumbo'  then Substring(nvcrDirectPayment,1,1)        
    when 'Booking' then 'Y' 
    when 'HRS' then 'Y' 
    when 'Laterooms' then 'Y'
	when 'Starwood' then Substring(nvcrDirectPayment,1,1)  
	when 'Accorhotels' then Substring(nvcrDirectPayment,1,1)
    when 'Travelocity' then Substring(nvcrDirectPayment,1,1)        
    when 'Orbitz' then Substring(nvcrDirectPayment,1,1)        
    when 'Local Market B4' then Substring(nvcrDirectPayment,1,1)
    when 'Local Market B5' then Substring(nvcrDirectPayment,1,1)
    when 'BOLCOM' then Substring(nvcrDirectPayment,1,1)         
    when 'BOLNET' then Substring(nvcrDirectPayment,1,1)         
    when 'HBDNET' then Substring(nvcrDirectPayment,1,1)         
    when 'BOLTH' then Substring(nvcrDirectPayment,1,1)         
    when 'BOLID' then Substring(nvcrDirectPayment,1,1)         
    when 'BOLMY' then Substring(nvcrDirectPayment,1,1)         
    when 'BOLSG' then Substring(nvcrDirectPayment,1,1)         
    when 'Venere' then Substring(nvcrDirectPayment,1,1)          
    when 'ExpediaHotel' then Substring(nvcrDirectPayment,1,1)        
	when 'ExpediaHotel1' then Substring(nvcrDirectPayment,1,1)        
	when 'ExpediaHotel2' then Substring(nvcrDirectPayment,1,1)        
    when 'TravelRepublic' then Substring(nvcrDirectPayment,1,1)
    when 'MuchoViaje' then Substring(nvcrDirectPayment,1,1)
    when 'BestDay' then Substring(nvcrDirectPayment,1,1)
	when 'Ctrip' then Substring(nvcrDirectPayment,1,1)
	when 'Hilton' then Substring(nvcrDirectPayment,1,1)
	when 'Marriot' then Substring(nvcrDirectPayment,1,1)
	when 'Hyatt' then Substring(nvcrDirectPayment,1,1)
    else 'N'        
    end `DirectPayment`,          
   Substring(nvcrSellingPriceMandatory ,1,1) `SellingPriceMandatory`,        
   Substring(nvcrPromotion,1,1) as nvcrPromotion,        
   nvcrPromotionDescription as nvcrPromotionDescription,        
   Cast(nvcrHotelCount As UNSIGNED) as nvcrHotelCount,        
   Substring(nvcrEventType ,1,5) as nvcrEventType        
   ,strSupplier
   ,nvcrRoomAvailability as nvcrRoomAvailability       
    ,nvcrAdult as nvcrAdult ,nvcrOpaqueRate,nvcrLeadTime  
    ,ifnull(nvcrAccountName,'') as  nvcrAccountName
    ,nvcrDynamicProperty as nvcrDynamicProperty
	,intMSTHotelId as intMSTHotelId
    , nvcrHotelAddress1 
	, intDiPBagDynamicId
	  , nvcrCity 	
    ,nvcrSupplierHotelURL 
    ,nvcrCompetitorHotelID  
    ,nvcrLongitude 
	,nvcrLatitude 
	,NvcrCost
			,NvcrCostCurrency
			,NvcrTaxIncluded
			,NvcrIncluded1
			,NvcrTAXNotIncluded
			,NvcrNotIncluded1
			,nvcrTAX$Included as nvcrTAX_Included
			,NvcrCurrencyIncluded
			,NvcrIncluded2
			,NvcrTAX$NotIncluded as NvcrTAX_NotIncluded
			,NvcrCurrencyNotIncluded
			,nvcrNotincluded2    
			,nvcrRoomChar 
			,nvcrMultipleZoneCheck 
			,nvcrCheckinDates 
   FROM  TEMP_BCD;            
   
            
-- Select * From TEMP_BCD;
     
              
END ;;
