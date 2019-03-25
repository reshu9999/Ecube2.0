DELIMITER ;;

CREATE PROCEDURE `GetRequestStatusCount`(
IN fromdate datetime ,
IN todate  datetime ,
OUT runningCount varchar(100),
OUT queueCount varchar(100),
OUT completeCount varchar(100),
OUT stopCount varchar(100),
OUT pauseCount varchar(100),
OUT scheduledCount varchar(100),
IN UId int,
IN bliid int)
BEGIN
/*******************************************************************         
'	Name					: GetRequestStatusCount
'	Desc					: To 
'	Called by				: 
'	Example of execution	: 
INPUT PARAMETRS		 	 
	fromdate datetime ,
	todate  datetime ,
	UId int,
	bliid int
Retruns 
	runningCount varchar(100),
	queueCount varchar(100),
	completeCount varchar(100),
	stopCount varchar(100),
	pauseCount varchar(100),
	scheduledCount varchar(100),

'	Created by				: 
'	Date of creation		: 

******************************************************************************************************
Change History
******************************************************************************************************
Sr.No.		Date:			Changed by:			Description:
1			11-Jun-2018		Bhavin.Dhimmar		Add new input parameter bliid
******************************************************************************************************/	
	SELECT count(StartDatetIme) INTO runningCount 
	FROM eCube_Centralized_DB.tbl_RequestRunDetail A
	join tbl_RequestMaster B on (A.FK_RequestId=B.RequestId)
	where date_format(StartDatetIme,'%Y-%m-%d')between fromdate and todate
	and A.FK_StatusId IN (1,5,11,13,14,10,9)
	and B.CreatedBy=UId
	and B.FK_BLIId = bliid;


	SELECT count(StartDatetIme) INTO completeCount FROM eCube_Centralized_DB.tbl_RequestRunDetail A
	join tbl_RequestMaster B on (A.FK_RequestId=B.RequestId)
	where date_format(StartDatetIme,'%Y-%m-%d') between fromdate and todate
	and A.FK_StatusId = 2
	and B.CreatedBy=UId
	and B.FK_BLIId = bliid;


	SELECT count(StartDatetIme) INTO stopCount FROM eCube_Centralized_DB.tbl_RequestRunDetail A
	join tbl_RequestMaster B on (A.FK_RequestId=B.RequestId)
	where date_format(StartDatetIme,'%Y-%m-%d') between fromdate and todate
	and A.FK_StatusId = 6 and B.CreatedBy=UId
	and B.FK_BLIId = bliid;

	SELECT count(StartDatetIme) INTO queueCount FROM eCube_Centralized_DB.tbl_RequestRunDetail A
	join tbl_RequestMaster B on (A.FK_RequestId=B.RequestId)
	where date_format(StartDatetIme,'%Y-%m-%d') between fromdate and todate
	and A.FK_StatusId = 3 and B.CreatedBy=UId
	and B.FK_BLIId = bliid;

	SELECT count(StartDatetIme) INTO pauseCount  FROM eCube_Centralized_DB.tbl_RequestRunDetail A
	join tbl_RequestMaster B on (A.FK_RequestId=B.RequestId)
	where date_format(StartDatetIme,'%Y-%m-%d') between fromdate and todate
	and A.FK_StatusId = 7 and B.CreatedBy=UId
	and B.FK_BLIId = bliid;

	/*select Count(*)  INTO scheduledCount  FROM eCube_Centralized_DB.tbl_ScheduleDate
	where ScheduleDate = curdate() and ScheduleTime > current_time()+1 and Status = 1
	and date_format(ScheduleDate,'%Y-%m-%d') between fromdate and todate;*/

	select Count(distinct SD_RequestId) INTO scheduledCount 
	FROM eCube_Centralized_DB.tbl_ScheduleDate  A
	join tbl_RequestMaster B on (A.SD_RequestId=B.RequestId)
	where date_format(ScheduleDate,'%Y-%m-%d') between fromdate and todate
	and B.CreatedBy=UId
	and B.FK_BLIId = bliid;

END ;;
