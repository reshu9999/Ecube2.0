DELIMITER ;;

CREATE PROCEDURE `sp_ExcelUploadHotelMaster_TEST`( p_intSupplierId int,  
 p_intUserId Int,  
 out p_nvcrErrorMsg  nvarchar(200)  
 
 )
BEGIN

  select * from temphotelmaster;
END ;;
