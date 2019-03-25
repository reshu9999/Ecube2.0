DELIMITER ;;

CREATE PROCEDURE `OfflineMatching_GetPrimarySuppliersHotel`(  
p_intUserId int,  
p_intCityId NVARCHAR(500))
Begin  
declare v_intAdmin int;   


      -- below sp not req as per bhushan
   -- call usermanagement.usp_DipBagHM_Common_GetUserAdminId( v_intUserId, v_intAdmin);  
  
				select distinct  
				s.name AS 'SupplierName',  
				H.intHotelId 'PrimaryHotelId',
				HotelName as 'PrimaryHotelName',  
				hs.vcrStatus AS 'HotelStatus', 
				WebSiteHotelId as 'PrimaryHotelCode', 
				H.nvcrLongitude as 'Longitude',
				H.nvcrLatitude as 'Latitude', 
				CONCITY.CityName AS 'City', 
				CONCITY.CityCode AS 'DestinationCode', 
				CONCITY.CountryName AS 'Country',
				HotelAddress1 as 'PrimaryHotelAddress',   
				DATE_FORMAT(H.LastAppearnceDate,'%d/%m/%Y')  AS LastAppearance
				from Hotels H
				INNER JOIN tbl_Competitor s 
				ON H.intSupplierId = s.Id  
				INNER JOIN `vw_DipBagHM_GetCityCountry` CONCITY 
				ON H.CityId = CONCITY.CityId  
				LEFT JOIN HotelStatus hs ON H.HotelStatusId =hs.HotelStatusId  
				 where H.CompetitorId =1
                 and H.CityId=p_intCityId   
                 -- IN (SELECT Items FROM [dbo].[Split](p_intCityId,','))
                order by CityName ;  
                 /* below code omment as per bhushan 
                 (  
					SELECT intSupplierId   
					from Usermanagement.MstUser with (nolock)   
					where intUsrId = v_intAdmin)  
					
                   */ 
				
				End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `OfflineMatching_MatchUnmatchHotel_Supplier` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
