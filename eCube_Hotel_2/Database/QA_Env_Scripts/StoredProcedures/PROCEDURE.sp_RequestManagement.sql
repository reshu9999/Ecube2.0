DELIMITER ;;

CREATE PROCEDURE `sp_RequestManagement`()
BEGIN
    
		select distinct RequestId,RequestDescription,C.ScheduleType,'tech' As userName,A.CreatedDatetime,
		D.EndDateTime,A.NextScheduleDateTime,StatusTitle
		from tbl_RequestMaster A
		left join tbl_RequestRunDetail D on (D.FK_RequestId=A.RequestId)
		left join tbl_ScheduleMaster B on (A.RequestId=B.SM_RequestId)
		left join tbl_ScheduleTypeMaster C on (C.ShedulId=B.SM_ScheduleTypeId)
        join tbl_StatusMaster E on (E.StatusId=D.FK_StatusId)
		;
   
   
END ;;
