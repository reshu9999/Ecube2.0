DELIMITER ;;

CREATE PROCEDURE `spGetAllFieldMaster`()
BEGIN
	    
    Select FMId,FieldName from tbl_FieldMaster where Active = 1
    and DomainTypeId = 1  order by FieldName asc;
    
    
END ;;
