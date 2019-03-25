DELIMITER ;;

CREATE PROCEDURE `sp_Save_data_push_to_staging`(

In req_id bigint(20),
In req_name varchar(50),
In prim_sup_id varchar(100),
In Sec_sup_id varchar(100),
In is_pnf int,
In Report_type varchar(10),
In p_UserId	int
)
BEGIN
	
    INSERT INTO MDM_Batches (`intBatchId`,`vcrBatchName`,`intDipBagDynamicId`,
	`intUserId`,`intStatusId`,`sintManualUpdate`,`sdtmDiPBagDynamicRecordDT`,
	`dtmCreatedDate`,`dtmUpdatedDate`,`dtmTimestamp`,`bitRenameFlag`,
	`IntWorkflowID`,`nvcrSupplierID`,`BitIsPNFStopper`,`nvcrSupplierIDExcludeSavePageUrl`,`Report_Type`)
	values (req_id,req_name,111,p_UserId,'1',0,Now(),Now(),Now(),Now(),0,0,prim_sup_id,is_pnf,Sec_sup_id,Report_type);

END ;;
