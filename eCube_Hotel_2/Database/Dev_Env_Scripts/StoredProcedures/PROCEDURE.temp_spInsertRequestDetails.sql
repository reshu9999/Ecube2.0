DELIMITER ;;

CREATE PROCEDURE `temp_spInsertRequestDetails`(
in RequestId INT,
in RequestRunId INT
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


select 19,RequestUrl,5,
CURDATE(),
'False',
0,0,0,0,
ReqInputDetailId,
RequestTypeId,
RequestId,FK_DomainId from tbl_RequestInputDetails 
where FK_RequestId= 20 ;


END ;;
