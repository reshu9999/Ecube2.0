DELIMITER ;;

CREATE PROCEDURE `sp_get_data_push_to_staging`(


)
BEGIN
	
     select  `intMDM_BatchesId`,`intBatchId`,`vcrBatchName`,`intDipBagDynamicId`
	,case when `intStatusId` =1 then 'Pending' else 'Completed'  end as `status`,`dtmCreatedDate`,`bitpriority`,`intUserId`,`intStatusId`,`sintManualUpdate`,`sdtmDiPBagDynamicRecordDT`
	,`dtmUpdatedDate`,`dtmTimestamp`,`bitRenameFlag`,
	`IntWorkflowID`,`nvcrSupplierID`,`BitIsPNFStopper`,`nvcrSupplierIDExcludeSavePageUrl`,`Report_Type`,`sdtmReportStartDateTime`,`sdtmReportEndDateTime`
     from MDM_Batches ;
	

END ;;
