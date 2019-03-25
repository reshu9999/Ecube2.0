DELIMITER ;;

CREATE PROCEDURE `sp_HBService_HMDataCleaning`()
BEGIN
                                
/*=====START: History of duplicate Hotels before delete  =====*/                        
                
  
    DROP TEMPORARY TABLE IF EXISTS TempDuplicateHotels;
	Create Temporary Table  TempDuplicateHotels
    As
	SELECT WebSiteHotelId, CityId, CompetitorId 
	FROM Hotels MH1
	WHERE MH1.CompetitorId NOT IN(1,6,25) 
	AND LTRIM(RTRIM(IFNULL(MH1.WebSiteHotelId,''))) <> ''                        
	GROUP BY WebSiteHotelId, CityId, CompetitorId
	HAVING COUNT(WebSiteHotelId) > 1;
	
	 
    
    DROP TEMPORARY TABLE IF EXISTS TempDeleteDuplicate;
	Create Temporary Table  TempDeleteDuplicate
	(`HotelId` bigint(20) NOT NULL);
    
     
        
    DROP TEMPORARY TABLE IF EXISTS TempDataCleansing;
	CREATE TEMPORARY TABLE TempDataCleansing 
	SELECT  MH.*
	FROM Hotels MH 
	INNER JOIN TempDuplicateHotels Tmp                                                  
	ON MH.CityId = Tmp.CityId
	AND MH.CompetitorId = Tmp.CompetitorId                                                       
	AND LTRIM(RTRIM(MH.WebSiteHotelId)) = LTRIM(RTRIM(Tmp.WebSiteHotelId))            
	ORDER BY MH.HotelId;
    
    
    DROP TEMPORARY TABLE IF EXISTS TempDataCleansing_MaxAddress;
	CREATE TEMPORARY TABLE  TempDataCleansing_MaxAddress(
	`WebSiteHotelId` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
	`MaxHotelAddress` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
	`CityId` int(11) NOT NULL,
	`CompetitorId` int(11) DEFAULT NULL
	);
    
    
    DROP TEMPORARY TABLE IF EXISTS TempDataCleansing_MaxLastAppDate;
	CREATE TEMPORARY TABLE  TempDataCleansing_MaxLastAppDate(
	`WebSiteHotelId` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
	`MaxLastAppDate`  datetime DEFAULT NULL,
	`CityId` int(11) NOT NULL,
	`CompetitorId` int(11) DEFAULT NULL
	);
      
    
    DROP TEMPORARY TABLE IF EXISTS TempAddressUpdate;
	CREATE TEMPORARY TABLE  TempAddressUpdate(
	`HotelId` bigint(20) NOT NULL ,
	`WebSiteHotelId` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
	`HotelName` varchar(512) CHARACTER SET utf8 NOT NULL,
	`HotelAddress1` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
	`HotelAddress2` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
	`CityId` int(11) NOT NULL,
	`HotelBrandName` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
	`StarRatingId` int(11) DEFAULT NULL,
	`HotelPostCode` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
	`CompetitorId` int(11) DEFAULT NULL,
	`HotelMatchStatus` tinyint(1) DEFAULT NULL,
	`HotelDescription` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
	`isProceesed` tinyint(1) DEFAULT NULL,
	`matchhotelname` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
    `MatchHotelAddress1` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
	`DipBagSyncId` int(11) DEFAULT NULL,
	`IsMailed` tinyint(1) DEFAULT NULL,
	`RequestId` int(11) DEFAULT NULL,
	`ismailed1` tinyint(1) DEFAULT NULL,
	`Active` tinyint(1) DEFAULT '1',
	`CreatedBy` int(11) NOT NULL,
	`CreatedDate` datetime DEFAULT CURRENT_TIMESTAMP,
	`ModifiedBy` int(11) DEFAULT NULL,
	`ModifiedDatetime` datetime DEFAULT NULL,
	`LastAppearnceDate` datetime DEFAULT NULL,
    `Longitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
    `Latitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL
	);
    
    
    
    DROP TEMPORARY TABLE IF EXISTS TempHotelUpdate;
	CREATE TEMPORARY TABLE  TempHotelUpdate(
	`HotelId` bigint(20) NOT NULL ,
	`WebSiteHotelId` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
	`HotelName` varchar(512) CHARACTER SET utf8 NOT NULL,
	`HotelAddress1` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
	`HotelAddress2` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
	`CityId` int(11) NOT NULL,
	`HotelBrandName` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
	`StarRatingId` int(11) DEFAULT NULL,
	`HotelPostCode` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
	`CompetitorId` int(11) DEFAULT NULL,
	`HotelMatchStatus` tinyint(1) DEFAULT NULL,
	`HotelDescription` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
	`isProceesed` tinyint(1) DEFAULT NULL,
	`matchhotelname` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
    `MatchHotelAddress1` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
	`DipBagSyncId` int(11) DEFAULT NULL,
	`IsMailed` tinyint(1) DEFAULT NULL,
	`RequestId` int(11) DEFAULT NULL,
	`ismailed1` tinyint(1) DEFAULT NULL,
	`Active` tinyint(1) DEFAULT '1',
	`CreatedBy` int(11) NOT NULL,
	`CreatedDate` datetime DEFAULT CURRENT_TIMESTAMP,
	`ModifiedBy` int(11) DEFAULT NULL,
	`ModifiedDatetime` datetime DEFAULT NULL,
	`LastAppearnceDate` datetime DEFAULT NULL,
    `Longitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
    `Latitude` varchar(50) CHARACTER SET utf8 DEFAULT NULL
	);
    
    
	
	
	
	
    
    
                
    INSERT INTO MSTHotelHMDataCleansing (
	`HotelId`, `WebSiteHotelId`, `HotelName`, `HotelAddress1`, `HotelAddress2`, `CityId`, `HotelBrandName`, `StarRatingId`,
	`HotelPostCode`, `CompetitorId`, `HotelMatchStatus`, `HotelDescription`, `isProceesed`, `matchhotelname`, `DipBagSyncId`,
	`IsMailed`, `RequestId`, `ismailed1`, `Active`, `CreatedBy`, `CreatedDate`, `ModifiedBy`, `ModifiedDatetime`,
	`LastAppearnceDate` 
	)              
	SELECT `HotelId`, `WebSiteHotelId`, `HotelName`, `HotelAddress1`, `HotelAddress2`, `CityId`, `HotelBrandName`, `StarRatingId`,
	`HotelPostCode`, `CompetitorId`, `HotelMatchStatus`, `HotelDescription`, `isProceesed`, `matchhotelname`, `DipBagSyncId`,
	`IsMailed`, `RequestId`, `ismailed1`, `Active`, `CreatedBy`, `CreatedDate`, `ModifiedBy`, `ModifiedDatetime`,
	`LastAppearnceDate` 
	FROM TempDataCleansing;
	
                                                               
 
	/*=====END: History of duplicate Hotels before delete  =====*/                                                           
	/*=====START: Update Hotel Address based on MAX Length of Address =====*/                                          

	Insert into TempDataCleansing_MaxAddress 
		(MaxHotelAddress,WebSiteHotelId, CityId, CompetitorId)
	SELECT  MAX(CHAR_LENGTH(RTRIM(HotelAddress1))) AS MaxHotelAddress, WebSiteHotelId, CityId, CompetitorId
	FROM TempDataCleansing TH                                                                  
	GROUP BY WebSiteHotelId, CityId, CompetitorId 
	HAVING MAX(CHAR_LENGTH(RTRIM(HotelAddress1))) <> 0;

	 						   
	INSERT INTO TempAddressUpdate (
	`HotelId`, `WebSiteHotelId`, `HotelName`, `HotelAddress1`, `HotelAddress2`, `CityId`, `HotelBrandName`, `StarRatingId`,
	`HotelPostCode`, `CompetitorId`, `HotelMatchStatus`, `MatchHotelAddress1`,  `HotelDescription`, `isProceesed`, `matchhotelname`, `DipBagSyncId`,
	`IsMailed`, `RequestId`, `ismailed1`, `Active`, `CreatedBy`, `CreatedDate`, `ModifiedBy`, `ModifiedDatetime`,
	`LastAppearnceDate`,`Longitude`,`Latitude`
	)              
	SELECT MH.`HotelId`, MH.`WebSiteHotelId`, MH.`HotelName`, MH.`HotelAddress1`, MH.`HotelAddress2`, MH.`CityId`, MH.`HotelBrandName`, MH.`StarRatingId`,
	MH.`HotelPostCode`, MH.`CompetitorId`, MH.`HotelMatchStatus`, MH.`MatchHotelAddress1`, MH.`HotelDescription`, MH.`isProceesed`, MH.`matchhotelname`, MH.`DipBagSyncId`,
	MH.`IsMailed`, MH.`RequestId`, MH.`ismailed1`, MH.`Active`, MH.`CreatedBy`, MH.`CreatedDate`, MH.`ModifiedBy`, MH.`ModifiedDatetime`,
	MH.`LastAppearnceDate` ,MH.`Longitude`, MH.`Latitude`  
    FROM TempDataCleansing MH
	INNER JOIN TempDataCleansing_MaxAddress A
	ON MH.CityId = A.CityId
	AND MH.CompetitorId = A.CompetitorId                                
	AND LTRIM(RTRIM(MH.WebSiteHotelId)) = LTRIM(RTRIM(A.WebSiteHotelId))
	AND CHAR_LENGTH(RTRIM(MH.HotelAddress1)) = A.MaxHotelAddress;
	 
    
    /*Need to work on it Bhushan Gaud Start*/
	/*
	;WITH CTESameAddressLength AS
	(
	SELECT WebSiteHotelId, CityId, CompetitorId, LastAppearnceDate,
		ROW_NUMBER() OVER(PARTITION BY WebSiteHotelId, CityId, CompetitorId ORDER BY LastAppearnceDate DESC) AS RowNo 
	FROM TempAddressUpdate TH                                                              
	)
	DELETE FROM CTESameAddressLength WHERE RowNo > 1;
	*/
	/*Need to work on it Bhushan Gaud End*/
    
	
    Set @rn1 = 1;
	Set @LastAppearnceDate = now();
	Set @WebSiteHotelId = '';
	Set @CityId = 0;
	Set @CompetitorId = 0;   
    
    
    Truncate Table TempDeleteDuplicate;
    
    INsert into TempDeleteDuplicate (HotelId)
    Select B.HotelId From 
    (
		Select 
		@rn1 := 
			if(@WebSiteHotelId = A.WebSiteHotelId
				&& @CityId = A.CityId && @CompetitorId = A.CompetitorId, 
				@rn1 +1
			,  1) As Rank, A.HotelId,
		A.LastAppearnceDate, A.WebSiteHotelId, A.CityId, A.CompetitorId,
			@LastAppearnceDate := A.LastAppearnceDate,
			@WebSiteHotelId := A.WebSiteHotelId,
			@CityId := A.CityId,
			@CompetitorId := A.CompetitorId	
		From (
		SELECT   MH.HotelId, MH.WebSiteHotelId, MH.CityId, MH.CompetitorId, MH.LastAppearnceDate
			FROM TempAddressUpdate MH
			ORDER BY  MH.WebSiteHotelId, MH.CityId, MH.CompetitorId,MH.LastAppearnceDate DESC
		) A
    ) B Where Rank > 1;
    
    DELETE HD 
	FROM Hotels MH 
	INNER JOIN TempAddressUpdate HD                                                 
	ON MH.HotelId = HD.HotelId;
         
	UPDATE Hotels MHotel 
	INNER JOIN TempAddressUpdate IHotel                                                            
	ON MHotel.CityId = IHotel.CityId
		AND MHotel.CompetitorId = IHotel.CompetitorId
		AND MHotel.WebSiteHotelId = IHotel.WebSiteHotelId
	SET MHotel.HotelAddress1 = IHotel.HotelAddress1
	WHERE MHotel.HotelId <> IHotel.HotelId; 
	
    
	/*=====END: Update Hotel Address based on MAX Length of Address  =====*/                                             
		/*=====START: Update Hotel Name based on MAX Last Appearance Date  =====*/                      
	
    
    Insert into TempDataCleansing_MaxLastAppDate 
		(MaxLastAppDate,WebSiteHotelId, CityId, CompetitorId)
	SELECT MAX(LastAppearnceDate) AS MaxLastAppDate, WebSiteHotelId, CityId, CompetitorId
		FROM TempDataCleansing TH                                                                 
		GROUP BY WebSiteHotelId, CityId, CompetitorId;
    
    
    Insert into TempHotelUpdate (
	`HotelId`,`WebSiteHotelId`,`HotelName`,`HotelAddress1`,`HotelAddress2`,`CityId`,
	`HotelBrandName`,`StarRatingId`,`HotelPostCode`,`CompetitorId`,`HotelMatchStatus`,
	`HotelDescription`,`isProceesed`,`matchhotelname`,`MatchHotelAddress1`, `DipBagSyncId`,`IsMailed`,
	`RequestId`,`ismailed1`,`Active`,`CreatedBy`,`CreatedDate`,`ModifiedBy`,
	`ModifiedDatetime`,`LastAppearnceDate`,`Longitude`,`Latitude`)
	SELECT `HotelId`,MH.`WebSiteHotelId`,`HotelName`,`HotelAddress1`,`HotelAddress2`,MH.`CityId`,
	`HotelBrandName`,`StarRatingId`,`HotelPostCode`,MH.`CompetitorId`,`HotelMatchStatus`,
	`HotelDescription`,`isProceesed`,`matchhotelname`,`MatchHotelAddress1`, `DipBagSyncId`,`IsMailed`,
	`RequestId`,`ismailed1`,`Active`,`CreatedBy`,`CreatedDate`,`ModifiedBy`,
	`ModifiedDatetime`,`LastAppearnceDate`,`Longitude`,`Latitude` 
	FROM TempDataCleansing MH
	INNER JOIN TempDataCleansing_MaxLastAppDate A
	ON MH.CityId = A.CityId
	AND MH.CompetitorId = A.CompetitorId
	AND MH.LastAppearnceDate = A.MaxLastAppDate   
	AND LTRIM(RTRIM(MH.WebSiteHotelId)) = LTRIM(RTRIM(A.WebSiteHotelId));  
	
	 	  
	UPDATE Hotels MHotel 
	INNER JOIN TempHotelUpdate IHotel
	ON MHotel.CityId = IHotel.CityId
		AND MHotel.CompetitorId = IHotel.CompetitorId
		AND MHotel.WebSiteHotelId = IHotel.WebSiteHotelId
	SET MHotel.HotelName = IHotel.HotelName,
	MHotel.HotelAddress2 = IHotel.HotelAddress2, 
	MHotel.StarRatingId = IHotel.StarRatingId,
	MHotel.matchhotelname = IHotel.matchhotelname,
	MHotel.MatchHotelAddress1 = IHotel.MatchHotelAddress1,
	MHotel.LastAppearnceDate = IHotel.LastAppearnceDate,
	MHotel.Longitude = IHotel.Longitude,
	MHotel.Latitude = IHotel.Latitude
	WHERE MHotel.HotelId <> IHotel.HotelId; 
	 
	/*=====END: Update Hotel Name based on MAX Last Appearance Date  =====*/          

	/*=====START: Delete Duplicate Records that are un-match =====*/   
	/* 
	SELECT * 
	INTO #TempDeleteDuplicate 
	FROM 
	(
	SELECT MH.HotelId, 
					ROW_NUMBER() OVER(PARTITION BY MH.WebSiteHotelId, MH.CityId, MH.CompetitorId ORDER BY MH.HotelId DESC) AS RowNo 
	FROM TempDataCleansing MH 
					LEFT JOIN HotelMonitor.HotelRelation HR                            
					ON MH.HotelId = HR.intHotelRelationComHotelId      
	WHERE HR.intHotelRelationComHotelId IS NULL                

	)Hotel
	WHERE Hotel.RowNo > 1; 
    */
    
    
    Set @rn1 = 1;
	Set @HotelId = 0;
	Set @WebSiteHotelId = '';
	Set @CityId = 0;
	Set @CompetitorId = 0;   
    
    Truncate Table TempDeleteDuplicate;
    
    INsert into TempDeleteDuplicate (HotelId)
    Select B.HotelId From 
    (
		Select 
		@rn1 := 
			if(@WebSiteHotelId = A.WebSiteHotelId
				&& @CityId = A.CityId && @CompetitorId = A.CompetitorId, 
				If(@HotelId = A.HotelId,@rn1,@rn1 +1)
			,  1) As Rank, 
		A.HotelId, A.WebSiteHotelId, A.CityId, A.CompetitorId,
			@HotelId := A.HotelId,
			@WebSiteHotelId := A.WebSiteHotelId,
			@CityId := A.CityId,
			@CompetitorId := A.CompetitorId	
		From (
		SELECT MH.HotelId, MH.WebSiteHotelId, MH.CityId, MH.CompetitorId
			FROM TempDataCleansing MH 
				LEFT JOIN HotelRelation HR                            
				ON MH.HotelId = HR.HotelRelationComHotelId      
			WHERE HR.HotelRelationComHotelId IS NULL
			ORDER BY MH.WebSiteHotelId, MH.CityId, MH.CompetitorId ASC, MH.HotelId DESC
		) A
    ) B Where Rank > 1;
    
	 Drop Temporary Table If Exists Temp_DeleteHotel;
     Create Temporary Table Temp_DeleteHotel
     As 
     Select MH.HotelId
		FROM Hotels MH 
		INNER JOIN TempDeleteDuplicate HD                                                 
		ON MH.HotelId = HD.HotelId;
	
    DELETE HDG From HotelGroupDetails HDG Where HDG.HotelId in
     (
		Select HotelId From Temp_DeleteHotel
     );
									
	DELETE MH 
	FROM Hotels MH 
	INNER JOIN TempDeleteDuplicate HD                                                 
	ON MH.HotelId = HD.HotelId;

	DELETE FROM TempDataCleansing WHERE HotelId IN( SELECT HotelId FROM TempDeleteDuplicate);
								
     
     Drop Temporary Table If Exists Temp_DeleteHotel;
     Create Temporary Table Temp_DeleteHotel
     As     
     Select TH.HotelId
		FROM Hotels TH
	INNER JOIN 
	(              
	SELECT  WebSiteHotelId, CityId, CompetitorId
	FROM TempDataCleansing TH                                                                  
	GROUP BY WebSiteHotelId, CityId, CompetitorId 
	HAVING COUNT(WebSiteHotelId) > 1
	)Hotel
	ON TH.CityId = Hotel.CityId
	AND TH.CompetitorId = Hotel.CompetitorId
	AND TH.WebSiteHotelId = Hotel.WebSiteHotelId
	LEFT JOIN HotelRelation HR                            
	ON TH.HotelId = HR.HotelRelationComHotelId        
	WHERE HR.HotelRelationComHotelId IS NULL;
     
     DELETE HDG From HotelGroupDetails HDG Where HDG.HotelId in
     (
		Select  HotelId From Temp_DeleteHotel
     );
                                 
	
	-- SELECT * 
	DELETE TH
	FROM Hotels TH
	INNER JOIN 
	(              
	SELECT  WebSiteHotelId, CityId, CompetitorId
	FROM TempDataCleansing TH                                                                  
	GROUP BY WebSiteHotelId, CityId, CompetitorId 
	HAVING COUNT(WebSiteHotelId) > 1
	)Hotel
	ON TH.CityId = Hotel.CityId
	AND TH.CompetitorId = Hotel.CompetitorId
	AND TH.WebSiteHotelId = Hotel.WebSiteHotelId
	LEFT JOIN HotelRelation HR                            
	ON TH.HotelId = HR.HotelRelationComHotelId        
	WHERE HR.HotelRelationComHotelId IS NULL;
	
	/*=====END: Delete Duplicate Records that are un-match =====*/       


		
		-- -Delete Records from probable table because hotels does not exist in msthotel Start
		Delete P
		From ProbableMatchedHotels P Left Join Hotels MH
		On P.HotelId = MH.HotelId
		Where MH.HotelId Is Null;


		Delete P
		From ProbableMatchedHotels P Left Join Hotels MH
		On P.ProbableMatchedHotelComHotelId = MH.HotelId
		Where MH.HotelId Is Null;

		-- -Delete Records from probable table because hotels does not exist in msthotel End


 
    
END ;;
