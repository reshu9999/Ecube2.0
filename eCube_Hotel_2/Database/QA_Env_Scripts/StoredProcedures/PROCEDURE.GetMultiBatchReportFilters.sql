DELIMITER ;;

CREATE PROCEDURE `GetMultiBatchReportFilters`(
IN BLIId Int)
BEGIN

	SELECT UserId,username FROM tbl_UserMaster 
	where UM_BliId=BLIId and Active=1;

	SELECT groupID,GroupName FROM 
	tbl_Field_Group_Master gm join tbl_UserMaster um
	on gm.FGM_UserId = um.userId
	where gm.Active = 1 
	and um.Active = 1 and um.UM_BliId=BLIId;

	SELECT rm.RequestId,Concat(rm.RequestName ,'-', rm.RequestId) as requestName
	from tbl_RequestMaster rm join tbl_UserMaster um
	on rm.CreatedBy = um.userId
	where um.Active = 1 and um.UM_BliId=BLIId;


END ;;
