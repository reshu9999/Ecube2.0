DELIMITER ;;

CREATE PROCEDURE `spUpdateRequestStatus`(
IN RequestRunId INT)
BEGIN
SET SQL_SAFE_UPDATES = 0;
Update tbl_RequestRunDetail set FK_StatusId = 5 where RequestRunId = RequestRunId;
SET SQL_SAFE_UPDATES = 1;
END ;;
