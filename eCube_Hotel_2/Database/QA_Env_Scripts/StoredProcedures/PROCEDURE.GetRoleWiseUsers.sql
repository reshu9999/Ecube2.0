DELIMITER ;;

CREATE PROCEDURE `GetRoleWiseUsers`(IN UserId INT)
BEGIN
Select RAM.Roles_Access_Id, RM.RoleName from tbl_UserMaster UM
	inner join tbl_RolesAccessMapping RAM
	on RAM.Roles_Id = UM.UM_RoleId
	inner join tbl_RoleMaster RM
	on RM.RoleId = RAM.Roles_Access_Id
	where UM.UserId=UserId and UM.Active =1 and RM.Active=1 and RAM.Active=1;
    
END ;;
