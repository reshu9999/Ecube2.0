DELIMITER ;;

CREATE PROCEDURE `sp_FilterReqManagementbystatus`(

IN ReqStatus varchar(100),
IN user_Id int
)
BEGIN


		if ReqStatus='Running' then
            
				select distinct RequestRunId As requestrunid,RequestId,RequestName as RequestTitle,RequestDescription,
				case when A.FK_ScheduleTypeId=1 then 'Daily' when A.FK_ScheduleTypeId=2 then 'Monthly' when A.FK_ScheduleTypeId=3 then 'Weekly'
				when A.FK_ScheduleTypeId=4 then 'Once' else 'One Time' end AS ScheduleType,
				CONCAT(FirstName," ",LastName) As userName,A.CreatedDatetime,
				D.EndDateTime,TotalRequests AS TR,CompletedRequests As Completed,PNFCounts As PNF,
				Case when (D.FK_StatusId=1 OR D.FK_StatusId=5 OR D.FK_StatusId=13 OR D.FK_StatusId=14 OR D.FK_StatusId=10 OR D.FK_StatusId=9) then 'Running' when D.FK_StatusId=2 then 'Completed' when D.FK_StatusId=3 then 'InQue' end  As
				Status,ROUND(((CompletedRequests+PNFCounts)/TotalRequests)*100,0) AS Percent,ReportDownloadLink
				from tbl_RequestMaster A
				left join tbl_RequestRunDetail D on (D.FK_RequestId=A.RequestId)
				left join tbl_ScheduleMaster B on (A.RequestId=B.SM_RequestId)
				left join tbl_ScheduleTypeMaster C on (C.ShedulId=A.FK_ScheduleTypeId)
				left join tbl_StatusMaster E on (E.StatusId=D.FK_StatusId)
				join tbl_UserMaster U on (U.UserId=A.CreatedBy)
				where D.FK_StatusId in(1,5,11,13,14,9,10) 				
                and U.UserId=user_Id
				order by A.RequestId desc ; 
                
            elseif ReqStatus='Completed' then

				select distinct RequestRunId As requestrunid,RequestId,RequestName as RequestTitle,RequestDescription,
				case when A.FK_ScheduleTypeId=1 then 'Daily' when A.FK_ScheduleTypeId=2 then 'Monthly' when A.FK_ScheduleTypeId=3 then 'Weekly'
				when A.FK_ScheduleTypeId=4 then 'Once' else 'One Time' end AS ScheduleType,
				CONCAT(FirstName," ",LastName) As userName,A.CreatedDatetime,
				D.EndDateTime,TotalRequests AS TR,CompletedRequests As Completed,PNFCounts As PNF,
				Case when (D.FK_StatusId=1 OR D.FK_StatusId=5 OR D.FK_StatusId=13 OR D.FK_StatusId=14 OR D.FK_StatusId=10 OR D.FK_StatusId=9) then 'Running' when D.FK_StatusId=2 then 'Completed' when D.FK_StatusId=3 then 'InQue' end  As
				Status,ROUND(((CompletedRequests+PNFCounts)/TotalRequests)*100,0) AS Percent,ReportDownloadLink
				from tbl_RequestMaster A
				left join tbl_RequestRunDetail D on (D.FK_RequestId=A.RequestId)
				left join tbl_ScheduleMaster B on (A.RequestId=B.SM_RequestId)
				left join tbl_ScheduleTypeMaster C on (C.ShedulId=A.FK_ScheduleTypeId)
				left join tbl_StatusMaster E on (E.StatusId=D.FK_StatusId)
				join tbl_UserMaster U on (U.UserId=A.CreatedBy)
				where  D.FK_StatusId in(2)
                and U.UserId=user_Id
				order by A.RequestId desc ;  
                
            elseif ReqStatus='InQue' then
            
				select distinct RequestRunId As requestrunid,RequestId,RequestName as RequestTitle,RequestDescription,
				case when A.FK_ScheduleTypeId=1 then 'Daily' when A.FK_ScheduleTypeId=2 then 'Monthly' when A.FK_ScheduleTypeId=3 then 'Weekly'
				when A.FK_ScheduleTypeId=4 then 'Once' else 'One Time' end AS ScheduleType,
				CONCAT(FirstName," ",LastName) As userName,A.CreatedDatetime,
				D.EndDateTime,TotalRequests AS TR,CompletedRequests As Completed,PNFCounts As PNF,
				Case when (D.FK_StatusId=1 OR D.FK_StatusId=5 OR D.FK_StatusId=13 OR D.FK_StatusId=14 OR D.FK_StatusId=10 OR D.FK_StatusId=9) then 'Running' when D.FK_StatusId=2 then 'Completed' when D.FK_StatusId=3 then 'InQue' end  As
				Status,ROUND(((CompletedRequests+PNFCounts)/TotalRequests)*100,0) AS Percent,ReportDownloadLink
				from tbl_RequestMaster A
				left join tbl_RequestRunDetail D on (D.FK_RequestId=A.RequestId)
				left join tbl_ScheduleMaster B on (A.RequestId=B.SM_RequestId)
				left join tbl_ScheduleTypeMaster C on (C.ShedulId=A.FK_ScheduleTypeId)
				left join tbl_StatusMaster E on (E.StatusId=D.FK_StatusId)
				join tbl_UserMaster U on (U.UserId=A.CreatedBy)
				where D.FK_StatusId in(3)
                and U.UserId=user_Id
				order by A.RequestId desc ;  
			elseif ReqStatus='Scheduled' then
           
				select distinct RequestRunId As requestrunid,RequestId,RequestName as RequestTitle,RequestDescription,
				case when A.FK_ScheduleTypeId=1 then 'Daily' when A.FK_ScheduleTypeId=2 then 'Monthly' when A.FK_ScheduleTypeId=3 then 'Weekly'
				when A.FK_ScheduleTypeId=4 then 'Once' else 'One Time' end AS ScheduleType,
				CONCAT(FirstName," ",LastName) As userName,A.CreatedDatetime,
				D.EndDateTime,TotalRequests AS TR,CompletedRequests As Completed,PNFCounts As PNF,
				Case when (D.FK_StatusId=1 OR D.FK_StatusId=5 OR D.FK_StatusId=13 OR D.FK_StatusId=14 OR D.FK_StatusId=10 OR D.FK_StatusId=9) then 'Running' when D.FK_StatusId=2 then 'Completed' when D.FK_StatusId=3 then 'InQue' end  As
				Status,ROUND(((CompletedRequests+PNFCounts)/TotalRequests)*100,0) AS Percent,ReportDownloadLink
				from tbl_RequestMaster A
				left join tbl_RequestRunDetail D on (D.FK_RequestId=A.RequestId)
				join tbl_ScheduleDate ts on (ts.SD_RequestId=A.RequestId)	
				join tbl_UserMaster U on (U.UserId=A.CreatedBy)						
                where U.UserId=user_Id
				order by A.RequestId desc ;  
			else
				select distinct RequestRunId As requestrunid,RequestId,RequestName as RequestTitle,RequestDescription,
				case when A.FK_ScheduleTypeId=1 then 'Daily' when A.FK_ScheduleTypeId=2 then 'Monthly' when A.FK_ScheduleTypeId=3 then 'Weekly'
				when A.FK_ScheduleTypeId=4 then 'Once' else 'One Time' end AS ScheduleType,
				CONCAT(FirstName," ",LastName) As userName,A.CreatedDatetime,
				D.EndDateTime,TotalRequests AS TR,CompletedRequests As Completed,PNFCounts As PNF,
				Case when (D.FK_StatusId=1 OR D.FK_StatusId=5 OR D.FK_StatusId=13 OR D.FK_StatusId=14 OR D.FK_StatusId=10 OR D.FK_StatusId=9) then 'Running' when D.FK_StatusId=2 then 'Completed' when D.FK_StatusId=3 then 'InQue' end  As
				Status,ROUND(((CompletedRequests+PNFCounts)/TotalRequests)*100,0) AS Percent,ReportDownloadLink
				from tbl_RequestMaster A
				left join tbl_RequestRunDetail D on (D.FK_RequestId=A.RequestId)
				left join tbl_ScheduleMaster B on (A.RequestId=B.SM_RequestId)
				left join tbl_ScheduleTypeMaster C on (C.ShedulId=A.FK_ScheduleTypeId)
				left join tbl_StatusMaster E on (E.StatusId=D.FK_StatusId)
				join tbl_UserMaster U on (U.UserId=A.CreatedBy)		
                where U.UserId=user_Id
				order by A.RequestId desc ;  

			end if;
	

END ;;
