DELIMITER ;;

CREATE PROCEDURE `spGetAllUsers`()
BEGIN
	
    
    Select FirstName, LastName, UserName, RoleName, RM.Active from 
    tbl_UserMaster UM
    inner join 
    tbl_RoleMaster RM on UM.UM_RoleID = RM.roleid
    where RM.Active = 1;
END ;;
