DELIMITER ;;

CREATE PROCEDURE `spInsertRequestDetails_old`(
IN RequestId INT,
IN RequestRunId INT
)
BEGIN


INSERT INTO `eCube_Centralized_DB`.`tbl_CrawlRequestDetail`
(
`RequestRunId`,
`RequestUrl`,
`FK_StatusId`,
`StartDatetime`,
`IsRecrawl`,
`RecrawlCount`,
`IsReparse`,
`CrawlPriority`,
`CrawlTimeout`,
`Requestinputdetailid`,
`FK_RequestTypeId`,
`RequestId`,
`DomainId`) 


select RequestRunId,RequestUrl,5,
CURDATE(),
'False',
0,0,0,0,
ReqInputDetailId,
RequestTypeId,
RequestId,FK_DomainId from tbl_RequestInputDetails 
where FK_RequestId= RequestId ;


END ;;
