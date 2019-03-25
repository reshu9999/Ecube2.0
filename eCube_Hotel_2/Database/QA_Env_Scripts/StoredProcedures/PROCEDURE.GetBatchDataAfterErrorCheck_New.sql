DELIMITER ;;

CREATE PROCEDURE `GetBatchDataAfterErrorCheck_New`(
 In abc int
,IN v_intDipBagDynamicId int 
, In supplier varchar(50) )
BEGIN
select * from TempQA_ECUBE_MDM_5;
END ;;
