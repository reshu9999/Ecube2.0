DELIMITER ;;

CREATE PROCEDURE `PriorityMessagingCategoryQueue`()
BEGIN
	
set  @CategoryLastRun = (Select QueueLastRunDate from  tbl_RequestUpdate order by id desc limit 1);


select A.RequestId,A.SubRequestId,A.RequestRunID,A.RequestUrl,A.FK_RequestTypeId as IsCategory,
B.DomainName,B.ParsingScriptName,B.ScrapingScriptName,
C.PointOfSale,D.CountryName
from tbl_CrawlRequestDetail A inner join tbl_RequestMaster rq on A.RequestId = rq.RequestId
join tbl_DomainMaster B on (A.DomainId=B.DomainId)
left join tbl_BLIDomainProxyCountryMapping C on (A.DomainId=C.DomainId) and C.BliId = rq.FK_BLIId
join tbl_CountryMaster D on (D.CountryID = B.FK_CountryId)
where  (StartDatetime > @CategoryLastRun) and (FK_RequestTypeId = 1
or FK_RequestTypeId = 0) and (CrawlPriority = 1);

/*
select A.RequestId,A.SubRequestId,A.RequestRunID,A.RequestUrl,A.FK_RequestTypeId as IsCategory,
B.DomainName,B.ParsingScriptName,B.ScrapingScriptName,
C.PointOfSale,D.CountryName
from tbl_CrawlRequestDetail A inner join tbl_RequestMaster rq on A.RequestId = rq.RequestId
join tbl_DomainMaster B on (A.DomainId=B.DomainId)
join tbl_BLIDomainProxyCountryMapping C on (A.DomainId=C.DomainId) and C.BliId = rq.FK_BLIId
join tbl_CountryMaster D on (D.CountryID = B.FK_CountryId);

*/
#join tbl_BliMaster E on (E.BliId = C.BliId);

/*where StartDatetime > @CategoryLastRun;*/

Update tbl_RequestUpdate set QueueLastRunDate = now() where Id = 1;


END ;;
