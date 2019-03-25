DELIMITER ;;

CREATE PROCEDURE `InsertHotelMaster`()
BEGIN
set foreign_key_checks = 0;

ALTER TABLE `Hotels` CHANGE `HotelId` `HotelId` bigint(20)  NOT NULL;

truncate table Hotels;

insert into Hotels (HotelId,WebSiteHotelId,HotelName,HotelAddress1,HotelAddress2,CityId,HotelBrandName,StarRatingId,HotelPostCode,CompetitorId,HotelMatchStatus,HotelDescription,isProceesed,matchhotelname,DipBagSyncId,IsMailed,RequestId,ismailed1,Active,CreatedBy,CreatedDate,ModifiedBy,ModifiedDatetime,MatchHotelAddress1,isConsiderForMatching,LastAppearnceDate,LastRequestRunId,Longitude,Latitude,YieldManager,ContractManager,DemandGroup,CrawledHotelAddress,CrawledHotelStar,ZoneName,CrawledZoneName,HotelStatusId)
Select HotelId,WebSiteHotelId,HotelName,HotelAddress1,HotelAddress2,CityId,HotelBrandName,StarRatingId,HotelPostCode,CompetitorId,HotelMatchStatus,HotelDescription,isProceesed,matchhotelname,DipBagSyncId,IsMailed,RequestId,ismailed1,Active,CreatedBy,CreatedDate,ModifiedBy,ModifiedDatetime,MatchHotelAddress1,isConsiderForMatching,LastAppearnceDate,LastRequestRunId,Longitude,Latitude,YieldManager,ContractManager,DemandGroup,CrawledHotelAddress,CrawledHotelStar,ZoneName,CrawledZoneName,HotelStatusId
from ecube_Staging.Hotels order by HotelId;




ALTER TABLE `Hotels` CHANGE `HotelId` `HotelId` bigint(20) NOT NULL auto_increment;

SET @new_index = (SELECT MAX(HotelId) FROM Hotels);
SET @sql = CONCAT('ALTER TABLE Hotels AUTO_INCREMENT = ', @new_index);
PREPARE st FROM @sql;
EXECUTE st;


set foreign_key_checks = 1;
END ;;
