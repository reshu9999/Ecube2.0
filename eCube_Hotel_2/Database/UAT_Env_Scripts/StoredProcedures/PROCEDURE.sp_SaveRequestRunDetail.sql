DELIMITER ;;

CREATE PROCEDURE `sp_SaveRequestRunDetail`(
IN requestId int,
IN flag int
)
BEGIN
        
        IF (FLAG = 1) THEN

                INSERT INTO TestAddRequest(RequestId,Date) Values(requestId,NOW());

                set  @TotalRequests = (Select Count(*) from tbl_RequestInputDetails where FK_RequestId = requestId);
                set  @StatusId = (Select StatusId from tbl_StatusMaster where StatusTitle = 'InQue' limit 1);
                INSERT INTO tbl_RequestRunDetail
                (
                FK_RequestId,
                TotalRequests,
                CompletedRequests,
                InQueRequests,
                PNFCounts,
                FK_StatusId,
                StartDatetime
                )
                VALUES
                (
                requestId,
                @TotalRequests,
                0,
                @TotalRequests,
                0,
                @StatusId,
                NOW()
                );

        ELSEIF (FLAG = 2) THEN
                INSERT INTO TestAddRequest(RequestId,Date) Values(requestId,NOW());

                set  @TotalRequests = (Select Count(*) from tbl_hotelrequestinputdetails where RequestId = requestId);
                set  @StatusId = (Select StatusId from tbl_StatusMaster where StatusTitle = 'InQue' limit 1);
                INSERT INTO tbl_RequestRunDetail
                (
                FK_RequestId,
                TotalRequests,
                CompletedRequests,
                InQueRequests,
                PNFCounts,
                FK_StatusId,
                StartDatetime
                )
                VALUES
                (
                requestId,
                @TotalRequests,
                0,
                @TotalRequests,
                0,
                @StatusId,
                NOW()
                );

    ELSE
                INSERT INTO TestAddRequest(RequestId,Date) Values(requestId,NOW());

                set  @TotalRequests = (Select Count(*) from tbl_hotelflightrequestinputdetails where RequestId = requestId);
                set  @StatusId = (Select StatusId from tbl_StatusMaster where StatusTitle = 'InQue' limit 1);
                INSERT INTO tbl_RequestRunDetail
                (
                FK_RequestId,
                TotalRequests,
                CompletedRequests,
                InQueRequests,
                PNFCounts,
                FK_StatusId,
                StartDatetime
                )
                VALUES
                (
                requestId,
                @TotalRequests,
                0,
                @TotalRequests,
                0,
                @StatusId,
                NOW()
                );
        END IF; 

END ;;
