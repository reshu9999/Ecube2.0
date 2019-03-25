DELIMITER ;;

CREATE PROCEDURE `GetCrawlDataMapper`(
IN requestId int(11)
)
BEGIN
Declare groupId int(11);
Select FK_GroupId INTO groupId from tbl_RequestMaster where RequestId = requestId; -- order by 1 DESC NOT Requered LIMIT 1;


Select t3. GroupName, t2.FieldName, t1.TextBoxValue, t1.DataType  
from tbl_FieldGroupMappingDetails t1, tbl_FieldMaster t2, tbl_Field_Group_Master t3 
where t1.FGMD_FieldId = t2.FMId 
And t3.GroupID = t1.FGMD_GroupID 
And t1.FGMD_GroupID = groupId;

END ;;
