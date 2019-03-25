DELIMITER ;;

CREATE PROCEDURE `GetHotelCount`(
in batchid int ,
in intDipBagDynamicId int)
BEGIN
select *  from Hotel_Count_Ecube_MDM_5;
END ;;
