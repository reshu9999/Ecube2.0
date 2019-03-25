DELIMITER ;;

CREATE FUNCTION `ReplaceSpanishChars`(p_str NVARCHAR(500)) RETURNS varchar(500) CHARSET utf8
BEGIN   

/*	DECLARE v_intCnt INT;    
	DECLARE v_intMaxCnt INT;    
	DECLARE v_NewStr nvarchar(100);    
	DECLARE v_NewChar CHAR;    
	DECLARE v_chr CHAR;    
	DECLARE v_startIndex INT;    
	DECLARE v_UnicodeVal INT;    
		
	SET v_startIndex=1;    
	SET v_NewStr='';    
	SET v_intCnt=1;    
  */
	set p_str = LTRIM(RTRIM(p_str)) ; 
	-- SET v_intMaxCnt=LENGTH(p_str);    

	-- ACCENTS - Make sure the sequence of withaccents and withoutaccents must be same
    SET @withaccents    = 'Ã€ÃÃ‚ÃƒÃ„Ã…Ã Ã¡Ã¢Ã£Ã¤Ã¥ÃˆÃ‰ÃŠÃ‹Ã¨Ã©ÃªÃ«ÃŒÃÃŽÃÃ¬Ã­Ã®Ã¯Ã‘Ã±Ã’Ã“Ã”Ã•Ã–Ã²Ã³Ã´ÃµÃ¶Ã™ÃšÃ›ÃœÃ¹ÃºÃ»Ã¼ÃÃ½Ã¿Ã§ÂºÃŸ';
    SET @withoutaccents = 'AAAAAAaaaaaaEEEEeeeeIIIIiiiiNnOOOOOoooooUUUUuuuuYyycab';
    SET @count = LENGTH(@withaccents);

    WHILE @count > 0 DO
        SET p_str = REPLACE(p_str, SUBSTRING(@withaccents, @count, 1), SUBSTRING(@withoutaccents, @count, 1));
        SET @count = @count - 1;
    END WHILE;
	/*WHILE(v_intCnt<=v_intMaxCnt) Do     
		SET v_chr= SUBSTRING(p_str,v_intCnt,1);
		SET v_pos= FIND_IN_SET(v_chr,'0,1,2,3,4,5,6,7,8,9,.');

		if v_pos > 0 then
			SET p_str=replace(p_str,v_char);
		end if;
		
		set v_intCnt = v_intCnt + 1;
	End while;
    */
/*
   
WHILE(v_intCnt<=v_intMaxCnt) Do     
    
 SET v_chr=SUBSTRING(p_str,v_startIndex,v_intCnt);    
 SET v_UnicodeVal = UNICODE(v_chr);
   
  
 -- Replacing 'Ã€'    
 IF(v_UnicodeVal=192) THEN   SET v_NewChar=NCHAR(65);    
 -- Replacing 'Ã'    
 ELSEIF (v_UnicodeVal=193) THEN   SET v_NewChar=NCHAR(65);    
 -- Replacing 'Ã‚'    
 ELSEIF (v_UnicodeVal=194) THEN   SET v_NewChar=NCHAR(65);    
 -- Replacing 'Ãƒ'    
 ELSEIF (v_UnicodeVal=195) THEN   SET v_NewChar=NCHAR(65);    
 -- Replacing 'Ã„'    
 ELSEIF (v_UnicodeVal=196) THEN   SET v_NewChar=NCHAR(65);    
 -- Replacing 'Ã…'    
 ELSEIF (v_UnicodeVal=197) THEN   SET v_NewChar=NCHAR(65);    
 -- Replacing 'Ã '    
 ELSEIF (v_UnicodeVal=224) THEN SET v_NewChar=NCHAR(97);    
 -- Replacing 'Ã¡'    
 ELSEIF (v_UnicodeVal=225) THEN SET v_NewChar=NCHAR(97);    
 -- Replacing 'Ã¢'    
 ELSEIF (v_UnicodeVal=226) THEN SET v_NewChar=NCHAR(97);    
 -- Replacing 'Ã£'    
 ELSEIF (v_UnicodeVal=227) THEN SET v_NewChar=NCHAR(97);    
 -- Replacing 'Ã¤'    
 ELSEIF (v_UnicodeVal=228) THEN SET v_NewChar=NCHAR(97);    
 -- Replacing 'Ã¥'    
 ELSEIF (v_UnicodeVal=229) THEN SET v_NewChar=NCHAR(97);    
  
  
 -- For 'Ãˆ'    
 ELSEIF (v_UnicodeVal=200) THEN SET v_NewChar=NCHAR(69);    
 -- For 'Ã‰'    
 ELSEIF (v_UnicodeVal=201) THEN SET v_NewChar=NCHAR(69);    
 -- For 'ÃŠ'    
 ELSEIF (v_UnicodeVal=202) THEN SET v_NewChar=NCHAR(69);    
 -- For 'Ã‹'    
 ELSEIF (v_UnicodeVal=203) THEN SET v_NewChar=NCHAR(69);    
 -- For 'Ã¨'    
 ELSEIF (v_UnicodeVal=232) THEN   SET v_NewChar=NCHAR(101);    
 -- For 'Ã©'    
 ELSEIF (v_UnicodeVal=233) THEN   SET v_NewChar=NCHAR(101);    
 -- For 'Ãª'    
 ELSEIF (v_UnicodeVal=234) THEN   SET v_NewChar=NCHAR(101);    
 -- For 'Ã«'    
 ELSEIF (v_UnicodeVal=235) THEN   SET v_NewChar=NCHAR(101);    
  
  
  
 -- For 'ÃŒ'    
 ELSEIF (v_UnicodeVal=204) THEN   SET v_NewChar=NCHAR(73);    
 -- For 'Ã'    
 ELSEIF (v_UnicodeVal=205) THEN   SET v_NewChar=NCHAR(73);    
 -- For 'ÃŽ'    
 ELSEIF (v_UnicodeVal=206) THEN SET v_NewChar=NCHAR(73);    
 -- For 'Ã'    
 ELSEIF (v_UnicodeVal=207) THEN SET v_NewChar=NCHAR(73);    
 -- For 'Ã¬'    
 ELSEIF (v_UnicodeVal=236) THEN   SET v_NewChar=NCHAR(105);  
 -- For 'Ã­'    
 ELSEIF (v_UnicodeVal=237) THEN   SET v_NewChar=NCHAR(105);  
 -- For 'Ã®'    
 ELSEIF (v_UnicodeVal=238) THEN   SET v_NewChar=NCHAR(105);  
 -- For 'Ã¯'    
 ELSEIF (v_UnicodeVal=239) THEN   SET v_NewChar=NCHAR(105);  
  
 -- For 'Ã‘'    
 ELSEIF (v_UnicodeVal=209) THEN   SET v_NewChar=NCHAR(78);    
 -- For 'Ã±'    
 ELSEIF (v_UnicodeVal=241) THEN   SET v_NewChar=NCHAR(110);    
  
 -- For 'Ã’'    
 ELSEIF (v_UnicodeVal=210) THEN   SET v_NewChar=NCHAR(79);    
 -- For 'Ã“'    
 ELSEIF (v_UnicodeVal=211) THEN   SET v_NewChar=NCHAR(79);    
 -- For 'Ã”'    
 ELSEIF (v_UnicodeVal=212) THEN   SET v_NewChar=NCHAR(79);    
 -- For 'Ã•'    
 ELSEIF (v_UnicodeVal=213) THEN   SET v_NewChar=NCHAR(79);    
 -- For 'Ã–'    
 ELSEIF (v_UnicodeVal=214) THEN   SET v_NewChar=NCHAR(79);    
 -- For 'Ã²'    
 ELSEIF (v_UnicodeVal=242) THEN   SET v_NewChar=NCHAR(111);    
 -- For 'Ã³'    
 ELSEIF (v_UnicodeVal=243) THEN   SET v_NewChar=NCHAR(111);    
 -- For 'Ã´'    
 ELSEIF (v_UnicodeVal=244) THEN   SET v_NewChar=NCHAR(111);    
 -- For 'Ãµ'    
 ELSEIF (v_UnicodeVal=245) THEN   SET v_NewChar=NCHAR(111);    
 -- For 'Ã¶'    
 ELSEIF (v_UnicodeVal=246) THEN   SET v_NewChar=NCHAR(111);    
  
 -- For 'Ã™'    
 ELSEIF (v_UnicodeVal=217) THEN   SET v_NewChar=NCHAR(85);    
 -- For 'Ãš'    
 ELSEIF (v_UnicodeVal=218) THEN   SET v_NewChar=NCHAR(85);    
 -- For 'Ã›'    
 ELSEIF (v_UnicodeVal=219) THEN   SET v_NewChar=NCHAR(85);    
 -- For 'Ãœ'    
 ELSEIF (v_UnicodeVal=220) THEN   SET v_NewChar=NCHAR(85);    
 -- For 'Ã¹'    
 ELSEIF (v_UnicodeVal=249) THEN   SET v_NewChar=NCHAR(117);    
 -- For 'Ãº'    
 ELSEIF (v_UnicodeVal=250) THEN   SET v_NewChar=NCHAR(117);    
 -- For 'Ã»'    
 ELSEIF (v_UnicodeVal=251) THEN   SET v_NewChar=NCHAR(117);    
 -- For 'Ã¼'    
 ELSEIF (v_UnicodeVal=252) THEN   SET v_NewChar=NCHAR(117);    
  
 -- For 'Ã'    
 ELSEIF (v_UnicodeVal=221) THEN   SET v_NewChar=NCHAR(89);    
 -- For 'Ã½'    
 ELSEIF (v_UnicodeVal=253) THEN   SET v_NewChar=NCHAR(121);    
 -- For 'Ã¿'    
 ELSEIF (v_UnicodeVal=255) THEN   SET v_NewChar=NCHAR(121);    
 
 	 -- Change request #1--------------------------------
 -- For Ã§ replace with c
 ELSEIF (v_UnicodeVal=231) THEN   SET v_NewChar=NCHAR(99);    

 -- For Âº replace with a
ELSEIF (v_UnicodeVal=186) THEN   SET v_NewChar=NCHAR(97);    

-- --For (!) replace with space
-- ELSE IF(@UnicodeVal=40)   SET @NewChar=NCHAR(32)    
-- 
-- 
-- --For (.) replace with space
-- ELSE IF(@UnicodeVal=40)   SET @NewChar=NCHAR(32) 

 -- For ÃŸ replace with b
ELSEIF (v_UnicodeVal=223) THEN   SET v_NewChar=NCHAR(98); 

 -- End Change request #1--------------------------------------------------

  
 ELSE      SET v_NewChar=NCHAR(v_UnicodeVal);
 END IF;    
SET v_NewStr=v_NewStr+v_NewChar;    
SET v_startIndex=v_startIndex+1;    
SET v_intCnt=v_intCnt+1;    
End While;    
    */
RETURN p_str;    
   
END ;;
