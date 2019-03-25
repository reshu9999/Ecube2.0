DELIMITER ;;

CREATE PROCEDURE `sp_SearchRequestManagement`(
 	IN RequestNo INT,
    IN RequestDesc varchar(1000),
    IN RequestFromDate datetime,
    IN RequestToDate datetime,
    IN FromNextScheduleDate datetime,
    IN TONextScheduleDate datetime,
    IN FromCompletionDate datetime,
    IN ToCompletionDate datetime,
    IN ReqStatus Varchar(100),
    IN Fetchall int,
    IN user_Id INT
)
BEGIN
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ;
	
    IF Fetchall=1 THEN
			
            IF user_Id=1 then
		
				select distinct RequestRunId As requestrunid,RequestId,RequestName as RequestTitle,RequestDescription,
				case when A.FK_ScheduleTypeId=1 then 'Daily' when A.FK_ScheduleTypeId=2 then 'Monthly' when A.FK_ScheduleTypeId=3 then 'Weekly'
				when A.FK_ScheduleTypeId=4 then 'Once' else 'One Time' end AS ScheduleType,
				CONCAT(FirstName," ",LastName) As userName,A.CreatedDatetime,
				D.EndDateTime,TotalRequests AS TR,CompletedRequests As Completed,PNFCounts As PNF,
				Case when (D.FK_StatusId=1 OR D.FK_StatusId=5 OR D.FK_StatusId=13 OR D.FK_StatusId=14 OR D.FK_StatusId=10 OR D.FK_StatusId=9) then 'Running' when D.FK_StatusId=2 then 'Completed' when D.FK_StatusId=3 then 'InQue' when D.FK_StatusId=7 then 'Paused' end  As
				Status,ROUND(((CompletedRequests+PNFCounts)/TotalRequests)*100,0) AS Percent,ReportDownloadLink
				from tbl_RequestMaster A
				left join tbl_RequestRunDetail D on (D.FK_RequestId=A.RequestId)
				left join tbl_StatusMaster E on (E.StatusId=D.FK_StatusId)
				left join tbl_ScheduleDate F on (F.SD_RequestId=A.RequestId)
				join tbl_UserMaster U on (U.UserId=A.CreatedBy)
				where U.UserId=user_Id
				and (D.FK_RequestId=A.RequestId OR F.SD_RequestId=A.RequestId)
				order by A.RequestId desc ;
			else
				select distinct RequestRunId As requestrunid,RequestId,RequestName as RequestTitle,RequestDescription,
				case when A.FK_ScheduleTypeId=1 then 'Daily' when A.FK_ScheduleTypeId=2 then 'Monthly' when A.FK_ScheduleTypeId=3 then 'Weekly'
				when A.FK_ScheduleTypeId=4 then 'Once' else 'One Time' end AS ScheduleType,
				CONCAT(FirstName," ",LastName) As userName,A.CreatedDatetime,
				D.EndDateTime,TotalRequests AS TR,CompletedRequests As Completed,PNFCounts As PNF,
				Case when (D.FK_StatusId=1 OR D.FK_StatusId=5 OR D.FK_StatusId=13 OR D.FK_StatusId=14 OR D.FK_StatusId=10 OR D.FK_StatusId=9) then 'Running' when D.FK_StatusId=2 then 'Completed' when D.FK_StatusId=3 then 'InQue' when D.FK_StatusId=7 then 'Paused' end  As
				Status,ROUND(((CompletedRequests+PNFCounts)/TotalRequests)*100,0) AS Percent,ReportDownloadLink
				from tbl_RequestMaster A
				left join tbl_RequestRunDetail D on (D.FK_RequestId=A.RequestId)
				left join tbl_StatusMaster E on (E.StatusId=D.FK_StatusId)
				left join tbl_ScheduleDate F on (F.SD_RequestId=A.RequestId)
				join tbl_UserMaster U on (U.UserId=A.CreatedBy)
				where U.UserId=user_Id
				and (D.FK_RequestId=A.RequestId OR F.SD_RequestId=A.RequestId)
				order by A.RequestId desc ;
				
            end if;

    elseif Fetchall=2  THEN
			if ReqStatus='Running' then
            
				select distinct RequestRunId As requestrunid,RequestId,RequestName as RequestTitle,RequestDescription,
				case when A.FK_ScheduleTypeId=1 then 'Daily' when A.FK_ScheduleTypeId=2 then 'Monthly' when A.FK_ScheduleTypeId=3 then 'Weekly'
				when A.FK_ScheduleTypeId=4 then 'Once' else 'One Time' end AS ScheduleType,
				CONCAT(FirstName," ",LastName) As userName,A.CreatedDatetime,
				D.EndDateTime,TotalRequests AS TR,CompletedRequests As Completed,PNFCounts As PNF,
				Case when (D.FK_StatusId=1 OR D.FK_StatusId=5 OR D.FK_StatusId=13 OR D.FK_StatusId=14 OR D.FK_StatusId=10 OR D.FK_StatusId=9) then 'Running' when D.FK_StatusId=2 then 'Completed' when D.FK_StatusId=3 then 'InQue' when D.FK_StatusId=7 then 'Paused' end  As
				Status,ROUND(((CompletedRequests+PNFCounts)/TotalRequests)*100,0) AS Percent,ReportDownloadLink
				from tbl_RequestMaster A
				left join tbl_RequestRunDetail D on (D.FK_RequestId=A.RequestId)
				left join tbl_ScheduleTypeMaster C on (C.ShedulId=A.FK_ScheduleTypeId)
				left join tbl_StatusMaster E on (E.StatusId=D.FK_StatusId)
				join tbl_UserMaster U on (U.UserId=A.CreatedBy)
				where DATE_FORMAT(D.StartDatetIme,'%Y-%m-%d') between (RequestFromDate)and (RequestToDate)
				and D.FK_StatusId in(1,5,11,13,14,10,9) 				
				and U.UserId=user_Id
                order by A.RequestId desc ; 
                
            elseif ReqStatus='Complete' then

				select distinct RequestRunId As requestrunid,RequestId,RequestName as RequestTitle,RequestDescription,
				case when A.FK_ScheduleTypeId=1 then 'Daily' when A.FK_ScheduleTypeId=2 then 'Monthly' when A.FK_ScheduleTypeId=3 then 'Weekly'
				when A.FK_ScheduleTypeId=4 then 'Once' else 'One Time' end AS ScheduleType,
				CONCAT(FirstName," ",LastName) As userName,A.CreatedDatetime,
				D.EndDateTime,TotalRequests AS TR,CompletedRequests As Completed,PNFCounts As PNF,
				Case when (D.FK_StatusId=1 OR D.FK_StatusId=5 OR D.FK_StatusId=13 OR D.FK_StatusId=14 OR D.FK_StatusId=10 OR D.FK_StatusId=9) then 'Running' when D.FK_StatusId=2 then 'Completed' when D.FK_StatusId=3 then 'InQue' when D.FK_StatusId=7 then 'Paused' end  As
				Status,ROUND(((CompletedRequests+PNFCounts)/TotalRequests)*100,0) AS Percent,ReportDownloadLink
				from tbl_RequestMaster A
				left join tbl_RequestRunDetail D on (D.FK_RequestId=A.RequestId)
				left join tbl_ScheduleTypeMaster C on (C.ShedulId=A.FK_ScheduleTypeId)
				left join tbl_StatusMaster E on (E.StatusId=D.FK_StatusId)
				join tbl_UserMaster U on (U.UserId=A.CreatedBy)
				where DATE_FORMAT(D.EndDateTime,'%Y-%m-%d') between (RequestFromDate)and (RequestToDate)
				and D.FK_StatusId in(2)
                and  U.UserId=user_Id
				order by A.RequestId desc ;  
                
            elseif ReqStatus='Inqueu' then
            
				select distinct RequestRunId As requestrunid,RequestId,RequestName as RequestTitle,RequestDescription,
				case when A.FK_ScheduleTypeId=1 then 'Daily' when A.FK_ScheduleTypeId=2 then 'Monthly' when A.FK_ScheduleTypeId=3 then 'Weekly'
				when A.FK_ScheduleTypeId=4 then 'Once' else 'One Time' end AS ScheduleType,
				CONCAT(FirstName," ",LastName) As userName,A.CreatedDatetime,
				D.EndDateTime,TotalRequests AS TR,CompletedRequests As Completed,PNFCounts As PNF,
				Case when (D.FK_StatusId=1 OR D.FK_StatusId=5 OR D.FK_StatusId=13 OR D.FK_StatusId=14 OR D.FK_StatusId=10 OR D.FK_StatusId=9) then 'Running' when D.FK_StatusId=2 then 'Completed' when D.FK_StatusId=3 then 'InQue'  when D.FK_StatusId=7 then 'Paused' end  As
				Status,ROUND(((CompletedRequests+PNFCounts)/TotalRequests)*100,0) AS Percent,ReportDownloadLink
				from tbl_RequestMaster A
				left join tbl_RequestRunDetail D on (D.FK_RequestId=A.RequestId)
				left join tbl_ScheduleTypeMaster C on (C.ShedulId=A.FK_ScheduleTypeId)
				left join tbl_StatusMaster E on (E.StatusId=D.FK_StatusId)
				join tbl_UserMaster U on (U.UserId=A.CreatedBy)
				where DATE_FORMAT(D.StartDatetIme,'%Y-%m-%d') between (RequestFromDate)and (RequestToDate)
				and D.FK_StatusId in(3) 				
                and U.UserId=user_Id
				order by A.RequestId desc ;  
			
            elseif ReqStatus='Scheduled' then
				select distinct RequestRunId As requestrunid,RequestId,RequestName as RequestTitle,RequestDescription,
				case when A.FK_ScheduleTypeId=1 then 'Daily' when A.FK_ScheduleTypeId=2 then 'Monthly' when A.FK_ScheduleTypeId=3 then 'Weekly'
				when A.FK_ScheduleTypeId=4 then 'Once' else 'One Time' end AS ScheduleType,
				CONCAT(FirstName," ",LastName) As userName,A.CreatedDatetime,
				D.EndDateTime,TotalRequests AS TR,CompletedRequests As Completed,PNFCounts As PNF,
				Case when (D.FK_StatusId=1 OR D.FK_StatusId=5 OR D.FK_StatusId=13 OR D.FK_StatusId=14 OR D.FK_StatusId=10 OR D.FK_StatusId=9) then 'Running' when D.FK_StatusId=2 then 'Completed' when D.FK_StatusId=3 then 'InQue'  when D.FK_StatusId=7 then 'Paused' end  As
				Status,ROUND(((CompletedRequests+PNFCounts)/TotalRequests)*100,0) AS Percent,ReportDownloadLink
				from tbl_RequestMaster A
				left join tbl_RequestRunDetail D on (D.FK_RequestId=A.RequestId)
				join tbl_ScheduleDate ts on (ts.SD_RequestId=A.RequestId)
				join tbl_UserMaster U on (U.UserId=A.CreatedBy)
				where 
                DATE_FORMAT(ts.ScheduleDate,'%Y-%m-%d') between (RequestFromDate)and (RequestToDate)
				and 
                U.UserId=user_Id
				order by A.RequestId desc ;  
				
			end if;
	
    elseif Fetchall=0 THEN
   	
		IF RequestNo !=0 THEN
				
				select distinct RequestRunId As requestrunid,RequestId,RequestName as RequestTitle,RequestDescription,
				case when A.FK_ScheduleTypeId=1 then 'Daily' when A.FK_ScheduleTypeId=2 then 'Monthly' when A.FK_ScheduleTypeId=3 then 'Weekly'
				when A.FK_ScheduleTypeId=4 then 'Once' else 'One Time' end AS ScheduleType,
				CONCAT(FirstName," ",LastName) As userName,A.CreatedDatetime,
				D.EndDateTime,TotalRequests AS TR,CompletedRequests As Completed,PNFCounts As PNF,
				Case when (D.FK_StatusId=1 OR D.FK_StatusId=5 OR D.FK_StatusId=13 OR D.FK_StatusId=14 OR D.FK_StatusId=10 OR D.FK_StatusId=9) then 'Running' when D.FK_StatusId=2 then 'Completed' when D.FK_StatusId=3 then 'InQue' when D.FK_StatusId=7 then 'Paused' end  As
				Status,ROUND(((CompletedRequests+PNFCounts)/TotalRequests)*100,0) AS Percent,ReportDownloadLink
				from tbl_RequestMaster A
				left join tbl_RequestRunDetail D on (D.FK_RequestId=A.RequestId)
				left join tbl_ScheduleTypeMaster C on (C.ShedulId=A.FK_ScheduleTypeId)
				left join tbl_StatusMaster E on (E.StatusId=D.FK_StatusId)
				join tbl_UserMaster U on (U.UserId=A.CreatedBy)
				where A.RequestId=RequestNo				
                and U.UserId=user_Id
				order by A.RequestId desc ;
				
		
			
		ELSEIF RequestDesc!='' THEN
				
				select distinct RequestRunId As requestrunid,RequestId,RequestName as RequestTitle,RequestDescription,
				case when A.FK_ScheduleTypeId=1 then 'Daily' when A.FK_ScheduleTypeId=2 then 'Monthly' when A.FK_ScheduleTypeId=3 then 'Weekly'
				when A.FK_ScheduleTypeId=4 then 'Once' else 'One Time' end AS ScheduleType,
				CONCAT(FirstName," ",LastName) As userName,A.CreatedDatetime,
				D.EndDateTime,TotalRequests AS TR,CompletedRequests As Completed,PNFCounts As PNF,
				Case when (D.FK_StatusId=1 OR D.FK_StatusId=5 OR D.FK_StatusId=13 OR D.FK_StatusId=14 OR D.FK_StatusId=10 OR D.FK_StatusId=9) then 'Running' when D.FK_StatusId=2 then 'Completed' when D.FK_StatusId=3 then 'InQue' when D.FK_StatusId=7 then 'Paused' end  As
				Status,ROUND(((CompletedRequests+PNFCounts)/TotalRequests)*100,0) AS Percent,ReportDownloadLink
				from tbl_RequestMaster A
				left join tbl_RequestRunDetail D on (D.FK_RequestId=A.RequestId)
				left join tbl_ScheduleTypeMaster C on (C.ShedulId=A.FK_ScheduleTypeId)
				left join tbl_StatusMaster E on (E.StatusId=D.FK_StatusId)
				join tbl_UserMaster U on (U.UserId=A.CreatedBy)
				where A.RequestName=RequestDesc				
                and U.UserId=user_Id
				order by A.RequestId desc ;
			
		ELSEIF RequestFromDate !='' AND RequestToDate!='' THEN 
							
				select distinct RequestRunId As requestrunid,RequestId,RequestName as RequestTitle,RequestDescription,
				case when A.FK_ScheduleTypeId=1 then 'Daily' when A.FK_ScheduleTypeId=2 then 'Monthly' when A.FK_ScheduleTypeId=3 then 'Weekly'
				when A.FK_ScheduleTypeId=4 then 'Once' else 'One Time' end AS ScheduleType,
				CONCAT(FirstName," ",LastName) As userName,A.CreatedDatetime,
				D.EndDateTime,TotalRequests AS TR,CompletedRequests As Completed,PNFCounts As PNF,
				Case when (D.FK_StatusId=1 OR D.FK_StatusId=5 OR D.FK_StatusId=13 OR D.FK_StatusId=14 OR D.FK_StatusId=10 OR D.FK_StatusId=9) then 'Running' when D.FK_StatusId=2 then 'Completed' when D.FK_StatusId=3 then 'InQue' when D.FK_StatusId=7 then 'Paused' end  As
				Status,ROUND(((CompletedRequests+PNFCounts)/TotalRequests)*100,0) AS Percent,ReportDownloadLink
				from tbl_RequestMaster A
				left join tbl_RequestRunDetail D on (D.FK_RequestId=A.RequestId)
				left join tbl_ScheduleTypeMaster C on (C.ShedulId=A.FK_ScheduleTypeId)
				left join tbl_StatusMaster E on (E.StatusId=D.FK_StatusId)
				join tbl_UserMaster U on (U.UserId=A.CreatedBy)
				where DATE_FORMAT(A.CreatedDatetime,'%Y-%m-%d') between (RequestFromDate)and (RequestToDate)							
                and U.UserId=user_Id
				order by A.RequestId desc ;
			
		ELSEIF FromNextScheduleDate !=NULL AND ToNextScheduleDate!=NULL THEN
				
				select distinct RequestRunId As requestrunid,RequestId,RequestName as RequestTitle,RequestDescription,
				case when A.FK_ScheduleTypeId=1 then 'Daily' when A.FK_ScheduleTypeId=2 then 'Monthly' when A.FK_ScheduleTypeId=3 then 'Weekly'
				when A.FK_ScheduleTypeId=4 then 'Once' else 'One Time' end AS ScheduleType,
				CONCAT(FirstName," ",LastName) As userName,A.CreatedDatetime,
				D.EndDateTime,TotalRequests AS TR,CompletedRequests As Completed,PNFCounts As PNF,
				Case when (D.FK_StatusId=1 OR D.FK_StatusId=5 OR D.FK_StatusId=13 OR D.FK_StatusId=14 OR D.FK_StatusId=10 OR D.FK_StatusId=9) then 'Running' when D.FK_StatusId=2 then 'Completed' when D.FK_StatusId=3 then 'InQue' when D.FK_StatusId=7 then 'Paused' end  As
				Status,ROUND(((CompletedRequests+PNFCounts)/TotalRequests)*100,0) AS Percent,ReportDownloadLink
				from tbl_RequestMaster A
				left join tbl_RequestRunDetail D on (D.FK_RequestId=A.RequestId)
				left join tbl_ScheduleTypeMaster C on (C.ShedulId=A.FK_ScheduleTypeId)
				left join tbl_StatusMaster E on (E.StatusId=D.FK_StatusId)
                left join tbl_ScheduleDate ts on(ts.SD_RequestId=A.RequestId)
				join tbl_UserMaster U on (U.UserId=A.CreatedBy)
				where DATE_FORMAT(ts.ScheduleDate,'%Y-%m-%d') between (FromNextScheduleDate)and (ToNextScheduleDate)							
                and U.UserId=user_Id
				order by A.RequestId desc ;
			
		ELSEIF FromCompletionDate !='' AND ToCompletionDate!='' THEN
				
				select distinct RequestRunId As requestrunid,RequestId,RequestName as RequestTitle,RequestDescription,
				case when A.FK_ScheduleTypeId=1 then 'Daily' when A.FK_ScheduleTypeId=2 then 'Monthly' when A.FK_ScheduleTypeId=3 then 'Weekly'
				when A.FK_ScheduleTypeId=4 then 'Once' else 'One Time' end AS ScheduleType,
				CONCAT(FirstName," ",LastName) As userName,A.CreatedDatetime,
				D.EndDateTime,TotalRequests AS TR,CompletedRequests As Completed,PNFCounts As PNF,
				Case when (D.FK_StatusId=1 OR D.FK_StatusId=5 OR D.FK_StatusId=13 OR D.FK_StatusId=14 OR D.FK_StatusId=10 OR D.FK_StatusId=9) then 'Running' when D.FK_StatusId=2 then 'Completed' when D.FK_StatusId=3 then 'InQue' when D.FK_StatusId=7 then 'Paused' end  As
				Status,ROUND(((CompletedRequests+PNFCounts)/TotalRequests)*100,0) AS Percent,ReportDownloadLink
				from tbl_RequestMaster A
				left join tbl_RequestRunDetail D on (D.FK_RequestId=A.RequestId)
				left join tbl_ScheduleTypeMaster C on (C.ShedulId=A.FK_ScheduleTypeId)
				left join tbl_StatusMaster E on (E.StatusId=D.FK_StatusId)
				join tbl_UserMaster U on (U.UserId=A.CreatedBy)
				where E.StatusId in (2) and DATE_FORMAT(D.EndDateTime,'%Y-%m-%d') between (FromCompletionDate)and (ToCompletionDate)							
                and U.UserId=user_Id
				order by A.RequestId desc ;
			
		ELSEIF ReqStatus!='' THEN
				
				select distinct RequestRunId As requestrunid,RequestId,RequestName as RequestTitle,RequestDescription,
				case when A.FK_ScheduleTypeId=1 then 'Daily' when A.FK_ScheduleTypeId=2 then 'Monthly' when A.FK_ScheduleTypeId=3 then 'Weekly'
				when A.FK_ScheduleTypeId=4 then 'Once' else 'One Time' end AS ScheduleType,
				CONCAT(FirstName," ",LastName) As userName,A.CreatedDatetime,
				D.EndDateTime,TotalRequests AS TR,CompletedRequests As Completed,PNFCounts As PNF,
				Case when (D.FK_StatusId=1 OR D.FK_StatusId=5 OR D.FK_StatusId=13 OR D.FK_StatusId=14 OR D.FK_StatusId=10 OR D.FK_StatusId=9) then 'Running' when D.FK_StatusId=2 then 'Completed' when D.FK_StatusId=3 then 'InQue' when D.FK_StatusId=7 then 'Paused' end  As
				Status,ROUND(((CompletedRequests+PNFCounts)/TotalRequests)*100,0) AS Percent,ReportDownloadLink
				from tbl_RequestMaster A
				left join tbl_RequestRunDetail D on (D.FK_RequestId=A.RequestId)
				left join tbl_ScheduleTypeMaster C on (C.ShedulId=A.FK_ScheduleTypeId)
				left join tbl_StatusMaster E on (E.StatusId=D.FK_StatusId)
				join tbl_UserMaster U on (U.UserId=A.CreatedBy)
				where D.FK_StatusId=ReqStatus							
                and U.UserId=user_Id
				order by A.RequestId desc ;
			END IF;
	
  END if;  
  SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ ;
   
END ;;
