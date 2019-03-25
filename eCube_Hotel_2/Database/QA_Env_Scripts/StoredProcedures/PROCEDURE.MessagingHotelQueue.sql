DELIMITER ;;

CREATE PROCEDURE `MessagingHotelQueue`()
BEGIN

select 
temp.RequestId,
temp.HotelCrawlRequestDetailId,
temp.RequestRunID,
temp.IsCategory,
temp.DomainName,
temp.ParsingScriptName,
temp.ScrapingScriptName,
#temp.PointOfSale,
temp2.BLIGroupName,
temp.DomainId,
temp.CheckInDate,
temp.RentalLength,
temp.CompetitorName,
temp.PointOfSale,
temp.Adult,
temp.Child,
temp.CrawlMode,
temp.HotelName,
temp.WebSiteHotelId,
temp.CityName,
temp.CountryName,
temp.StarRating,
temp.BoardType,
temp.RoomType
from 
(select A.RequestId,
A.HotelCrawlRequestDetailId,
A.RequestRunID,
#A.FK_RequestTypeId as IsCategory,
A.IsCategory,
B.DomainName,
B.ParsingScriptName,
B.ScrapingScriptName,
rq.FK_BLIId,
B.DomainId,
A.CheckInDate,
A.RentalLength,
A.CompetitorName,
A.PointOfSale,
A.Adult,
A.Child,
A.CrawlMode,
A.HotelName,
A.WebSiteHotelId,
A.CityName,
A.CountryName,
A.StarRating,
A.BoardType,
A.RoomType
from tbl_HotelCrawlRequestDetail A inner join tbl_RequestMaster rq 
on A.RequestId = rq.RequestId
join tbl_DomainMaster B on (A.CompetitorName=B.DomainName)
-- left join tbl_BLIDomainProxyCountryMapping C 
-- on (A.DomainId=C.DomainId) 
-- and C.BliId = rq.FK_BLIId
join tbl_CountryMaster D 
on (D.CountryID = B.FK_CountryId)
where  (A.StatusId = 5)) as temp
inner join 
(
select bM.BliId,gM.BLIGroupName
from tbl_BliMaster bM inner join tbl_Bli_GroupMaster gM
on bM.BLI_GRP_Id = gM.Id where bM.active =1) as temp2  on 
temp.FK_BLIId = temp2.BliId;

END ;;
