DELIMITER ;;

CREATE PROCEDURE `GetMultiBatchReportsData`(
In BLIId Int,
In userId varchar(500),
In groupId Int,
In requestId varchar(1000)
)
BEGIN

	SELECT 
	rd.RequestRunId,
	Concat(rm.RequestName ,'-', rm.RequestId) as requestName,  
	um.UserName,
	Date_Format(rd.EndDateTime,'%Y-%m-%d') as EndDateTime,
	gm.GroupName
	from eCube_Centralized_DB.tbl_RequestMaster rm 
		inner join eCube_Centralized_DB.tbl_RequestRunDetail rd 
			on rm.RequestId = rd.FK_RequestId 
		inner join eCube_Centralized_DB.tbl_UserMaster um
			on rm.CreatedBy = um.userId 
		inner join eCube_Centralized_DB.tbl_Field_Group_Master gm
			on gm.FGM_UserId = um.userId    
	where  
	um.Active = 1 and
	gm.Active = 1 and
	um.UM_BliId=BLIId and
	gm.GroupID = groupId and
	FIND_IN_SET(um.userId,userId) and 
	FIND_IN_SET(rm.RequestId,requestId);
END ;;
