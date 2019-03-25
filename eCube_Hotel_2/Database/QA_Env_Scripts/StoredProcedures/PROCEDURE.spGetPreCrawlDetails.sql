DELIMITER ;;

CREATE PROCEDURE `spGetPreCrawlDetails`(IN ReqID INT)
BEGIN
	
    select * from tbl_hotelrequestinputdetails
	where RequestId = ReqID;
    
END ;;
