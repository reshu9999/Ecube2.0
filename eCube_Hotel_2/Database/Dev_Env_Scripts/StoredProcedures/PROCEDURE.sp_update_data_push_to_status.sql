DELIMITER ;;

CREATE PROCEDURE `sp_update_data_push_to_status`(

In req_id varchar(200),
In p_UserId	int
)
BEGIN
	
   call sp_split(req_id,','); 
   
   update MDM_Batches set `intStatusId` = 10 where `intMDM_BatchesId` in(
	Select items From SplitValue
   ) ;
END ;;
