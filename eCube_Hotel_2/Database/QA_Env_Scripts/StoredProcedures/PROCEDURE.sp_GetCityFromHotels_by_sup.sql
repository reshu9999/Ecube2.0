DELIMITER ;;

CREATE PROCEDURE `sp_GetCityFromHotels_by_sup`(

in param varchar(100) 
)
BEGIN

call sp_split(param,',');

   
select  Distinct ci.CityId, ci.CityName from  Cities ci 
inner join Hotels h 
on h.CityId = ci.CityId
And h.active = 1
Where h.CompetitorId in(
	Select items From SplitValue
   );
 
 
END ;;
