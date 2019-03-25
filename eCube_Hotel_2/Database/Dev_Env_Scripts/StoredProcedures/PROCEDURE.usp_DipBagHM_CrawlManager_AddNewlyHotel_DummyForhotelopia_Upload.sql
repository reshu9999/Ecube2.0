DELIMITER ;;

CREATE PROCEDURE `usp_DipBagHM_CrawlManager_AddNewlyHotel_DummyForhotelopia_Upload`(                    
  p_intDiPBagDynamicId int /* =0 */                   
)
Begin
/*******************************************************************         
'	Name					: usp_DipBagHM_CrawlManager_AddNewlyHotel_DummyForhotelopia_Upload
'	Desc					: Add Hotels for Primary Supplier
'	Called by				: 
'	Example of execution	: call usp_DipBagHM_CrawlManager_AddNewlyHotel_DummyForhotelopia_Upload 99

INPUT PARAMETRS		 
	p_intDiPBagDynamicId int
		
OUTPUT PARAMETRS		
	none

'	Created by				: Bhavin Dhimmar
'	Date of creation		: 01-Jun-2018

******************************************************************************************************
Change History
******************************************************************************************************

******************************************************************************************************/

		Declare v_Hotelbeds int;
		Declare v_Bedsonline int;
		Declare v_hotelopia int;
		Declare v_TUI int;
		Declare v_OpaqueRetailPrice int;
		Declare v_PrimarySuppID int;
		Declare v_BOLCOM int;
		Declare v_BOLNET int;
		Declare v_HBDNET int;
		declare v_BOLSG int;
		declare v_BOLMY int;
		declare v_BOLID int;
		declare v_BOLTH int;



		Set v_Hotelbeds = 25;
		Set v_Bedsonline = 6;
		Set v_hotelopia=1;
		Set v_TUI = 37;
		Set v_OpaqueRetailPrice =46;
		Set v_PrimarySuppID = 1;
		Set v_BOLCOM = 70;
		Set v_BOLNET = 71;
		Set v_HBDNET = 72;
		set v_BOLSG = 73;
		set v_BOLMY = 74;
		set v_BOLID = 75;
		set v_BOLTH = 76;
	
		Drop temporary table if exists tmpOtherPrimary;
		CREATE temporary TABLE `tmpOtherPrimary` (
		`intHotelId` int(11) NOT NULL AUTO_INCREMENT,
		`nvcrWebSiteHotelId` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrHotelName` varchar(512) CHARACTER SET utf8 NOT NULL,
		`nvcrHotelAddress1` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrHotelAddress2` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
		`intCityId` int(11) NOT NULL,
		`nvcrHotelBrandName` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrHotelStar` varchar(5) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrHotelPostCode` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
		`intSupplierId` int(11) NOT NULL,
		`tintHotelMatchStatus` tinyint(3) unsigned NOT NULL,
		`nvcrHotelDescription` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
		`intUsrId` int(11) NOT NULL,
		`bitisProceesed` tinyint(4) NOT NULL DEFAULT '0',
		`sdtAddedDateTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
		`nvcrmatchhotelname` varchar(512) CHARACTER SET utf8 DEFAULT NULL,
		`intDipBagSyncId` int(11) DEFAULT NULL,
		`bitIsMailed` tinyint(4) NOT NULL DEFAULT '0',
		`intDiPBagDynamicId` int(11) NOT NULL DEFAULT '0',
		`Unq_HotelID` bigint(20) DEFAULT NULL,
		`nvcrMatchHotelAddress1` varchar(1000) CHARACTER SET utf8 DEFAULT '',
		`bitConsiderForMatching` bit(1) DEFAULT b'1',
		`intStatusID` int(11) DEFAULT NULL,
		`sdtLastAppearnceDate` datetime DEFAULT CURRENT_TIMESTAMP,
		`IntLastDipbagDynamic` bigint(20) DEFAULT '0',
		`nvcrLongitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrLatitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrYieldManager` longtext,
		`nvcrContractManager` longtext,
		`nvcrDemandGroup` longtext,
		`nvcrCrawledHotelAddress` varchar(4000) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrCrawledHotelStar` varchar(5) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrZoneName` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrCrawledZoneName` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
		PRIMARY KEY (`intHotelId`)
		) ;

		insert into tmpOtherPrimary
		(nvcrWebSiteHotelId  ,	nvcrHotelName,nvcrHotelAddress1  ,	nvcrHotelAddress2  ,	intCityId ,	nvcrHotelBrandName  ,	nvcrHotelStar  
        ,	nvcrHotelPostCode  ,	intSupplierId ,	tintHotelMatchStatus ,	nvcrHotelDescription  ,	intUsrId ,	bitisProceesed ,	sdtAddedDateTime 
        ,	nvcrmatchhotelname  ,	intDipBagSyncId ,	bitIsMailed ,	intDiPBagDynamicId  -- ,	Unq_HotelID 
        ,	nvcrMatchHotelAddress1 ,	bitConsiderForMatching ,	intStatusID ,	sdtLastAppearnceDate ,	IntLastDipbagDynamic 
        ,	nvcrLongitude  ,	nvcrLatitude  ,	nvcrYieldManager ,	nvcrContractManager ,	nvcrDemandGroup 
        ,	nvcrCrawledHotelAddress ,	nvcrCrawledHotelStar  ,	nvcrZoneName ,	nvcrCrawledZoneName)
		select WebSiteHotelId,	HotelName,	HotelAddress1,	HotelAddress2,	CityId,	HotelBrandName,	StarRatingId
        ,	HotelPostCode,	CompetitorId,	HotelMatchStatus,	HotelDescription,	CreatedBy ,	isProceesed,	CreatedDate
        ,	matchhotelname,	DipBagSyncId,	IsMailed,	ifnull(RequestId, 0)
		,	MatchHotelAddress1,	isConsiderForMatching,	HotelStatusId,	LastAppearnceDate,	LastRequestRunId
        ,	Longitude,	Latitude,	YieldManager,	ContractManager,	DemandGroup
        ,	CrawledHotelAddress,	CrawledHotelStar,	ZoneName,	CrawledZoneName
		from Hotels 
		where CompetitorId in (v_Hotelbeds,v_Bedsonline,v_TUI,v_OpaqueRetailPrice,v_BOLCOM,v_BOLNET,v_HBDNET,v_BOLSG,v_BOLMY,v_BOLID,v_BOLTH)-- 6,25,37,46,70,71,72,73,74,75,76)--PMS# 32387
		and WebSiteHotelId is not null;


		Drop temporary table if exists tmpOtherPrimaryHotelbedss;
		CREATE temporary TABLE `tmpOtherPrimaryHotelbedss` (
		`intHotelId` int(11) NOT NULL AUTO_INCREMENT,
		`nvcrWebSiteHotelId` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrHotelName` varchar(512) CHARACTER SET utf8 NOT NULL,
		`nvcrHotelAddress1` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrHotelAddress2` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
		`intCityId` int(11) NOT NULL,
		`nvcrHotelBrandName` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrHotelStar` varchar(5) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrHotelPostCode` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
		`intSupplierId` int(11) NOT NULL,
		`tintHotelMatchStatus` tinyint(3) unsigned NOT NULL,
		`nvcrHotelDescription` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
		`intUsrId` int(11) NOT NULL,
		`bitisProceesed` tinyint(4) NOT NULL DEFAULT '0',
		`sdtAddedDateTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
		`nvcrmatchhotelname` varchar(512) CHARACTER SET utf8 DEFAULT NULL,
		`intDipBagSyncId` int(11) DEFAULT NULL,
		`bitIsMailed` tinyint(4) NOT NULL DEFAULT '0',
		`intDiPBagDynamicId` int(11) NOT NULL DEFAULT '0',
		`Unq_HotelID` bigint(20) DEFAULT NULL,
		`nvcrMatchHotelAddress1` varchar(1000) CHARACTER SET utf8 DEFAULT '',
		`bitConsiderForMatching` bit(1) DEFAULT b'1',
		`intStatusID` int(11) DEFAULT NULL,
		`sdtLastAppearnceDate` datetime DEFAULT CURRENT_TIMESTAMP,
		`IntLastDipbagDynamic` bigint(20) DEFAULT '0',
		`nvcrLongitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrLatitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrYieldManager` longtext,
		`nvcrContractManager` longtext,
		`nvcrDemandGroup` longtext,
		`nvcrCrawledHotelAddress` varchar(4000) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrCrawledHotelStar` varchar(5) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrZoneName` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrCrawledZoneName` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
		PRIMARY KEY (`intHotelId`)
		) ;

					
		insert into tmpOtherPrimaryHotelbedss             
		(nvcrWebSiteHotelId  ,	nvcrHotelName,nvcrHotelAddress1  ,	nvcrHotelAddress2  ,	intCityId ,	nvcrHotelBrandName  ,	nvcrHotelStar  
		,	nvcrHotelPostCode  ,	intSupplierId ,	tintHotelMatchStatus ,	nvcrHotelDescription  ,	intUsrId ,	bitisProceesed ,	sdtAddedDateTime 
		,	nvcrmatchhotelname  ,	intDipBagSyncId ,	bitIsMailed ,	intDiPBagDynamicId  -- ,	Unq_HotelID 
		,	nvcrMatchHotelAddress1 ,	bitConsiderForMatching ,	intStatusID ,	sdtLastAppearnceDate ,	IntLastDipbagDynamic 
		,	nvcrLongitude  ,	nvcrLatitude  ,	nvcrYieldManager ,	nvcrContractManager ,	nvcrDemandGroup 
		,	nvcrCrawledHotelAddress ,	nvcrCrawledHotelStar  ,	nvcrZoneName ,	nvcrCrawledZoneName)
		select WebSiteHotelId,	HotelName,	HotelAddress1,	HotelAddress2,	CityId,	HotelBrandName,	StarRatingId
		,	HotelPostCode,	CompetitorId,	HotelMatchStatus,	HotelDescription,	CreatedBy ,	isProceesed,	CreatedDate
		,	matchhotelname,	DipBagSyncId,	IsMailed,	ifnull(RequestId, 0)
		,	MatchHotelAddress1,	isConsiderForMatching,	HotelStatusId,	LastAppearnceDate,	LastRequestRunId
		,	Longitude,	Latitude,	YieldManager,	ContractManager,	DemandGroup
		,	CrawledHotelAddress,	CrawledHotelStar,	ZoneName,	CrawledZoneName
		from Hotels 
		where CompetitorId in (v_hotelopia)-- ,@Bedsonline,@TUI,@OpaqueRetailPrice,@BOLCOM,@BOLNET,@HBDNET,@BOLSG,@BOLMY,@BOLID,@BOLTH)--6,25,37,46,70,71,72,73,74,75,76)--PMS# 32387
		and WebSiteHotelId is not null;

		Drop temporary table if exists tmpOtherPrimarybedsonline;
		CREATE temporary TABLE `tmpOtherPrimarybedsonline` (
		`intHotelId` int(11) NOT NULL AUTO_INCREMENT,
		`nvcrWebSiteHotelId` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrHotelName` varchar(512) CHARACTER SET utf8 NOT NULL,
		`nvcrHotelAddress1` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrHotelAddress2` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
		`intCityId` int(11) NOT NULL,
		`nvcrHotelBrandName` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrHotelStar` varchar(5) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrHotelPostCode` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
		`intSupplierId` int(11) NOT NULL,
		`tintHotelMatchStatus` tinyint(3) unsigned NOT NULL,
		`nvcrHotelDescription` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
		`intUsrId` int(11) NOT NULL,
		`bitisProceesed` tinyint(4) NOT NULL DEFAULT '0',
		`sdtAddedDateTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
		`nvcrmatchhotelname` varchar(512) CHARACTER SET utf8 DEFAULT NULL,
		`intDipBagSyncId` int(11) DEFAULT NULL,
		`bitIsMailed` tinyint(4) NOT NULL DEFAULT '0',
		`intDiPBagDynamicId` int(11) NOT NULL DEFAULT '0',
		`Unq_HotelID` bigint(20) DEFAULT NULL,
		`nvcrMatchHotelAddress1` varchar(1000) CHARACTER SET utf8 DEFAULT '',
		`bitConsiderForMatching` bit(1) DEFAULT b'1',
		`intStatusID` int(11) DEFAULT NULL,
		`sdtLastAppearnceDate` datetime DEFAULT CURRENT_TIMESTAMP,
		`IntLastDipbagDynamic` bigint(20) DEFAULT '0',
		`nvcrLongitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrLatitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrYieldManager` longtext,
		`nvcrContractManager` longtext,
		`nvcrDemandGroup` longtext,
		`nvcrCrawledHotelAddress` varchar(4000) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrCrawledHotelStar` varchar(5) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrZoneName` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
		`nvcrCrawledZoneName` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
		PRIMARY KEY (`intHotelId`)
		) ;

		insert into tmpOtherPrimarybedsonline
		(nvcrWebSiteHotelId  ,	nvcrHotelName,nvcrHotelAddress1  ,	nvcrHotelAddress2  ,	intCityId ,	nvcrHotelBrandName  ,	nvcrHotelStar  
		,	nvcrHotelPostCode  ,	intSupplierId ,	tintHotelMatchStatus ,	nvcrHotelDescription  ,	intUsrId ,	bitisProceesed ,	sdtAddedDateTime 
		,	nvcrmatchhotelname  ,	intDipBagSyncId ,	bitIsMailed ,	intDiPBagDynamicId  -- ,	Unq_HotelID 
		,	nvcrMatchHotelAddress1 ,	bitConsiderForMatching ,	intStatusID ,	sdtLastAppearnceDate ,	IntLastDipbagDynamic 
		,	nvcrLongitude  ,	nvcrLatitude  ,	nvcrYieldManager ,	nvcrContractManager ,	nvcrDemandGroup 
		,	nvcrCrawledHotelAddress ,	nvcrCrawledHotelStar  ,	nvcrZoneName ,	nvcrCrawledZoneName)
		select WebSiteHotelId,	HotelName,	HotelAddress1,	HotelAddress2,	CityId,	HotelBrandName,	StarRatingId
		,	HotelPostCode,	CompetitorId,	HotelMatchStatus,	HotelDescription,	CreatedBy ,	isProceesed,	CreatedDate
		,	matchhotelname,	DipBagSyncId,	IsMailed,	ifnull(RequestId, 0)
		,	MatchHotelAddress1,	isConsiderForMatching,	HotelStatusId,	LastAppearnceDate,	LastRequestRunId
		,	Longitude,	Latitude,	YieldManager,	ContractManager,	DemandGroup
		,	CrawledHotelAddress,	CrawledHotelStar,	ZoneName,	CrawledZoneName
		from Hotels 
		where CompetitorId in (v_hotelopia)-- ,@TUI,@OpaqueRetailPrice,@BOLCOM,@BOLNET,@HBDNET,@BOLSG,@BOLMY,@BOLID,@BOLTH)--6,25,37,46,70,71,72,73,74,75,76)--PMS# 32387
		and WebSiteHotelId is not null;

		Drop temporary table if exists tmpOtherPrimary_copy;
		CREATE TEMPORARY TABLE tmpOtherPrimary_copy LIKE tmpOtherPrimary;
        
        Insert into tmpOtherPrimary_copy (nvcrWebSiteHotelId  ,	nvcrHotelName,nvcrHotelAddress1  ,	nvcrHotelAddress2  ,	intCityId ,	nvcrHotelBrandName  ,	nvcrHotelStar  
			,	nvcrHotelPostCode  ,	intSupplierId ,	tintHotelMatchStatus ,	nvcrHotelDescription  ,	intUsrId ,	bitisProceesed ,	sdtAddedDateTime 
			,	nvcrmatchhotelname  ,	intDipBagSyncId ,	bitIsMailed ,	intDiPBagDynamicId  -- ,	Unq_HotelID 
			,	nvcrMatchHotelAddress1 ,	bitConsiderForMatching ,	intStatusID ,	sdtLastAppearnceDate ,	IntLastDipbagDynamic 
			,	nvcrLongitude  ,	nvcrLatitude  ,	nvcrYieldManager ,	nvcrContractManager ,	nvcrDemandGroup 
			,	nvcrCrawledHotelAddress ,	nvcrCrawledHotelStar  ,	nvcrZoneName ,	nvcrCrawledZoneName)
        select nvcrWebSiteHotelId  ,	nvcrHotelName,nvcrHotelAddress1  ,	nvcrHotelAddress2  ,	intCityId ,	nvcrHotelBrandName  ,	nvcrHotelStar  
			,	nvcrHotelPostCode  ,	intSupplierId ,	tintHotelMatchStatus ,	nvcrHotelDescription  ,	intUsrId ,	bitisProceesed ,	sdtAddedDateTime 
			,	nvcrmatchhotelname  ,	intDipBagSyncId ,	bitIsMailed ,	intDiPBagDynamicId  -- ,	Unq_HotelID 
			,	nvcrMatchHotelAddress1 ,	bitConsiderForMatching ,	intStatusID ,	sdtLastAppearnceDate ,	IntLastDipbagDynamic 
			,	nvcrLongitude  ,	nvcrLatitude  ,	nvcrYieldManager ,	nvcrContractManager ,	nvcrDemandGroup 
			,	nvcrCrawledHotelAddress ,	nvcrCrawledHotelStar  ,	nvcrZoneName ,	nvcrCrawledZoneName
		From tmpOtherPrimary; 
        
		Insert into Hotels
			(WebSiteHotelId, HotelName, HotelAddress1, HotelAddress2
			,CityId, HotelBrandName, StarRatingId, HotelPostCode
			,CompetitorId, HotelMatchStatus, HotelDescription,CreatedBy
			,matchhotelname ,RequestId,Latitude,Longitude
			,YieldManager, ContractManager, DemandGroup, HotelStatusId)
		Select distinct x.nvcrWebSiteHotelId, x.nvcrHotelName, x.nvcrHotelAddress1, x.nvcrHotelAddress2
			, x.intCityId, x.nvcrHotelBrandName, x.nvcrHotelStar, x.nvcrHotelPostCode
			, v_hotelopia as intSupplierId,  tintHotelMatchStatus, x.nvcrHotelDescription, x.intUsrId
			, x.nvcrmatchhotelname, p_intDiPBagDynamicId as intDiPBagDynamicId,nvcrLatitude,nvcrLongitude
			, nvcrYieldManager, nvcrContractManager, nvcrDemandGroup, intStatusID
		FROM  tmpOtherPrimary x
			inner join 
			(
			Select B.nvcrWebSiteHotelId, B.intCityId
			From
				(Select WebSiteHotelId, CityId, HotelId 
				FROM Hotels 
				Where CompetitorId = v_hotelopia -- 1 --
				)A
				right outer join
				(select distinct nvcrWebSiteHotelId,intCityId
				from tmpOtherPrimary_copy 
				)B 
				on  A.WebSiteHotelId = B.nvcrWebSiteHotelId 
					and A.CityId = B.intCityId
				where A.HotelId is null
			)y
			on x.nvcrWebSiteHotelId = y.nvcrWebSiteHotelId
			and x.intCityId = y.intCityId;

		Drop temporary table if exists tmpOtherPrimary_copy;
        
		Drop temporary table if exists tmpOtherPrimaryHotelbedss_copy;
        CREATE TEMPORARY TABLE tmpOtherPrimaryHotelbedss_copy LIKE tmpOtherPrimaryHotelbedss;
        Insert into tmpOtherPrimaryHotelbedss_copy (nvcrWebSiteHotelId  ,	nvcrHotelName,nvcrHotelAddress1  ,	nvcrHotelAddress2  ,	intCityId ,	nvcrHotelBrandName  ,	nvcrHotelStar  
			,	nvcrHotelPostCode  ,	intSupplierId ,	tintHotelMatchStatus ,	nvcrHotelDescription  ,	intUsrId ,	bitisProceesed ,	sdtAddedDateTime 
			,	nvcrmatchhotelname  ,	intDipBagSyncId ,	bitIsMailed ,	intDiPBagDynamicId  -- ,	Unq_HotelID 
			,	nvcrMatchHotelAddress1 ,	bitConsiderForMatching ,	intStatusID ,	sdtLastAppearnceDate ,	IntLastDipbagDynamic 
			,	nvcrLongitude  ,	nvcrLatitude  ,	nvcrYieldManager ,	nvcrContractManager ,	nvcrDemandGroup 
			,	nvcrCrawledHotelAddress ,	nvcrCrawledHotelStar  ,	nvcrZoneName ,	nvcrCrawledZoneName)
        select nvcrWebSiteHotelId  ,	nvcrHotelName,nvcrHotelAddress1  ,	nvcrHotelAddress2  ,	intCityId ,	nvcrHotelBrandName  ,	nvcrHotelStar  
			,	nvcrHotelPostCode  ,	intSupplierId ,	tintHotelMatchStatus ,	nvcrHotelDescription  ,	intUsrId ,	bitisProceesed ,	sdtAddedDateTime 
			,	nvcrmatchhotelname  ,	intDipBagSyncId ,	bitIsMailed ,	intDiPBagDynamicId  -- ,	Unq_HotelID 
			,	nvcrMatchHotelAddress1 ,	bitConsiderForMatching ,	intStatusID ,	sdtLastAppearnceDate ,	IntLastDipbagDynamic 
			,	nvcrLongitude  ,	nvcrLatitude  ,	nvcrYieldManager ,	nvcrContractManager ,	nvcrDemandGroup 
			,	nvcrCrawledHotelAddress ,	nvcrCrawledHotelStar  ,	nvcrZoneName ,	nvcrCrawledZoneName
		From tmpOtherPrimaryHotelbedss; 
        
		Insert into Hotels
		(WebSiteHotelId, HotelName, HotelAddress1, HotelAddress2
		,CityId, HotelBrandName, StarRatingId, HotelPostCode
		,CompetitorId, HotelMatchStatus, HotelDescription,CreatedBy
		,matchhotelname ,RequestId,Latitude,Longitude
		,YieldManager, ContractManager, DemandGroup, HotelStatusId)
		Select distinct x.nvcrWebSiteHotelId, x.nvcrHotelName, x.nvcrHotelAddress1, x.nvcrHotelAddress2
		, x.intCityId, x.nvcrHotelBrandName, x.nvcrHotelStar, x.nvcrHotelPostCode
		, v_Hotelbeds as intSupplierId,  tintHotelMatchStatus, x.nvcrHotelDescription, x.intUsrId
		, x.nvcrmatchhotelname, p_intDiPBagDynamicId as intDiPBagDynamicId,nvcrLatitude,nvcrLongitude
		, nvcrYieldManager, nvcrContractManager, nvcrDemandGroup, intStatusID
		FROM  tmpOtherPrimaryHotelbedss x
		inner join 
		(
			Select B.nvcrWebSiteHotelId, B.intCityId
			From
			(Select WebSiteHotelId, CityId, HotelId 
			FROM Hotels 
			Where CompetitorId = v_Hotelbeds -- 1 --
			)A
			right outer join
			(select distinct nvcrWebSiteHotelId,intCityId
			from tmpOtherPrimaryHotelbedss_copy  
			)B 
			on  A.WebSiteHotelId = B.nvcrWebSiteHotelId 
			and A.CityId = B.intCityId
			where A.HotelId is null
		)y
		on x.nvcrWebSiteHotelId = y.nvcrWebSiteHotelId
			and x.intCityId = y.intCityId;


			
		Drop temporary table if exists tmpOtherPrimaryHotelbedss_copy;
        
        
        Drop temporary table if exists tmpOtherPrimarybedsonline_copy;
        CREATE TEMPORARY TABLE tmpOtherPrimarybedsonline_copy LIKE tmpOtherPrimarybedsonline;
        Insert into tmpOtherPrimarybedsonline_copy (nvcrWebSiteHotelId  ,	nvcrHotelName,nvcrHotelAddress1  ,	nvcrHotelAddress2  ,	intCityId ,	nvcrHotelBrandName  ,	nvcrHotelStar  
			,	nvcrHotelPostCode  ,	intSupplierId ,	tintHotelMatchStatus ,	nvcrHotelDescription  ,	intUsrId ,	bitisProceesed ,	sdtAddedDateTime 
			,	nvcrmatchhotelname  ,	intDipBagSyncId ,	bitIsMailed ,	intDiPBagDynamicId  -- ,	Unq_HotelID 
			,	nvcrMatchHotelAddress1 ,	bitConsiderForMatching ,	intStatusID ,	sdtLastAppearnceDate ,	IntLastDipbagDynamic 
			,	nvcrLongitude  ,	nvcrLatitude  ,	nvcrYieldManager ,	nvcrContractManager ,	nvcrDemandGroup 
			,	nvcrCrawledHotelAddress ,	nvcrCrawledHotelStar  ,	nvcrZoneName ,	nvcrCrawledZoneName)
        select nvcrWebSiteHotelId  ,	nvcrHotelName,nvcrHotelAddress1  ,	nvcrHotelAddress2  ,	intCityId ,	nvcrHotelBrandName  ,	nvcrHotelStar  
			,	nvcrHotelPostCode  ,	intSupplierId ,	tintHotelMatchStatus ,	nvcrHotelDescription  ,	intUsrId ,	bitisProceesed ,	sdtAddedDateTime 
			,	nvcrmatchhotelname  ,	intDipBagSyncId ,	bitIsMailed ,	intDiPBagDynamicId  -- ,	Unq_HotelID 
			,	nvcrMatchHotelAddress1 ,	bitConsiderForMatching ,	intStatusID ,	sdtLastAppearnceDate ,	IntLastDipbagDynamic 
			,	nvcrLongitude  ,	nvcrLatitude  ,	nvcrYieldManager ,	nvcrContractManager ,	nvcrDemandGroup 
			,	nvcrCrawledHotelAddress ,	nvcrCrawledHotelStar  ,	nvcrZoneName ,	nvcrCrawledZoneName
		From tmpOtherPrimarybedsonline; 
        
		Insert into Hotels
		(WebSiteHotelId, HotelName, HotelAddress1, HotelAddress2
		,CityId, HotelBrandName, StarRatingId, HotelPostCode
		,CompetitorId, HotelMatchStatus, HotelDescription,CreatedBy
		,matchhotelname ,RequestId,Latitude,Longitude
		,YieldManager, ContractManager, DemandGroup, HotelStatusId)
		Select distinct x.nvcrWebSiteHotelId, x.nvcrHotelName, x.nvcrHotelAddress1, x.nvcrHotelAddress2
			, x.intCityId, x.nvcrHotelBrandName, x.nvcrHotelStar, x.nvcrHotelPostCode
			, v_Bedsonline as intSupplierId,  tintHotelMatchStatus, x.nvcrHotelDescription, x.intUsrId
			, x.nvcrmatchhotelname, p_intDiPBagDynamicId as intDiPBagDynamicId,nvcrLatitude,nvcrLongitude
			, nvcrYieldManager, nvcrContractManager, nvcrDemandGroup, intStatusID
		FROM  tmpOtherPrimarybedsonline x
			inner join 
			(
				Select B.nvcrWebSiteHotelId, B.intCityId
				From
				(Select WebSiteHotelId,CityId, HotelId 
				FROM Hotels
				Where CompetitorId = v_Bedsonline -- 1 --
				)A
				right outer join
				(select distinct nvcrWebSiteHotelId,intCityId
				from tmpOtherPrimarybedsonline_copy  
				)B 
				on  A.WebSiteHotelId = B.nvcrWebSiteHotelId 
					and A.CityId = B.intCityId
				where A.HotelId is null
			)y
			on x.nvcrWebSiteHotelId = y.nvcrWebSiteHotelId
				and x.intCityId = y.intCityId;

		Drop temporary table if exists tmpOtherPrimarybedsonline_copy;
            
	drop table tmpOtherPrimary;
	drop table tmpOtherPrimarybedsonline;
	drop table tmpOtherPrimaryHotelbedss;

end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-28 18:50:47
