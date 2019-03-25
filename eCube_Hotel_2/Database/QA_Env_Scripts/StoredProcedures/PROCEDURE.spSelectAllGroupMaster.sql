DELIMITER ;;

CREATE PROCEDURE `spSelectAllGroupMaster`()
BEGIN

	Select GroupID, GroupName from tbl_Field_Group_Master 
    where Active = 1;

	
END ;;
