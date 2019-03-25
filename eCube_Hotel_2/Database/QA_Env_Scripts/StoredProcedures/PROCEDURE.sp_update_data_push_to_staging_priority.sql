DELIMITER ;;

CREATE PROCEDURE `sp_update_data_push_to_staging_priority`(

In req_id bigint(20),
In val bool,
In p_UserId	int
)
BEGIN
	
   update MDM_Batches set `bitpriority` = val where `intMDM_BatchesId` = req_id;
END ;;
