DELIMITER ;;

CREATE PROCEDURE `LastResult_Avail`(
p_intBatchId int ,
p_id int,
p_id1 int,
p_supplier_id nvarchar(50)
)
BEGIN
INSERT INTO `eCube_Centralized_DB`.`BatchCrawlDatafinal_Hotel_Avail_Last_R_SEC` (`nvcrCompany`, `Nights`, `nvcrHotel`, `HotelId`, `nvcrPointOfSale`, `nvcrCity`, `nvcrState`, `nvcrCountry`, `nvcrDailyRate`, `StarRating`, `nvcrstar`, `nvcrCurrency`,`intBatchId`,`MasterID`) VALUES ('HotelBeds_Avail', '2', 'TAJ', '101', 'UK', 'London', 'MH', 'IN', '2.0', 'Yes', '3', 'INR',10431,1111);
END ;;
