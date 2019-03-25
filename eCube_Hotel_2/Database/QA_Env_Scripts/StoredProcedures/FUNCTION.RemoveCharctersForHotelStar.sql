DELIMITER ;;

CREATE FUNCTION `RemoveCharctersForHotelStar`(p_string VARCHAR(1000)) RETURNS varchar(100) CHARSET utf8
BEGIN
/*******************************************************************         
'	Name					: RemoveCharctersForHotelStar
'	Desc					: To get Proper Hotel Start rating from given string
'	Called by				: sp: spExcelUploadHotelMaster5
'	Example of execution	: select RemoveCharctersForHotelStar('qq4rr.tt5l');
INPUT PARAMETRS		 	 
	Data NVARCHAR(512)
Retruns 
	varchar(512) CHARSET utf8
'	Created by				: Bhavin.Dhimmar
'	Date of creation		: 05-Jun-2018

******************************************************************************************************
Change History
******************************************************************************************************
Sr.No.		Date:			Changed by:					Description:
******************************************************************************************************/	
	declare v_pos, v_len, v_init int; 
    declare v_char varchar(1);
    declare o_number varchar(64);
    
    set p_string = ltrim(rtrim(p_string));
    set o_number = '';
    set v_len = (select length(p_string)); 
    set v_init = 0;
    
    if v_len > 0 then 
		while v_len >= v_init do
			SET v_char= SUBSTRING(p_string,v_init,1);
			SET v_pos= FIND_IN_SET(v_char,'0,1,2,3,4,5,6,7,8,9,.');
    
			if v_pos > 0 then
				SET o_number=CONCAT(o_number,v_char);
            end if;
            
            set v_init = v_init + 1;
        End while;
        
        RETURN o_number;
	else
		Return '';
    End if;
	-- SET v_pos = PATINDEX('%[^0-9^_^.]%', UPPER(p_string));
	-- set v_pos = SELECT LOCATE('ev', 'web development');
/* WHILE v_pos > 0
DO
SET p_string = REPLACE(p_string, SUBSTRING(p_string, v_pos, 1), '');
SET v_pos = PATINDEX('%[^0-9^_^.]%', UPPER(p_string));
END WHILE;
*/
	
	
END ;;
