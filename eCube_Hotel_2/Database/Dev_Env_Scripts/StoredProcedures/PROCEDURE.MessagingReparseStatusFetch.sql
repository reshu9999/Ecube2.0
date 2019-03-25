DELIMITER ;;

CREATE PROCEDURE `MessagingReparseStatusFetch`()
BEGIN

set  @RequestRunId = (SELECT RequestRunId
FROM tbl_RequestRunDetail
where ReParseStatus = "Reparse");

update tbl_RequestRunDetail
set ReParseStatus = "Running"
where RequestRunId in (@RequestRunId);

END ;;
