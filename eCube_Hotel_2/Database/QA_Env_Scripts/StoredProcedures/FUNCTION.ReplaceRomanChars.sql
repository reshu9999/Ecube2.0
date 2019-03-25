DELIMITER ;;

CREATE FUNCTION `ReplaceRomanChars`(p_str NVARCHAR(500)) RETURNS varchar(500) CHARSET utf8
BEGIN        
DECLARE v_intLastIndex INT;  
      
SET v_intLastIndex=CHAR_LENGTH(RTRIM(p_str));        
-- ----------------------------------------Array1------------------------        
SET p_str=REPLACE(p_str,'-IX','-9');        
SET p_str=REPLACE(p_str,'-X','-10');        
SET p_str=REPLACE(p_str,'-VIII','-8');        
SET p_str=REPLACE(p_str,'-VII','-7');        
SET p_str=REPLACE(p_str,'-VI','-6');        
SET p_str=REPLACE(p_str,'-IV','-4');        
SET p_str=REPLACE(p_str,'-V','-5');        
SET p_str=REPLACE(p_str,'-III','-3');        
SET p_str=REPLACE(p_str,'-II','-2');        
SET p_str=REPLACE(p_str,'-I','-1');        
        
SET p_str=REPLACE(p_str,'IX-','9-');        
SET p_str=REPLACE(p_str,'X-','10-');        
SET p_str=REPLACE(p_str,'VIII-','8-');        
SET p_str=REPLACE(p_str,'VII-','7-');        
SET p_str=REPLACE(p_str,'VI-','6-');        
SET p_str=REPLACE(p_str,'IV-','4-');        
SET p_str=REPLACE(p_str,'V-','5-');        
SET p_str=REPLACE(p_str,'III-','3-');        
SET p_str=REPLACE(p_str,'II-','2-');        
SET p_str=REPLACE(p_str,'I-','1-');        
        
SET p_str=REPLACE(p_str,' IX ',' 9 ');     
SET p_str=REPLACE(p_str,' X ',' 10 ');        
SET p_str=REPLACE(p_str,' VIII ',' 8 ');        
SET p_str=REPLACE(p_str,' VII ',' 7 ');        
SET p_str=REPLACE(p_str,' VI ',' 6 ');        
SET p_str=REPLACE(p_str,' IV ',' 4 ');        
SET p_str=REPLACE(p_str,' V ',' 5 ');        
SET p_str=REPLACE(p_str,' III ',' 3 ');        
SET p_str=REPLACE(p_str,' II ',' 2 ');        
SET p_str=REPLACE(p_str,' I ',' 1 ');        
       
-- ----------------------------------------Array2------------------------        
SET p_str=CASE WHEN CHAR_LENGTH(RTRIM(p_str))-2=locate(' IX',p_str)  AND CHAR_LENGTH(RTRIM(p_str))-2 > 0 THEN INSERT(p_str, CHAR_LENGTH(RTRIM(p_str))-1,CHAR_LENGTH(RTRIM(p_str)), ' 9') ELSE p_str END;        
SET p_str=CASE WHEN CHAR_LENGTH(RTRIM(p_str))-1=locate(' X',p_str)   AND CHAR_LENGTH(RTRIM(p_str))-1 > 0 THEN INSERT(p_str, CHAR_LENGTH(RTRIM(p_str))-1,CHAR_LENGTH(RTRIM(p_str)), ' 10') ELSE p_str END;        
SET p_str=CASE WHEN CHAR_LENGTH(RTRIM(p_str))-4=locate(' VIII',p_str)AND CHAR_LENGTH(RTRIM(p_str))-4 > 0 THEN INSERT(p_str, CHAR_LENGTH(RTRIM(p_str))-3,CHAR_LENGTH(RTRIM(p_str)), ' 8') ELSE p_str END;        
SET p_str=CASE WHEN CHAR_LENGTH(RTRIM(p_str))-3=locate(' VII',p_str) AND CHAR_LENGTH(RTRIM(p_str))-3 > 0 THEN INSERT(p_str, CHAR_LENGTH(RTRIM(p_str))-3,CHAR_LENGTH(RTRIM(p_str)), ' 7') ELSE p_str END;        
SET p_str=CASE WHEN CHAR_LENGTH(RTRIM(p_str))-2=locate(' VI',p_str)  AND CHAR_LENGTH(RTRIM(p_str))-2 > 0 THEN INSERT(p_str, CHAR_LENGTH(RTRIM(p_str))-1,CHAR_LENGTH(RTRIM(p_str)), ' 6') ELSE p_str END;        
SET p_str=CASE WHEN CHAR_LENGTH(RTRIM(p_str))-2=locate(' IV',p_str)  AND CHAR_LENGTH(RTRIM(p_str))-2 > 0 THEN INSERT(p_str, CHAR_LENGTH(RTRIM(p_str))-1,CHAR_LENGTH(RTRIM(p_str)), ' 4') ELSE p_str END;        
SET p_str=CASE WHEN CHAR_LENGTH(RTRIM(p_str))-1=locate(' V',p_str)   AND CHAR_LENGTH(RTRIM(p_str))-1 > 0 THEN INSERT(p_str, CHAR_LENGTH(RTRIM(p_str))-1,CHAR_LENGTH(RTRIM(p_str)), ' 5') ELSE p_str END;        
SET p_str=CASE WHEN CHAR_LENGTH(RTRIM(p_str))-3=locate(' III',p_str) AND CHAR_LENGTH(RTRIM(p_str))-3 > 0 THEN INSERT(p_str, CHAR_LENGTH(RTRIM(p_str))-3,CHAR_LENGTH(RTRIM(p_str)), ' 3') ELSE p_str END;        
SET p_str=CASE WHEN CHAR_LENGTH(RTRIM(p_str))-2=locate(' II',p_str)  AND CHAR_LENGTH(RTRIM(p_str))-2 > 0 THEN INSERT(p_str, CHAR_LENGTH(RTRIM(p_str))-1,CHAR_LENGTH(RTRIM(p_str)), ' 2') ELSE p_str END;        
SET p_str=CASE WHEN CHAR_LENGTH(RTRIM(p_str))-1=locate(' I',p_str)   AND CHAR_LENGTH(RTRIM(p_str))-1 > 0 THEN INSERT(p_str, CHAR_LENGTH(RTRIM(p_str))-1,CHAR_LENGTH(RTRIM(p_str)), ' 1')ELSE p_str END;        
        
     
         
-- ----------------------------------------Array3------------------------        
-- SET @str=CASE WHEN 1=CHARINDEX('I ',@str) THEN REPLACE(@str,'I ','1 ') ELSE @str END        
SET p_str=CASE WHEN 1=locate('IX ',p_str) THEN INSERT(p_str, 1, 2, '9 ') ELSE p_str END;        
SET p_str=CASE WHEN 1=locate('X ',p_str) THEN INSERT(p_str, 1, 1, '10 ') ELSE p_str END;        
SET p_str=CASE WHEN 1=locate('VIII ',p_str) THEN INSERT(p_str, 1, 4, '8 ') ELSE p_str END;        
SET p_str=CASE WHEN 1=locate('VII ',p_str) THEN INSERT(p_str, 1, 3, '7 ') ELSE p_str END;        
SET p_str=CASE WHEN 1=locate('VI ',p_str) THEN INSERT(p_str, 1, 2, '6 ') ELSE p_str END;        
SET p_str=CASE WHEN 1=locate('IV ',p_str) THEN INSERT(p_str, 1, 2, '4 ') ELSE p_str END;        
SET p_str=CASE WHEN 1=locate('V ',p_str) THEN INSERT(p_str, 1, 1, '5 ') ELSE p_str END;        
SET p_str=CASE WHEN 1=locate('III ',p_str) THEN INSERT(p_str, 1, 3, '3 ') ELSE p_str END;        
SET p_str=CASE WHEN 1=locate('II ',p_str) THEN INSERT(p_str, 1, 2, '2 ') ELSE p_str END;        
SET p_str=CASE WHEN 1=locate('I ',p_str) THEN INSERT(p_str, 1, 1, '1 ') ELSE p_str END;        
      
RETURN p_str;        
END ;;
