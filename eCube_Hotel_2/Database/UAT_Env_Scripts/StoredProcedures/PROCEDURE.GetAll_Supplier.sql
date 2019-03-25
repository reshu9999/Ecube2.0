DELIMITER ;;

CREATE PROCEDURE `GetAll_Supplier`()
BEGIN
SELECT intSupplierId
      ,nvcrSupplierName
      ,nvcrSupplierURL
      ,intSupplierScriptId
      ,nvcrSupplierUserName
      ,nvcrSupplierPassword
      ,bitSupplierStatus
      ,nvcrSupplierAccNo
      ,nvcrSupplierCode
      ,nvcrDisplaySupplierName
  FROM MSTSupplier;
  
END ;;
