DELIMITER ;;

CREATE PROCEDURE `GetTableData_Hotel_Avail_DETAIL_R_2_FINAL_Y`(
    p_intBatchId  INT 
	,p_vcrBatchName VARCHAR(500)
	,p_sdtmDiPBagDynamicRecordDT VARCHAR(50)
	,p_Status VARCHAR(50)
	,p_intDipBagDynamicId INT
	,p_intSourceMDM_BatchesId INT
	,p_dtmTimestamp VARCHAR(50)
    ,p_bitRenameFlag tinyint
    ,p_nvcrSupplierID NVARCHAR (500)
    ,p_BitIsPNFStopper NVARCHAR(50)      
    ,p_intpartialuploadid int       
    ,p_intDetailsReport int
	)
BEGIN
		
        
        
        declare p_FileName nvarchar(50);
		DECLARE v_id INT;
		DECLARE v_Start VARCHAR(50) DEFAULT 'Start';
		DECLARE v_Stop VARCHAR(50) DEFAULT 'Stop'; -- ------------------Yogesh
		Declare v_Continue varchar (50) Default 'Continue'; -- -----Yogesh
		DECLARE v_intStatusId INT DEFAULT 6; -- - statusid  6 for Started
		-- DECLARE v_DipbagDynamicDT DATETIME(3) DEFAULT LEFT(p_sdtmDiPBagDynamicRecordDT, CHARINDEX('.', p_sdtmDiPBagDynamicRecordDT) - 1);

		IF p_Status = 8 THEN -- Manually Update 
			SET v_intStatusId = p_Status;
		END IF;
		
		-- select p_bitRenameFlag;
		-- SET v_id = LAST_INSERT_ID();
		

		UPDATE MDM_Batches_Hotel_Avail	SET `intstatusDETAIL_R` = 7 WHERE intMDM_BatchesId = v_id and IntWorkFlowID=2;
	
		-- TRUNCATE TABLE `BatchCrawlDatafinal_Hotel_Avail_DETAIL_R_2`;
		        
         CALL sp_DetailsSection(p_intDipBagDynamicId,p_intBatchId,p_intSourceMDM_BatchesId,p_vcrBatchName); -- (v_intDipBagDynamicId);
				
		set p_FileName = '' ;


		IF p_bitRenameFlag = 0
		then
		-- SET p_FileName = CONCAT(CONVERT(VARCHAR, p_intBatchId) , '_' concat(p_vcrBatchName , '_') , concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'), + case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as varchar(1)) end , '.xls');
	SET p_FileName = Concat(CAST(p_intBatchId As unsigned) , '_'  ,concat(p_vcrBatchName , '_') ,concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  concat( case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as unsigned) end) ,concat( '.xls')));	
	-- SET p_FileName = Concat(CAST(p_intBatchId As unsigned) , '_' , concat(cast(p_intSourceMDM_BatchesId As unsigned)),  '_' ,concat(p_vcrBatchName , '_') ,concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  concat( case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as unsigned) end) ,concat( '.csv')));	
    ELSE
	SET p_FileName = Concat(CAST(p_intBatchId As unsigned) , '_'  ,concat(p_vcrBatchName , '_') ,concat( Date_Format(now(),'%d%M%y'), time_format(now(),'%H%i%s'),  concat( case p_intpartialuploadid when 0 then '' else cast(p_intpartialuploadid as unsigned) end) ,concat( '.xls')));	

 
 
		 end if; 


   
	
		IF NOT EXISTS (
				SELECT *
				FROM BatchCrawlDatafinal_Hotel_Avail_DETAIL_R_2
				)
		THEN
		 UPDATE MDM_Batches_Hotel_Avail	SET `intstatusDETAIL_R` = 9	WHERE intMDM_BatchesId = 1 and IntWorkFlowID=2;
		-- LEAVE sp_lbl;
		END IF;


		-- UPDATE MDM_Batches_Hotel_Avail 	SET vcrFileName = p_FileName WHERE intMDM_BatchesId = v_id and IntWorkFlowID=2;
	
/*
		UPDATE MDM_Batches_Hotel_Avail
		SET vcrFileName = (
				SELECT CONCAT(ERROR_MESSAGE() , ' Line No:' , concat(CAST( ERROR_LINE() as char)) AS ErrorNumber
				)
			,intStatusId = 10 -- for error
		WHERE intMDM_BatchesId = v_id
		and IntWorkFlowID=2 
		);
*/
	
END ;;
