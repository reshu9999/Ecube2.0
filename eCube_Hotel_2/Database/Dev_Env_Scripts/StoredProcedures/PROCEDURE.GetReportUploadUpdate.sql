DELIMITER ;;

CREATE PROCEDURE `GetReportUploadUpdate`(
v_intBatchId int ,v_intDipBagDynamicId int,v_nvcrSupplierID nvarchar(50))
BEGIN
select * from TempQAStop_ECUBE_MDM_5;

END ;;
