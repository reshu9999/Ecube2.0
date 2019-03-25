DELIMITER ;;

CREATE PROCEDURE `InsertSupplierMaster`()
BEGIN
set foreign_key_checks = 0;

ALTER TABLE `MSTSupplier` CHANGE `intSupplierId` `intSupplierId` INT( 11 )  NOT NULL;

truncate table MSTSupplier;

insert into MSTSupplier (intSupplierId,nvcrSupplierName,nvcrSupplierURL,intSupplierScriptId,nvcrSupplierUserName,nvcrSupplierPassword,bitSupplierStatus,nvcrSupplierAccNo,nvcrSupplierCode,nvcrDisplaySupplierName)
Select intSupplierId,nvcrSupplierName,nvcrSupplierURL,intSupplierScriptId,nvcrSupplierUserName,nvcrSupplierPassword,bitSupplierStatus,nvcrSupplierAccNo,nvcrSupplierCode,nvcrDisplaySupplierName
from ecube_Staging.MSTSupplier order by intSupplierId;




ALTER TABLE `MSTSupplier` CHANGE `intSupplierId` `intSupplierId` INT( 11 )  NOT NULL auto_increment;

SET @new_index = (SELECT MAX(intSupplierId) FROM MSTSupplier);
SET @sql = CONCAT('ALTER TABLE MSTSupplier AUTO_INCREMENT = ', @new_index);
PREPARE st FROM @sql;
EXECUTE st;


set foreign_key_checks = 1;
END ;;
