DELIMITER ;;

CREATE PROCEDURE `InsertCountryMaster`()
BEGIN
set foreign_key_checks = 0;

ALTER TABLE `tbl_CountryMaster` CHANGE `CountryID` `CountryID` INT( 11 )  NOT NULL;

truncate table tbl_CountryMaster;

insert into tbl_CountryMaster (CountryID,CountryName,Active,CreatedDate,CountryCode)
Select CountryID,CountryName,Active,CreatedDate,CountryCode
from ecube_Staging.tbl_CountryMaster order by CountryID;




ALTER TABLE `tbl_CountryMaster` CHANGE `CountryID` `CountryID` INT( 11 )  NOT NULL auto_increment;

SET @new_index = (SELECT MAX(CountryID) FROM tbl_CountryMaster);
SET @sql = CONCAT('ALTER TABLE tbl_CountryMaster AUTO_INCREMENT = ', @new_index);
PREPARE st FROM @sql;
EXECUTE st;


set foreign_key_checks = 1;
END ;;
