DELIMITER ;;

CREATE PROCEDURE `sp_WeeklyMatchDataTransfer`()
Begin


	Declare v_IntWeeklyMatchTransferID Int Default 0;
	Declare v_intFetchingID Longtext Default '';
	Declare v_nvcrMatchType Longtext Default '';
    

	Select  IntWeeklyMatchTransferID, nvcrMatchType Into v_IntWeeklyMatchTransferID, v_nvcrMatchType  
		From  WeeklyMatchTransfer E Where intFlag = 0
	Order by E.IntWeeklyMatchTransferID limit 1;
 
    -- select v_IntWeeklyMatchTransferID;
	
  
    
    Update  WeeklyMatchTransfer Set intFlag = 2 WHere  IntWeeklyMatchTransferID  = v_IntWeeklyMatchTransferID;


	If (v_nvcrMatchType = 'E')  
		Then
			Truncate Table `Temp_ExcatMatch`;
      /*      
			INSERT INTO  Temp_ExcatMatch
					   (`intHotelRelationId`
					   ,`Secondary Supplier Company`
					   ,`Secondary Supplier Hotel ID`
					   ,`Secondary Website Hotel ID`
					   ,`Secondary Supplier Hotel Name `
					   ,`Secondary Supplier Hotel Address`
					   ,`Secondary Supplier Hotel Star` -- Added By Sumeet Helchal on 14th Dec 2017 
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
					   ,`Primary Hotel Last Appearance`-- Added By Sumeet Helchal on 16th Oct 2017 
					   ,nvcrZoneName -- Added By Sumeet Helchal on 14th Dec 2017 	
					   );
	*/
    
   
			CALL `sp_WeeklyExcatMatchHotels__ForClientAccess` (v_intFetchingID);
		
				Elseif (v_nvcrMatchType = 'P')  
				Then

				Truncate Table `Temp_ProbableMatch`;
            
      /*     
					INSERT INTO  Temp_ProbableMatch
					   (`intProbableMatchedHotelId`
						  ,`Secondary Supplier Company`
						  ,`Secondary Supplier Hotel ID`
						  ,`Secondary Website Hotel ID`
						  ,`Secondary Supplier Hotel Name`
						  ,`Secondary Supplier Hotel Address`
						  ,`Secondary supplier Hotel Star`-- Added By Sumeet helchal on 14th Nov 2017
						  ,`Longitude`
						  ,`Latitude`
						  ,`Primary Supplier Hotel ID`
						  ,`Primary Supplier Hotel Code`
						  ,`Primary Supplier Hotel Name`
						  ,`Primary Supplier Hotel Address`
						  ,`Primary supplier Hotel Star`-- Added By Sumeet helchal on 14th Nov 2017
						  ,`Primary Supplier Longitude`
						  ,`Primary Supplier Latitude`
						  ,`Primary Hotel Last Appearance`-- Added By Sumeet Helchal on 14th Dec 2017 
						  ,`Hotel Status`
						  ,`City`
						  ,`Destination Code`
						  ,`Country`
						  ,`Matching Type`
						  ,`Added on`
						  ,`Matched on`
						  ,`Last Appearance`
						  ,`Matching Score (%)`
						  ,`Primary Matched Exist`
						  ,`Secondary Match Exist`
						  ,`nvcrZoneName` -- Added By Sumeet Helchal on 14th Dec 2017
						  )
	*/

				CALL `sp_WeeklyProbableMatchHotels__ForClientAccess` (v_intFetchingID);


				End if;


			Select v_nvcrMatchType nvcrMatchType;
  
End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_WeeklyProbableMatchHotels__ForClientAccess` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
