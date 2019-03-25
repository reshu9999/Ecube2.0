DELIMITER ;;

CREATE PROCEDURE `ChangeStatusAfterEmail`(
	p_intMDM_BatchesId int,
	p_intSourceMDM_BatchesId int
)
BEGIN
  	declare v_intStatusId int default 0; 

	UPDATE MDM_Batches_MDM SET intStatusId =  CASE WHEN intStatusId = 3 THEN  4 
											   WHEN intStatusId = 2 THEN  5 
											   WHEN intStatusId = 6 THEN  7
											   ELSE intStatusId END 
											   WHERE intMDM_BatchesId=p_intMDM_BatchesId
											   and IntWorkFlowID=5;
		
		
		
		
		
		
				set v_intStatusId =  (select intStatusId
			FROM MDM_Batches
			WHERE intMDM_BatchesId = p_intMDM_BatchesId
			and IntWorkFlowID=5	);								   

	
											   	
	UPDATE MDM_Batches
	SET intStatusId = v_intStatusId,
	sintManualUpdate =  v_intStatusId,
	sdtmReportEndDateTime = now()
	WHERE intMDM_BatchesId = p_intSourceMDM_BatchesId
	and IntWorkFlowID=5;
END ;;
