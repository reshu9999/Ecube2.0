DELIMITER ;;

CREATE PROCEDURE `sp_DisplayLeadTimeAdhoc`()
BEGIN
SELECT 
	nvcrBookingDate,
    nvcrBatchName,
    nvcrDestination,
    nvcrLeadTime,
    nvcrEventType,
    intNights,
    NvcrAccountName,
    NvcrPrimarySupplier
FROM MstAdhocLeadTimeTemplate;
 


END ;;
