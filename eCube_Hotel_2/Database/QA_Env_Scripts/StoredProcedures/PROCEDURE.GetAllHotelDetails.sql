DELIMITER ;;

CREATE PROCEDURE `GetAllHotelDetails`()
Begin
		
        drop table if exists All_Hotel_details_temp;
		create table All_Hotel_details_temp
        as 
  		SELECT distinct `HotelId`
      ,`WebSiteHotelId`
      ,`HotelName`
      ,`HotelAddress1`
      ,`HotelAddress2`
      ,HM.`CityId`
      ,`HotelBrandName`
      ,`StarRatingId`
      ,`HotelPostCode`
      ,HM.`CompetitorId`
      ,`HotelMatchStatus`
      ,`HotelDescription`
      ,HM.`CreatedBy`     -- old intuserid 
      ,`isProceesed`
      ,HM.`CreatedDate`
      ,`matchhotelname`
      ,HM.`DipBagSyncId`
      ,`IsMailed`
      ,`RequestId`
									-- ,`Unq_HotelID` removed as per bushan
      ,`MatchHotelAddress1`
      ,`isConsiderForMatching`
      ,HM.`HotelStatusId`
      ,`LastAppearnceDate`
      ,`LastRequestRunId`
      ,`Longitude`
      ,`Latitude`
      ,`YieldManager`
      ,`ContractManager`
      ,`DemandGroup`
      ,`CrawledHotelAddress`
	  ,C.CityName
	  ,C.CityCode
	  ,CT.CountryName
	  ,S.name
	  ,SM.HotelStatus 
	  ,US.UserName
	  ,HM.ZoneName -- Added By Sumeet Helchal on 14th dec2017
  FROM Hotels HM
  INNER JOIN Cities C ON HM.CityId =C.CityId
  INNER JOIN tbl_CountryMaster CT ON CT.CountryId=C.CountryId
  INNER JOIN tbl_Competitor S ON HM.CompetitorId=S.Id
  INNER JOIN tbl_UserMaster US ON US.UserId=HM.CreatedBy
  LEFT JOIN HotelStatus SM ON SM.HotelStatusId=HM.HotelStatusId ;

End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GetAll_Supplier` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
