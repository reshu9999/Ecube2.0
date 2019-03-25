DELIMITER ;;

CREATE PROCEDURE `spGetRequestInputDomainDetails`(IN ReqID INT)
BEGIN

	Select RequestUrl from tbl_RequestInputDetails 
	where FK_RequestId = ReqID;

END ;;
