DELIMITER ;;

CREATE PROCEDURE `spInsertGroupMaster`(
IN GrpName VARCHAR(50), 
IN GrpDesc VARCHAR(50), 
IN User_ID INT,
IN ReqID INT)
BEGIN

	declare gID INT;
    
	INSERT INTO `tbl_Field_Group_Master`
	(
	`GroupName`,
	`Active`,
	`FGM_UserId`,
	`CreatedDate`,
	`GroupDesc`)
	VALUES
	(	
		GrpName,
		1,
		User_ID,
		NOW(),
		GrpDesc
	);
    
    select GroupID into gID from tbl_Field_Group_Master where Active = 1
    order by GroupID  desc limit 1;
    
    Update tbl_RequestMaster 
    SET FK_GroupId = gID
    where requestId = ReqID;
	

END ;;
