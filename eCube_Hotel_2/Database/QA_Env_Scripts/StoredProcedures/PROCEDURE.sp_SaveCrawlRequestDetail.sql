DELIMITER ;;

CREATE PROCEDURE `sp_SaveCrawlRequestDetail`(
RequestId int,
SubRequestId int,
RequestUrl varchar(500),
Response varchar(1000),
Status varchar(30),
StartDatetime datetime,
EndDatetime datetime,
/*StartDatetime varchar(20),
EndDatetime varchar(20),*/
IsCategory varchar(20),
PointOfSale varchar(50),
CategoryScraperScript varchar(100),
ParserScript varchar(100),
Domain_Name varchar(50),
ProductScraperScript varchar(100)
)
BEGIN
set  @RequestRunId = (Select RequestRunId from tbl_RequestRunDetail where FK_RequestId = RequestId limit 1);
set  @StatusId = (Select StatusId from tbl_StatusMaster where StatusTitle = 'InQue' limit 1);

set  @Domain_Id = (Select DomainId from tbl_DomainMaster where DomainName = Domain_Name limit 1);

INSERT INTO tbl_CrawlRequestDetail
(
RequestRunId,
ParentSubRequestId,
RequestUrl,
/*Response,*/
FK_StatusId,
StartDatetime,
/*EndDatetime,*/
RequestId,
IsCategory,
PointOfSale,
ScrapperScript,
ParserScript,
DomainId,
FK_RequestTypeId
/*,ProductScraperScript*/
)
VALUES
(
@RequestRunId,
SubRequestId,
/*RequestUrl,*/
Response,
@StatusId,
NOW(),
/*EndDatetime,*/
RequestId,
IsCategory,
PointOfSale,
CategoryScraperScript,
ParserScript,
@Domain_Id,
0
/*,ProductScraperScript*/
);


END ;;
