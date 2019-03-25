DELIMITER ;;

CREATE PROCEDURE `MatchingTest`(
in supplierID Int(11),
HotelId Varchar(500)
)
BEGIN

SELECT * FROM eCube_Centralized_DB.HotelMatching;
END ;;
