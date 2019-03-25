DELIMITER ;;

CREATE PROCEDURE `GetTableData_ECUBE_MDM_5_WithOUT_Linktest`(OUT p_intBatchId  INT )
BEGIN
set p_intBatchId =101 ;
select * from Hotels;
END ;;
