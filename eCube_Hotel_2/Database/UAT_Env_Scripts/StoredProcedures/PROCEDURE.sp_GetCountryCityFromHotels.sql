DELIMITER ;;

CREATE PROCEDURE `sp_GetCountryCityFromHotels`(
In p_IsCountry tinyint(1),
in param int 
)
BEGIN
if (p_IsCountry = 1) then

select distinct c.CountryID, c.CountryName
from tbl_CountryMaster c inner join Cities ci on c.CountryId = ci.CountryId and c.active=1
inner join Hotels h on h.CityId = ci.CityId  order by c.CountryName;
 
elseif (p_IsCountry = 2) then
select p.HotelGroupId,p.HotelGroup,c.cnt as `Count`, p.Active  from HotelGroups as p left join (
select HotelGroupId, Count(0) as cnt from HotelGroupDetails  group by HotelGroupId) as c
on p.HotelGroupId = c.HotelGroupId and p.Active =1;

elseif (p_IsCountry = 3) then

 
select distinct ci.CityId, ci.CityName from tbl_CountryMaster c inner join Cities ci on c.CountryId = ci.CountryId and c.active=1
inner join Hotels h on h.CityId = ci.CityId and c.CountryId =param order by ci.CityName;
 
elseif (p_IsCountry = 4) then
select   HotelId,HotelName from Hotels where Active =1 and cityid =param and CompetitorId =1;


elseif (p_IsCountry = 5) then

select distinct ci.CityId, ci.CityName from  Cities ci 
inner join Hotels  h
on h.CityId = ci.CityId and h .CompetitorId =param and h.active = 1;

elseif (p_IsCountry = 6) then

select   HotelId, HotelName, cityname , sr.StarRating , HotelPostCode  ,
case when h.Active  =1 then 'Active' else 'InActive' end as 'Status' ,
WebSiteHotelId  ,HotelAddress1, HotelAddress2,HotelBrandName,HotelMatchStatus,HotelDescription,isProceesed,
matchhotelname,DipBagSyncId,IsMailed,ismailed1
from Hotels as h inner join Cities as c on c.cityid= h.cityid 
inner join tbl_CountryMaster co on co.countryid = c.countryid 
inner join StarRatings sr on sr.StarRatingId = h.StarRatingid    
where c.cityid=param 
order by h.HotelId desc;




elseif (p_IsCountry = 7) then
 select   distinct cityname, c.cityid    
from Hotels as h inner join Cities as c on c.cityid= h.cityid  order by cityname ; 


elseif (p_IsCountry = 8) then
select  StarRatingId, StarRating   from StarRatings where Active =1; 

elseif (p_IsCountry = 9) then
select  StarRatingId, StarRating   from StarRatings where Active =1; 


elseif (p_IsCountry = 10) then
select ci.CityId, ci.CityName, c.countryname, ci.CityCode, ci.Active ,
case when ci.Active  =1 then 'Active' else 'InActive' end as 'Status' 
from tbl_CountryMaster c inner join Cities ci on c.CountryId = ci.CountryId  order by ci.cityid desc;

elseif (p_IsCountry = 11) then
select c.countryId, c.countryname,  c.Active from tbl_CountryMaster c  where c.Active =1 order by c.countryname asc;


elseif (p_IsCountry = 12) then
select *,case when Active  =1 then 'Active' else 'InActive' end as 'Status'   from tbl_CountryMaster ;


elseif (p_IsCountry = 13) then
select *,case when Active  =1 then 'Active' else 'InActive' end as 'Status'   from HotelPOS order by  PointOfSaleId desc ;


elseif (p_IsCountry = 14) then
select *,case when Active  =1 then 'Active' else 'InActive' end as 'Status' from BoardTypes;


elseif (p_IsCountry = 15) then
select a.AirportCodeId ,  a.AirportCode ,a.AirportName ,a.Active ,ci.cityname, t.countryName ,case when a.Active  =1 then 'Active' else 'InActive' end as 'Status' from AirportCodes as a inner join 
tbl_CountryMaster as t  on t.CountryId =a.CountryId inner join Cities ci on ci.CityID= a.CityID order by a.AirportCodeId desc;



elseif (p_IsCountry = 16) then
select CityId, CityName from Cities where Active =1 order by cityname;


elseif (p_IsCountry = 17) then
select distinct ci.CityId, ci.CityName from tbl_CountryMaster c inner join Cities ci on c.CountryId = ci.CountryId and c.active=1
inner join Hotels h on h.CityId = ci.CityId  order by ci.CityName ;


elseif (p_IsCountry = 18) then
select CityId, CityName from Cities where Active =1 order by cityname;


elseif (p_IsCountry = 19) then
select HotelStatusId, HotelStatus from HotelStatus where Active =1  order by HotelStatus;


End if;
END ;;
