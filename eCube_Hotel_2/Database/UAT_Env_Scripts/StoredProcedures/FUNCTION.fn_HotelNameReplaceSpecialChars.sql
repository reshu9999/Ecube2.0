DELIMITER ;;

CREATE FUNCTION `fn_HotelNameReplaceSpecialChars`(Data NVARCHAR(512)) RETURNS varchar(512) CHARSET utf8
BEGIN
/*******************************************************************         
'	Name					: fn_HotelNameReplaceSpecialChars
'	Desc					: To replace specific special character from Hotelname
'	Called by				: sp: spExcelUploadHotelMaster5
'	Example of execution	: select fn_HotelNameReplaceSpecialChars('xxto@mount%xx&amp;x 1Hotel$@s1 1Hotel$@s##1 u  room#%data  u');
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
    Declare minid, maxid int default 0;
    
    set Data = replace(Data, '&amp;','&');
	
    Drop  TEMPORARY TABLE if exists `tmp_HotelName_SpecialChars`;
    CREATE TEMPORARY TABLE `tmp_HotelName_SpecialChars` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `SpecialChars` varchar(512) NOT NULL,
	  `ReplaceChars` varchar(512) NOT NULL,
      Primary Key (`Id`)
	);
    
    SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ;
    
    Insert into tmp_HotelName_SpecialChars (SpecialChars,ReplaceChars)
    Select SpecialChars, ReplaceChars 
    from HotelNameSpecialChars 	where IsActive = 1 
    ORDER BY length(SpecialChars) DESC, HotelNameSpecialCharsId;
    
    select min(id), max(id) into minid, maxid 
    from tmp_HotelName_SpecialChars ;

	while maxid >= minid and minid<=3000 do
		set Data = (select replace(Data, SpecialChars, ReplaceChars)  
					FROM tmp_HotelName_SpecialChars 
					where id= minid );
            
		set minid = minid + 1;
    end while;
    
    /*set  Data = (select Data = replace(Data, SpecialChars, ReplaceChars)  
	FROM HotelNameSpecialChars 
	where isactive = 1
	ORDER BY LENgth(SpecialChars) DESC -- limit 10
    );
	*/
    SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ ;
    
	Drop  TEMPORARY TABLE if exists `tmp_HotelName_SpecialChars`;
    RETURN REPLACE(LTRIM(RTRIM(Data)),'  ',' ');
    
END ;;
