DELIMITER ;;

CREATE PROCEDURE `sp_GetRequestRunId`(
requestId int
)
BEGIN
set  @RequestRunId = (Select RequestRunId from tbl_RequestRunDetail where FK_RequestId = requestId limit 1);
select @RequestRunId as RequestRunId ;

END ;;
