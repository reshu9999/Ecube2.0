DELIMITER ;;

CREATE PROCEDURE `spInsertFieldGroupMappingDetails`(
IN FieldID INT, 
IN dttype VARCHAR(15), 
IN TxtBoxValue VARCHAR(100),
IN User_ID INT
)
BEGIN
    declare GrpID INT;
	Select GroupID into GrpID from tbl_Field_Group_Master 
    where FGM_UserId = User_ID
    order by GroupID Desc Limit 1; 

    INSERT INTO `eCube_Centralized_DB`.`tbl_FieldGroupMappingDetails`
	(
	`TextBoxValue`,
	`DataType`,
	`FGMD_GroupID`,
	`FGMD_FieldId`,
	`CreatedDate`
	)
	VALUES
	(
	TxtBoxValue,
	dttype,
	GrpID,
	FieldID,
	NOW()
    );

END ;;
