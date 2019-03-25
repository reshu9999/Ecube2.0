DELIMITER ;;

CREATE PROCEDURE `GetUserMenus`(IN UserId INT)
BEGIN
SELECT item.Accessitems FROM tbl_AccessItemsMaster item
	inner join tbl_UserMenuAccessMappings useraccess 
    on useraccess.AccessItem_Id = item.Id
	where useraccess.User_Id =  UserId and useraccess.active=1;
END ;;
