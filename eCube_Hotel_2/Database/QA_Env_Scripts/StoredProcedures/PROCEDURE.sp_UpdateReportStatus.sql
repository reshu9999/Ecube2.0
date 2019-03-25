DELIMITER ;;

CREATE PROCEDURE `sp_UpdateReportStatus`(
requestRunId int,
status varchar(10)
)
BEGIN
set  @StatusId = (Select StatusId from tbl_StatusMaster where StatusTitle = status limit 1);
set @StartDatetime = NULL;
set @EndDatetime = NULL;
if(status = 'WIP') then
	set @StartDatetime = NOW();
else
	set @EndDatetime = NOW();
end if;
UPDATE tbl_ReportRunDetail tbl
SET
tbl.FK_StatusId = @StatusId,
tbl.StartDate = if(status = 'WIP',NOW(),tbl.StartDate),
tbl.EndDate = if(status = 'Completed',NOW(),tbl.EndDate)
WHERE tbl.RID_RequestRunId = requestRunId
;

set @ReportName = (Select ReportName from tbl_ReportRunDetail WHERE RID_RequestRunId = requestRunId limit 1);

Select @ReportName as ReportName;
END ;;
