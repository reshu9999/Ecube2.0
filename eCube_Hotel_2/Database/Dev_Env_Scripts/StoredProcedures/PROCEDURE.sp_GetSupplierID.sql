DELIMITER ;;

CREATE PROCEDURE `sp_GetSupplierID`(
                IN p_SupplierName NVARCHAR(150),
                OUT p_SupplierId INT 
)
BEGIN

	SELECT Id into p_SupplierId FROM  tbl_Competitor WHERE `name` = p_SupplierName;

END ;;
