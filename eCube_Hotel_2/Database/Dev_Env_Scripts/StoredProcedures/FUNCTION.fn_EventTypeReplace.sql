DELIMITER ;;

CREATE FUNCTION `fn_EventTypeReplace`(p_Data   VARCHAR(4000)
 ) RETURNS varchar(4000) CHARSET latin1
BEGIN      
 
Declare v_Data Longtext Default '';
-- Declare p_Data Varchar(4000) Default '';

 Set v_Data = p_Data;   
 Set v_Data = REPLACE(v_Data, '(','');    
 Set v_Data = REPLACE(v_Data, ')','');    
 Set v_Data = REPLACE(v_Data, '+','');
 
 Set v_Data = REPLACE(v_Data, '0','');
 Set v_Data = REPLACE(v_Data, '1','');
 Set v_Data = REPLACE(v_Data, '2','');
 Set v_Data = REPLACE(v_Data, '3','');
 Set v_Data = REPLACE(v_Data, '4','');
 Set v_Data = REPLACE(v_Data, '5','');
 Set v_Data = REPLACE(v_Data, '6','');
 Set v_Data = REPLACE(v_Data, '7','');
 Set v_Data = REPLACE(v_Data, '8','');
 Set v_Data = REPLACE(v_Data, '9','');
 
 Set v_Data =  ltrim(rtrim(v_Data));
 
 Call sp_split(v_Data, '/');
 
 Set @Data = p_Data;
 SELECT @Data + Case WHen nvcrLeadTime IS Not Null Then replace(@Data,nvcrLeadTime, nvcrEventtype) Else replace(@Data,DT.items, 'Free') End  
	Into @Data
	FROM MstEventTypeTemplate ML 
	Right Join SplitValue DT
	On ML.nvcrLeadTime = DT.items;

 Set p_Data = REPLACE(LTRIM(RTRIM(@Data)),'  ',' ');
 
RETURN p_Data; 
   
END ;;
