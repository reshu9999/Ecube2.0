DELIMITER ;;

CREATE PROCEDURE `sp_GetInQueRequest`()
BEGIN
set  @StatusId = (Select StatusId from tbl_StatusMaster where StatusTitle = 'InQue' limit 1);
Select ReportRunId, RID_RequestId, ReportName, RID_RequestRunId from tbl_ReportRunDetail where FK_StatusId = @StatusId;


END ;;
