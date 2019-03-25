DELIMITER ;;

CREATE FUNCTION `SPLIT_STR`(
  str VARCHAR(4000),
  delim VARCHAR(12),
  pos INT
) RETURNS varchar(4000) CHARSET latin1
    DETERMINISTIC
BEGIN 
    RETURN REPLACE(SUBSTRING(SUBSTRING_INDEX(str, delim, pos),
       LENGTH(SUBSTRING_INDEX(str, delim, pos -1)) + 1),
       delim, '');
END ;;
