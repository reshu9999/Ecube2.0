DELIMITER ;;

CREATE FUNCTION `fn_GetSupplierID`(
    varSupplier1 varchar(100),
    varSupplier2 varchar(100),
    varSupplier3 varchar(100),
    varSupplier4 varchar(100),
    varSupplier5 varchar(100),
    varSupplier6 varchar(100),
    varSupplier7 varchar(100),
    varSupplier8 varchar(100),
    varSupplier9 varchar(100),
    varSupplier10 varchar(100),
    varSupplier11 varchar(100),
    varSupplier12 varchar(100),
    varSupplier13 varchar(100),
    varSupplier14 varchar(100),
    varSupplier15 varchar(100),
    varSupplier16 varchar(100),
    varSupplier17 varchar(100),
    varSupplier18 varchar(100),
    varSupplier19 varchar(100),
    varSupplier20 varchar(100)
    
) RETURNS varchar(4000) CHARSET latin1
    DETERMINISTIC
BEGIN

Declare SupplierID Varchar(500) default '';


Select group_concat(competitorID) into SupplierID From tbl_CompetitorMaster
                Where competitorName in 
(varSupplier1, varSupplier2, varSupplier3, varSupplier4, varSupplier5,
varSupplier6, varSupplier7, varSupplier8, varSupplier9, varSupplier10,
varSupplier11, varSupplier12, varSupplier13, varSupplier14, varSupplier15,
varSupplier16, varSupplier17, varSupplier18, varSupplier19, varSupplier20)
;
                


RETURN SupplierID;

END ;;
