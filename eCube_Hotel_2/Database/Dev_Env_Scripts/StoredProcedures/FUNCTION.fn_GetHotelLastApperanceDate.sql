DELIMITER ;;

CREATE FUNCTION `fn_GetHotelLastApperanceDate`(p_intHotelId BigInt) RETURNS datetime(3)
BEGIN
	
	DECLARE v_sdtLastAppearnceDate DateTime(3) DEFAULT Null;

	SELECT LastAppearnceDate INTO v_sdtLastAppearnceDate
	FROM Hotels  
	WHERE HotelId	= p_intHotelId;

	RETURN v_sdtLastAppearnceDate;
	
END ;;
