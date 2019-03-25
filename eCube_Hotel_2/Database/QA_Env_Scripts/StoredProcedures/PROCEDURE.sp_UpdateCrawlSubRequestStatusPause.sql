DELIMITER ;;

CREATE PROCEDURE `sp_UpdateCrawlSubRequestStatusPause`(
	IN RequestId INT,
    IN RequestSubId INT
)
BEGIN

	SET SQL_SAFE_UPDATES = 0;

	UPDATE tbl_CrawlRequestDetail SET FK_StatusId=7 WHERE RequestId=RequestId
	AND SubRequestId=RequestSubId;

END ;;
