DELIMITER ;;

CREATE PROCEDURE `sp_DisplayLeadTime`()
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
    
FROM  MstLeadTimeTemplate;
END ;;
