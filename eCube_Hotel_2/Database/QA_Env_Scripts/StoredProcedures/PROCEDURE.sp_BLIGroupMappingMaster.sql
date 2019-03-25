DELIMITER ;;

CREATE PROCEDURE `sp_BLIGroupMappingMaster`(
		IN prmBLIName varchar(500),
		IN prmBLIGroupName varchar(500)
)
BEGIN

		Select count(*) into @blicount from tbl_BliMaster where BliName=prmBLIName;


        select count(*) into @bligrpcount from tbl_Bli_GroupMaster where BLIGroupName=prmBLIGroupName;

        IF @bligrpcount= 0 then
        INSERT INTO tbl_Bli_GroupMaster (BLIGroupName)
		values (prmBLIGroupName);
        end if;

        select Id into @bligrpid from tbl_Bli_GroupMaster
        where BLIGroupName=prmBLIGroupName;

		if @blicount= 0 then
        Insert into tbl_BliMaster (BLIName,Active,CreatedDate,ModifiedDate,BLI_GRP_Id)
        values (prmBLIName,1,now(),now(),@bligrpid);
        END IF;
        end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_ClearDuplicate_Hotel` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
