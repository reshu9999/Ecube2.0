DELIMITER ;;

CREATE PROCEDURE `sp_GetSecondarySupplierHotelsCitywise`(      
       p_CityID int,
       p_SupplierID int   
)
BEGIN        


       
                                 SELECT MH.HotelId, IFNULL(MH.WebSiteHotelId,'-') WebSiteHotelId, MH.CityId ,MH.HotelName, 
									IFNULL(HotelAddress1,'-') AS HotelAddress1 , Sup.Id, Sup.name
                                , Case When MH.LastAppearnceDate is Null Then '-' Else MH.LastAppearnceDate End LastAppearnceDate
                                ,IFNULL(MH.Longitude,'-') Longitude,IFNULL(MH.Latitude,'-') Latitude
                                From Hotels MH  INNER JOIN tbl_Competitor Sup  
                                 ON MH.CompetitorId = Sup.Id
                                
                                 Where MH.CityId = p_CityID  
                                 AND Sup.Id = p_SupplierID and Sup.Id <>1 ;   
                                  
End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_GetSupplierID` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
