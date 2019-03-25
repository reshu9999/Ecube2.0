DELIMITER ;;

CREATE PROCEDURE `sp_SaveReportRunDetail`(
IN requestRunId int,
IN userId int
)
BEGIN
set  @StatusId = (Select StatusId from tbl_StatusMaster where StatusTitle = 'InQue' limit 1);
set @ReportName = (select concat( coalesce(tb1.RequestName),'_', coalesce(cast(Now() as char),'')) as ReportName from tbl_RequestMaster tb1
				  join tbl_RequestRunDetail tb2 on tb1.RequestId = tb2.FK_RequestId
				  where RequestRunId = requestRunId Limit 1);

INSERT INTO tbl_ReportRunDetail
(
RID_RequestRunId,
FK_StatusId,
CreatedBy,
CreatedDate,
ReportName
)
VALUES
(
requestRunId,
@StatusId,
/*userId,*/
1,
NOW(),
@ReportName)
;
END ;;
