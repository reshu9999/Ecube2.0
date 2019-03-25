DELIMITER ;;

CREATE PROCEDURE `LastResult_Report`(

)
BEGIN
-- SELECT * FROM BatchCrawlDatafinal_ECUBE_MDM_5_TEST;

INSERT INTO `eCube_Centralized_DB`.`BatchCrawlDatafinal_ECUBE_MDM_5` (`nvcrCompany`, `Nights`, `nvcrHotel`, `HotelId`, `nvcrPointOfSale`, `nvcrCity`, `nvcrState`, `nvcrCountry`, `nvcrDailyRate`, `Rcode`, `nvcrTax`, `nvcrRoomType`, `nvcrRoomCode`, `nvcrCancellationPolicy`, `StarRating`, `nvcrstar`, `nvcrPrice`, `nvcrCurrency`, `nvcrBreakFast`, `nvcrAvailability`, `nvcrBoard`, `nvcrStatus`,`intBatchCrawlDataFinalId`,`intBatchId`,`MasterID`) VALUES ('HotelBeds', '2', 'TAJ', '101', 'NO', 'Mumbai', 'MAH', 'INDIA', '2.6', 'RO', '1.6', 'BO', 'RO', 'NO', 'YES', '3', '2.5', 'INR', 'NO', 'YES', 'BO', 'PASS',1003,8,7778);
INSERT INTO `eCube_Centralized_DB`.`BatchCrawlDatafinal_ECUBE_MDM_5` (`nvcrCompany`, `Nights`, `nvcrHotel`, `HotelId`, `nvcrPointOfSale`, `nvcrCity`, `nvcrState`, `nvcrCountry`, `nvcrDailyRate`, `Rcode`, `nvcrTax`, `nvcrRoomType`, `nvcrRoomCode`, `nvcrCancellationPolicy`, `StarRating`, `nvcrstar`, `nvcrPrice`, `nvcrCurrency`, `nvcrBreakFast`, `nvcrAvailability`, `nvcrBoard`, `nvcrStatus`,`intBatchCrawlDataFinalId`,`intBatchId`,`MasterID`) VALUES ('HotelBeds', '2', 'TAJ', '101', 'NO', 'Mumbai', 'MAH', 'INDIA', '2.6', 'RO', '1.6', 'BO', 'RO', 'NO', 'YES', '3', '2.5', 'INR', 'NO', 'YES', 'BO', 'PASS',1004,8,7778);

/*
IN v_intBatchId int,
IN dipbagid int,
IN mdmflag1 INT,
IN v_nvcrSupplierID nvarchar(50)

*/
END ;;
