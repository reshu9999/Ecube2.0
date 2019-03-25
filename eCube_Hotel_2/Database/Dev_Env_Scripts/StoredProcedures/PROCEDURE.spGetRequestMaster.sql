DELIMITER ;;

CREATE PROCEDURE `spGetRequestMaster`(IN ReqID INT)
BEGIN
	
    Select RequestName, RequestDescription, RequestFile from tbl_RequestMaster
	where RequestId = ReqID;
    
END ;;
