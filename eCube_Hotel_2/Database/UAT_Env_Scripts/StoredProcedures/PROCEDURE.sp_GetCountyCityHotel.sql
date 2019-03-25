DELIMITER ;;

CREATE PROCEDURE `sp_GetCountyCityHotel`(
                p_CityId INT 
                ,p_SupplierId INT /* = 0 */
                ,p_DipBagDynamicId Int/* =0 */
)
BEGIN

 
	IF p_CityId = 0 AND p_SupplierId = 0  -- Primary Supplier details
	THEN
	if(p_DipBagDynamicId <= 0 )
	Then
		-- update Hotels Set  matchhotelname = fn_HotelKeyWordReplaceWeeklyMatching_Ematch(HotelName, CityId) 			Where CompetitorId = 1;
     
		SELECT DISTINCT PS.HotelId AS PrimaryHotelId ,
			0   As SecondaryHotelId,
			fn_HotelKeyWordReplaceWeeklyMatching_Ematch(PS.HotelName,PS.CityId) AS PrimaryHotelName,
			''   As SecondaryHotelName,
			PS.CityId AS PrimaryCityId,                                                                          
			PS.HotelAddress1 as PrimaryHotelAddress,
			Case   
			 When char_length(rtrim(ltrim(rtrim(PS.HotelAddress2)))) = 0 Then 'x'   
			 Else IFNULL(PS.HotelAddress2, 'x')   
			 End as PrimaryZoneInfo,                                                                             
			0   As Weightage,
			CITY.CityName,
			Cntry.CountryName,
			PS.Latitude AS PrimaryLatitude, 
			PS.Longitude AS PrimaryLongitude,
			'' AS SecondaryLatitude,
			'' AS SecondaryLongitude,
			'' as SecondaryZoneInfo,
			'' as SecondaryHotelAddress,
			0 as MatchingRunId,0 as MatchedInStepNo,0 MatchingScore,'' as MatchType
			, 0 decHotelNamePer, 0 decHotelAddressPer, 0 decGeoCoordinatesPer 
						
		FROM vw_primarysupplierhotels PS
		INNER JOIN Cities CITY 
		ON PS.CityId = CITY.CityId
		INNER JOIN tbl_CountryMaster Cntry  
		ON Cntry.CountryId = CITY.CountryId

		--  where 1=1 and CITY.CityId IN (161,162,163) 

		ORDER BY PrimaryCityId , PrimaryHotelName;
	Else
		/*
		SELECT DISTINCT              PS.HotelId AS PrimaryHotelId ,
						0   As SecondaryHotelId,
						HotelMonitor.fn_HotelKeyWordReplaceWeeklyMatching_Ematch(PS.nvcrHotelName,PS.CityId) AS PrimaryHotelName,
						-- PS.nvcrHotelName AS PrimaryHotelName,
						''   As SecondaryHotelName,
						PS.CityId AS PrimaryCityId,
						PS.HotelAddress1 as PrimaryHotelAddress,
						Case   
						 When char_length(rtrim(ltrim(rtrim(PS.HotelAddress2)))) = 0 Then 'x'   
						 Else IFNULL(PS.HotelAddress2, 'x')   
						 End as PrimaryZoneInfo,                                                                                                             
						0   As Weightage,
						x.nvcrCityName,
						Cntry.CountryName,
						-- Start: Added by Kiran Kadam - Geo Coordinates Matching on 25-Jul-2016 
						PS.nvcrLatitude AS PrimaryLatitude, 
						PS.nvcrLongitude AS PrimaryLongitude,
						'' AS SecondaryLatitude,
						'' AS SecondaryLongitude,
						'' as SecondaryZoneInfo,
						'' as SecondaryHotelAddress,
						0 as MatchingRunId,0 as MatchedInStepNo,0 MatchingScore,'' as MatchType
						, 0 decHotelNamePer, 0 decHotelAddressPer, 0 decGeoCoordinatesPer 
						-- End: Added by Kiran Kadam - Geo Coordinates Matching on 25-Jul-2016
		FROM HotelMonitor.vw_PrimarySupplierHotels PS
		Inner Join
		(              
						Select distinct city.CityId, city.nvcrCityName,city.intCountryId
										-- , bc.nvcrHotelName --Addded by Bhushan Gaud for New Matching Algorithm consider only batchCRawlData Hotel 
						from Cities CITY WITH;(NOLOCK) 
						Inner join HotelMonitor.BatchCrawlData bc WITH(NOLOCK)
										ON LTRIM(RTRIM(CITY.nvcrCityName)) = LTRIM(RTRIM(bc.nvcrCity))
						where bc.intDiPBagDynamicId =p_DipBagDynamicId
		)x
		ON PS.CityId = x.CityId
		INNER JOIN tbl_CountryMaster Cntry WITH(NOLOCK) 
		ON Cntry.intCountryId = x.intCountryId
		WHERE PS.HotelId not in   
		(select HotelId as HotelId from hotelMOnitor.HotelRelation with (nolock))                                           
		AND PS.HotelId not in   
		(select HotelId as HotelId from eMatch.ProbableMatchedHotels with (nolock))
		-- where nvcrHotelName like '%adrar%'
		-- And PS.nvcrHotelName = X.nvcrHotelName --Addded by Bhushan Gaud for New Matching Algorithm consider only batchCRawlData Hotel
		-- WHERE PS.nvcrHotelName IN('Fairmont Bab Al Bahr Abu Dhabi','Grand Millennium Al Wahda')--IN('Al Manzel Hotel Apartments','Al Seef Resort & SPA By Andalus')               
		ORDER BY PrimaryCityId , PrimaryHotelName
		*/ 
		Select 0 ID ;
	End if;
	ELSE                       -- Secondary Supplier details
	if(p_DipBagDynamicId <= 0 )
	THEN
    update Hotels Set  matchhotelname = fn_HotelKeyWordReplaceWeeklyMatching_Ematch(HotelName,CityId)
		WHERE CityId = p_CityId AND CompetitorId = p_SupplierId;
    
	SELECT Distinct SS.HotelId,
	fn_HotelKeyWordReplaceWeeklyMatching_Ematch(SS.HotelName,SS.CityId) AS HotelName,
	SS.HotelName_Original,
	SS.HotelAddress1,
	SS.HotelAddress2,
	SS.HotelPostCode,
	SS.CityId,
	SS.HotelBrandName,
	SS.CreatedBy,
	SS.isProceesed,
	SS.WebSiteHotelId,
	SS.CompetitorId,
	SS.Latitude,
	SS.Longitude,
	CITY.CityName,
	-- -Commented by Bhushan Gaud on 10-Oct-2017 CR received from Ops team (Prachi/Pallavi) Start
	IFNULL(HR.HotelId,0) AS ManualUnmatchPrimaryHotelId,
	-- 0 AS intManualUnmatchPrimaryHotelId,
	-- -Commented by Bhushan Gaud on 10-Oct-2017 CR received from Ops team (Prachi/Pallavi) Start
	Case   
					 When char_length(rtrim(ltrim(rtrim(SS.HotelAddress2)))) = 0 Then 'x'   
					 Else IFNULL(SS.HotelAddress2, 'x')   
					 End as ZoneInfo                                              
	FROM vw_secondarysupplier SS 
	INNER JOIN Cities CITY  
	ON SS.CityId = CITY.CityId
	LEFT OUTER JOIN HotelRelation HR  
	ON SS.HotelId = HR.HotelRelationComHotelId 
	WHERE SS.CityId = p_CityId AND SS.CompetitorId = p_SupplierId

	ORDER BY SS.CityId, HotelName;
	Else
	/*
	SELECT Distinct  SS.HotelId,
	HotelMonitor.fn_HotelKeyWordReplaceWeeklyMatching_Ematch(SS.nvcrHotelName,SS.CityId) AS nvcrHotelName,
	SS.nvcrHotelName_Original,
	SS.HotelAddress1,
	SS.HotelAddress2,
	SS.nvcrHotelPostCode,
	SS.CityId,
	SS.nvcrHotelBrandName,
	SS.intUsrId,
	SS.bitisProceesed,
	SS.nvcrWebSiteHotelId,
	SS.intSupplierId,
	SS.nvcrLatitude,
	SS.nvcrLongitude,
	x.nvcrCityName,IFNULL(HR.HotelId,0) AS intManualUnmatchPrimaryHotelId,
	Case   
					 When char_length(rtrim(ltrim(rtrim(SS.HotelAddress2)))) = 0 Then 'x'   
					 Else IFNULL(SS.HotelAddress2, 'x')   
					 End as ZoneInfo                                              
	FROM HotelMonitor.vw_SecondarySupplier SS
	INNER JOIN 
	(              
					Select distinct city.CityId, city.nvcrCityName 
					, bc.nvcrHotelName -- Addded by Bhushan Gaud for New Matching Algorithm consider only batchCRawlData Hotel
					from Cities CITY WITH;(NOLOCK) 
					Inner join HotelMonitor.BatchCrawlData bc WITH(NOLOCK)
									ON LTRIM(RTRIM(CITY.nvcrCityName)) = LTRIM(RTRIM(bc.nvcrCity))
					where bc.intDiPBagDynamicId =p_DipBagDynamicId
	)x
	ON SS.CityId = x.CityId
	And SS.nvcrHotelName_Original = x.nvcrHotelName -- Addded by Bhushan Gaud for New Matching Algorithm consider only batchCRawlData Hotel
	LEFT OUTER JOIN HotelMonitor.HotelRelation HR WITH(NOLOCK) 
	ON SS.HotelId = HR.intHotelRelationComHotelId AND bitIsManualUnmatch = 1 
	-- LEFT OUTER JOIN eMatch.probablematchedhotels pm WITH(NOLOCK)
	-- ON SS.HotelId = pm.intProbableMatchedHotelComHotelId
	WHERE SS.CityId = p_CityId AND SS.intSupplierId =p_SupplierId-- and SS.nvcrHotelName like '%adrar%'
	-- AND SS.nvcrHotelName_Original IN('Fairmont Bab Al Bahr','Grand Millennium Al Wahda Abu Dhabi') --IN('Al Manzel Hotel Apartments','Al Seef Resort & SPA By Andalus')
	ORDER BY SS.CityId, nvcrHotelName
	*/
	Select 0 ID;
	End if;
	END IF;
End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_GetDetailsToSendMatchingMail` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
