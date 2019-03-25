DELIMITER ;;

CREATE FUNCTION `udf_StripHTML`(p_HTMLText LONGTEXT) RETURNS longtext CHARSET latin1
BEGIN
/*******************************************************************         
'	Name					: udf_StripHTML
'	Desc					: To replace HTML/XML tags
'	Called by				: sp: spExcelUploadHotelMaster5
'	Example of execution	: select udf_StripHTML('<td>Hello eCube</td>');
INPUT PARAMETRS		 	 
	p_HTMLText LONGTEXT
Retruns 
	longtext CHARSET latin1
'	Created by				: Bhavin.Dhimmar
'	Date of creation		: 05-Jun-2018

******************************************************************************************************
Change History
******************************************************************************************************
Sr.No.		Date:			Changed by:					Description:
******************************************************************************************************/	
    DECLARE v_Start INT;
    DECLARE v_End INT;
    DECLARE v_Length INT;
   /* SET v_Start = CHARINDEX('<',p_HTMLText);
    SET v_End = CHARINDEX('>',p_HTMLText,CHARINDEX('<',p_HTMLText));
    SET v_Length = (v_End - v_Start) + 1;
    WHILE v_Start > 0 AND v_End > 0 AND v_Length > 0
    DO
        SET p_HTMLText = INSERT(p_HTMLText,v_Start,v_Length,'');
        SET v_Start = CHARINDEX('<',p_HTMLText);
        SET v_End = CHARINDEX('>',p_HTMLText,CHARINDEX('<',p_HTMLText));
        SET v_Length = (v_End - v_Start) + 1;
    END WHILE;
    set p_HTMLText=replace(REPLACE(p_HTMLText,'<',''),'>','');
    RETURN LTRIM(RTRIM(p_HTMLText));
    */
    
     SET v_Start = LOCATE('<'  , p_HTMLText);
    SET v_End = LOCATE( '>', p_HTMLText,  POSITION('<' in p_HTMLText));
    SET v_Length = (v_End - v_Start) + 1;
    WHILE v_Start > 0 AND v_End > 0 AND v_Length > 0
    DO
        SET p_HTMLText = INSERT(p_HTMLText,v_Start,v_Length,'');
        SET v_Start = LOCATE('<'  , p_HTMLText);
        SET v_End = LOCATE( '>', p_HTMLText,  POSITION('<' in p_HTMLText));
        SET v_Length = (v_End - v_Start) + 1;
    END WHILE;
    set p_HTMLText=replace(REPLACE(p_HTMLText,'<',''),'>','');
    RETURN LTRIM(RTRIM(p_HTMLText));
END ;;
