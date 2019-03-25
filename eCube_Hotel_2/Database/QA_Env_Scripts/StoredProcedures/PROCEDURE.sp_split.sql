DELIMITER ;;

CREATE PROCEDURE `sp_split`(IN str VARCHAR(4000),IN delim varchar(1))
begin
DECLARE delimIdx int default 0;
DECLARE charIdx int default 1;
DECLARE rest_str varchar(4000) default '';
DECLARE store_str varchar(4000) default '';

-- create TEMPORARY table IF NOT EXISTS SplitValue as (select  items from list_field where 1=0);

Drop Temporary Table if exists SplitValue;

Create Temporary Table SplitValue (items varchar(4000));

truncate table SplitValue;
set @rest_str = str;

set  @delimIdx = LOCATE(delim,@rest_str);
set @charIdx = 1;
set @store_str = '';
set @store_str = SUBSTRING(@rest_str,@charIdx,@delimIdx-1);

set @rest_str = SUBSTRING(@rest_str from @delimIdx+1);

if length(trim(@store_str)) = 0   then
    set @store_str = @rest_str;
end if;    


INSERT INTO SplitValue
SELECT (Ltrim(Rtrim(@store_str)));

WHILE @delimIdx <> 0 DO
    set  @delimIdx = LOCATE(delim,@rest_str);
    set @charIdx = 1;
    set @store_str = SUBSTRING(@rest_str,@charIdx,@delimIdx-1);
    set @rest_str = SUBSTRING(@rest_str from @delimIdx+1);

 
    if length(trim(@store_str)) = 0   then
        set @store_str = @rest_str;
    end if;    
    INSERT INTO SplitValue(items)
    SELECT (Ltrim(Rtrim(@store_str))); 
END WHILE;

 -- select items from SplitValue;
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_TruncateMatchingRecords` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
