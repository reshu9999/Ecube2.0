DELIMITER ;;

CREATE PROCEDURE `Batch_SuccesFullExecution_ECUBE_MDM_5`(
	p_intBatchId INT /* = 0 */
	,p_intBatchStatus INT
	)
ThisSP:BEGIN

	DECLARE v_vcrstatus VARCHAR(20);
	DECLARE p_intSourceMDM_BatchesId int ;
    Declare v_intstatusid Int Default 0;
   
	DECLARE v_ID INT DEFAULT (
			SELECT MAX(intMDM_BatchesId)
			FROM MDM_Batches_MDM WHERE isComplete = 0 and IntWorkFlowID=5 -- intStatusId in (7,8,9,10) and 
			); 
	-- If no batch then stop storedp procedure execution
	
	IF v_ID = null THEN
	 LEAVE ThisSP;
     end if;
     
	 Set  p_intSourceMDM_BatchesId  = (
			SELECT intSourceMDM_BatchesId -- -6293
			FROM MDM_Batches_MDM
			WHERE intMDM_BatchesId = v_ID
			and IntWorkFlowID=5
			);

	UPDATE MDM_Batches_MDM
	SET intStatusId = CASE 
			WHEN p_intBatchStatus = 103
				THEN CASE 
						WHEN intStatusId = 7
							THEN 3
						WHEN intStatusId = 8
							THEN 11 -- Manual Upload Complete 
						WHEN intStatusId = 9
							THEN 9 -- No Data Found
						WHEN intStatusId = 10
							THEN 10 -- Error in Data
						END
			WHEN p_intBatchStatus = 105
				THEN 2
			END
		,dtmUpdateDate = NOW()
		,isComplete = 1
		WHERE intMDM_BatchesId = v_ID -- intBatchId = @intBatchId
		and IntWorkFlowID=5;

      
	Set  v_intstatusid = (select intstatusid
			FROM MDM_Batches_MDM
			WHERE intMDM_BatchesId = v_ID
			and IntWorkFlowID=5);

	
    
    UPDATE MDM_Batches_MDM
	SET intStatusId = v_intstatusid
	WHERE intMDM_BatchesId = @intSourceMDM_BatchesId
	and IntWorkFlowID=5;

	SET v_vcrstatus = (
			SELECT CASE 
					WHEN intStatusId = 3
						THEN 'Success'
					WHEN intStatusId = 2
						THEN 'Fail'
					WHEN intStatusId = 11
						THEN 'ManualUpload'
					WHEN intStatusId = 9
						THEN 'NoData'
					WHEN intStatusId = 10
						THEN 'ERROR'
					END
			FROM MDM_Batches_MDM
			WHERE intMDM_BatchesId = v_ID
			and IntWorkFlowID=5
			);
		
		
     /*IMP this call in service nneed uncomment
	CALL SendMail_ECUBE_MDM_5 v_intMDM_BatchesId; = v_ID
		,v_vcrstatus = v_vcrstatus

*/

   /* IMP this call in service
CALL SendMail_Hotel_Count_ECUBE_MDM_5 v_intMDM_BatchesId; = v_ID
	,v_vcrstatus = v_vcrstatus
	
	*/

	-- CALL ChangeStatusAfterEmail (p_intMDM_BatchesId = v_ID,p_intSourceMDM_BatchesId = p_intSourceMDM_BatchesId);
	
END ;;
