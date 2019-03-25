DELIMITER ;;

CREATE PROCEDURE `usp_CrawlRequsts`(in RequestType varchar(10))
BEGIN
Create temporary table if not exists tmpRequests as

(select b.RequestRunId as RequestRunId,a.ReqInputDetailId as SubrequestId,a.url as RequestUrl,b.RequestId as RequestId,c.DomainName as Domain from tbl_RequestInputDetails a right join RequestRunDetail b 
on a.RID_RequestId = b.RequestId left join tbl_DomainMaster c on a.RID_DomainId = c.DomainId
where b.Status = 'InQue');
INSERT INTO `eCube_Centralized_DB`.`tbl_CrawlRequestDetail`
(
`RequestRunId`,
`SubRequestId`,
`RequestUrl`,
`Status`,
`StartDatetime`,
`CrawlerId`,
`IsRecrawl`,
`RecrawlCount`,
`ErrorCode`,
`Redistribute`,
`Requestinputdetails`,
`RequestType`,
`ProxyCountry`,
`ProxyScriptName`,
`RequestId`,
`DomainUrl`)

select RequestRunId,SubrequestId,RequestUrl,'Push InQue',
CURDATE(),
0,
'False',
0,
'',
'',
0,
@RequestType,
'',
'',RequestId,Domain from tmpRequests;


set sql_safe_updates=0;
update RequestRunDetail set Status = 'Push InQue' where RequestRunId in 
(select distinct(RequestRunId)
from tmpRequests); 
END ;;
