DELIMITER ;;

CREATE PROCEDURE `sp_GetNonPausedSubRequests`(
	IN RequestId INT,
    IN Rstatus INT
)
BEGIN

	SET SQL_SAFE_UPDATES = 0;
	
    IF Rstatus=1 then
		SELECT SubRequestId FROM tbl_CrawlRequestDetail WHERE RequestId=RequestId
		AND FK_StatusId NOT IN (1, 3);
	else
		SELECT SubRequestId FROM tbl_CrawlRequestDetail WHERE RequestId=RequestId
		AND FK_StatusId NOT IN (7);
	end if;
END ;;
