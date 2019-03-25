DELIMITER ;;

CREATE PROCEDURE `MessagingCategoryQueue`()
BEGIN
	
set  @CategoryLastRun = (Select QueueLastRunDate 
from  tbl_RequestUpdate order by id desc limit 1);

select 
temp.RequestId,
temp.SubRequestId,
temp.RequestRunID,
temp.RequestUrl,
temp.IsCategory,
temp.DomainName,
temp.ParsingScriptName,
temp.ScrapingScriptName,
temp.PointOfSale,
temp.CountryName,
temp2.BLIGroupName
from 
(select A.RequestId,
A.SubRequestId,A.RequestRunID,
A.RequestUrl,
A.FK_RequestTypeId as IsCategory,
B.DomainName,B.ParsingScriptName,B.ScrapingScriptName,
C.PointOfSale,D.CountryName,rq.FK_BLIId
from tbl_CrawlRequestDetail A inner join tbl_RequestMaster rq 
on A.RequestId = rq.RequestId
join tbl_DomainMaster B on (A.DomainId=B.DomainId)
left join tbl_BLIDomainProxyCountryMapping C 
on (A.DomainId=C.DomainId) 
and C.BliId = rq.FK_BLIId
join tbl_CountryMaster D 
on (D.CountryID = B.FK_CountryId)
where  (A.FK_StatusId = 5) and (FK_RequestTypeId = 1
or FK_RequestTypeId = 0)) as temp
inner join 
(
select bM.BliId,gM.BLIGroupName
from tbl_BliMaster bM inner join tbl_Bli_GroupMaster gM
on bM.BLI_GRP_Id = gM.Id where bM.active =1) as temp2  on 
temp.FK_BLIId = temp2.BliId;



# Below Query Comment for Dynamic Queue 28 march

/*
select A.RequestId,A.SubRequestId,A.RequestRunID,A.RequestUrl,A.FK_RequestTypeId as IsCategory,
B.DomainName,B.ParsingScriptName,B.ScrapingScriptName,
C.PointOfSale,D.CountryName,A.bligroupname
from tbl_CrawlRequestDetail A inner join tbl_RequestMaster rq on A.RequestId = rq.RequestId
join tbl_DomainMaster B on (A.DomainId=B.DomainId)
left join tbl_BLIDomainProxyCountryMapping C on (A.DomainId=C.DomainId) and C.BliId = rq.FK_BLIId
join tbl_CountryMaster D on (D.CountryID = B.FK_CountryId)
where  (StartDatetime > @CategoryLastRun) and (FK_RequestTypeId = 1
or FK_RequestTypeId = 0);
*/


Update tbl_RequestUpdate set QueueLastRunDate = now() where Id = 1;


END ;;
