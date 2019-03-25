DELIMITER ;;

CREATE PROCEDURE `spGetallGroupMaster`()
BEGIN
		
        Select GroupID, GroupName, GroupDesc from tbl_Field_Group_Master
        where Active = 1;
        
        
END ;;
