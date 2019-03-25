DELIMITER ;;

CREATE PROCEDURE `sp_GetSupplierListFromBCD`(
	p_RequestID Int
)
Begin

	Select  RequestRunId into @RequestRunId 
		From tbl_RequestRunDetail Where FK_RequestId = p_RequestID order by 1 desc Limit 1;
        
	Select Group_Concat(intSupplierId) into @vcrSupplierID From BatchCrawlData Where intDiPBagDynamicId = @RequestRunId;
    
    Select Id, `name` From tbl_Competitor Limit 5;
    -- Where Id in (@vcrSupplierID);


End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_GetSuppliers_LCBT` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
