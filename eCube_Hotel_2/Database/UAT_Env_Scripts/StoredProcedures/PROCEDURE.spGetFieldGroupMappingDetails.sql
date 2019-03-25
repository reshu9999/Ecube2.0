DELIMITER ;;

CREATE PROCEDURE `spGetFieldGroupMappingDetails`(IN GrpID INT)
BEGIN
	
    

	
SELECT FM.FieldName, FGMD.TextBoxValue,FGM.GroupName, FGM.GroupDesc  FROM tbl_FieldGroupMappingDetails FGMD
INNER JOIN tbl_Field_Group_Master FGM
ON FGMD.FGMD_GroupID = FGM.GroupID
INNER JOIN tbl_FieldMaster FM
ON FGMD_FieldId = FM.FMId
where FGMD_GroupID = GrpID;
    
    

END ;;
