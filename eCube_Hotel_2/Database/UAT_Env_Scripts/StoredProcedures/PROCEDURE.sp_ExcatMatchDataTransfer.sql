DELIMITER ;;

CREATE PROCEDURE `sp_ExcatMatchDataTransfer`()
Begin

	Declare v_IntEmatchTransferID Int Default 0;
	Declare v_intFetchingID Longtext Default '';
	Declare v_nvcrMatchType Longtext Default '';


	Select  IntEmatchTransferID Into v_IntEmatchTransferID  From EmatchTransfer E  Where intFlag = 0
	Order by E.IntEmatchTransferID limit 1;

	Update EmatchTransfer Set intFlag = 2 WHere  IntEmatchTransferID  = v_IntEmatchTransferID;


	 Select  Group_concat(intFetchingID) Into v_intFetchingID  From MatchingDetails Where IntEmatchTransferID = v_IntEmatchTransferID;

	
	Truncate Table `Temp_ExcatMatch`;
/*
	INSERT INTO Temp_ExcatMatch
			   (`intHotelRelationId`
			   ,`Secondary Supplier Company`
			   ,`Secondary Supplier Hotel ID`
			   ,`Secondary Website Hotel ID`
			   ,`Secondary Supplier Hotel Name `
			   ,`Secondary Supplier Hotel Address`
			   ,`Secondary Supplier Hotel Star`-- Added By Sumeet Helchal on 14th Dec 2017 
			   ,`Longitude`
			   ,`Latitude`
			   ,`Primary Supplier Hotel ID`
			   ,`Primary Supplier Hotel Code`
			   ,`Primary Supplier Hotel Name`
			   ,`Hotel Status`
			   ,`Primary Supplier Hotel Address`-- Added By Sumeet Helchal on 16th Oct 2017 
			   ,`Primary Supplier Hotel Star`-- Added By Sumeet Helchal on 14th Dec 2017 	
			   ,`Primary Hotel Longitude`-- Added By Sumeet Helchal on 16th Oct 2017 	
			   ,`Primary Hotel Latitude`-- Added By Sumeet Helchal on 16th Oct 2017 
			   ,`Destination Code`
			   ,`City`
			   ,`Country`
			   ,`Matching Type`
			   ,`Added on`
			   ,`Matched on`
			   ,`Last Appearance`
			   ,nvcrZoneName-- Added By Sumeet Helchal on 14th Dec 2017
			   )
	*/
				CALL `sp_HBService_HotelMatch_MatchUnmatchHotels_ForClientAccess` (v_intFetchingID);


End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_ExcelUploadHotelMaster_29MAY18` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
