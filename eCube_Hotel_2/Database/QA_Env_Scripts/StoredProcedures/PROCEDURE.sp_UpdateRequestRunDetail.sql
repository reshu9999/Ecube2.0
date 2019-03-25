DELIMITER ;;

CREATE PROCEDURE `sp_UpdateRequestRunDetail`(
status varchar(30),
requestId int,
subRequestId int
)
BEGIN
set  @StatusId = (Select StatusId from tbl_StatusMaster where StatusTitle = status limit 1);
set  @RequestRunId = (Select RequestRunId from tbl_RequestRunDetail where FK_RequestId = requestId 
					order by RequestRunId desc limit 1);
set @CompletedRequest = 0;
set @PNFCount = 0;
if(status = 'Completed') then
	set @CompletedRequest = 1;
else
	set @PNFCount = 1;
end if;
UPDATE tbl_RequestRunDetail tbl
SET
tbl.CompletedRequests = tbl.CompletedRequests + @CompletedRequest,
tbl.InQueRequests = tbl.InQueRequests - 1,
tbl.PNFCounts = tbl.PNFCounts + @PNFCount 
WHERE tbl.RequestRunId = @RequestRunId
;


UPDATE tbl_CrawlRequestDetail tbl
SET
tbl.FK_StatusId = @StatusId
, tbl.endDateTime = NOW(6) -- Added By Bhavin on 29-Mar-2018
WHERE tbl.SubRequestId = subRequestId;
END ;;
