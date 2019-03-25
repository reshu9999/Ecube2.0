DELIMITER ;;

CREATE PROCEDURE `sp_GetLatestAdhocLeadTimeTemplate`()
Begin  
 
SELECT  
    `tempLeadtimeAdhoc_Excel`.`Booking date`,
    `tempLeadtimeAdhoc_Excel`.`Batch Name`,
    `tempLeadtimeAdhoc_Excel`.`Destination`,
    `tempLeadtimeAdhoc_Excel`.`Lead time Value`,
    `tempLeadtimeAdhoc_Excel`.`Event Type Value`,
    `tempLeadtimeAdhoc_Excel`.`Nights`,
    `tempLeadtimeAdhoc_Excel`.`Account Name`,
    `tempLeadtimeAdhoc_Excel`.`Primary`
FROM `eCube_Centralized_DB`.`tempLeadtimeAdhoc_Excel`;

 
End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_GetLatestLeadTimeTemplate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
