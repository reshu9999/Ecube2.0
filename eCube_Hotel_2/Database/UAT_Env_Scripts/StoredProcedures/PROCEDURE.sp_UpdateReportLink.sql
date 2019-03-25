DELIMITER ;;

CREATE PROCEDURE `sp_UpdateReportLink`(
IN requestRunId int,
In reportLink varchar(1000)

)
BEGIN


UPDATE tbl_RequestRunDetail tbl
SET
tbl.ReportDownloadLink = reportLink,
tbl.EndDatatime = now(), -- Added By Bhavin on 29-Mar-2018
	tbl.FK_StatusId = 2 -- Added By Bhavin on 29-Mar-2018
WHERE tbl.RequestRunId = requestRunId
limit 1;
END ;;
