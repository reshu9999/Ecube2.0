DELIMITER ;;

CREATE PROCEDURE `sp_UpdateCrawlStatusPause`(
	IN RequestId INT
)
BEGIN

	SET SQL_SAFE_UPDATES = 0;

	UPDATE tbl_RequestRunDetail SET FK_StatusId=7 WHERE FK_RequestId=RequestId
	AND FK_StatusId IN (1,3);

END ;;
