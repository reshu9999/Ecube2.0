DELIMITER ;;

CREATE PROCEDURE `sp_Hotels_by_sup_city`(

in sup_id int, in city int
)
BEGIN

select HotelId, HotelName from Hotels where Active =1 and cityid =  city and  CompetitorId =sup_id ;
 
END ;;
