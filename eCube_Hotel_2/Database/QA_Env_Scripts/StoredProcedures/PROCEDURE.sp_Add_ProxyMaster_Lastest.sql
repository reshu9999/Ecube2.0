DELIMITER ;;

CREATE PROCEDURE `sp_Add_ProxyMaster_Lastest`(

 	 	IN domain VARCHAR(1000),
 	IN proxyserver VARCHAR(255),
	IN proxyport VARCHAR(100),
 	IN proxycountry VARCHAR(255),
 	IN proxyregion VARCHAR(255),
 	IN pstatus VARCHAR(20),
    OUT result integer)
BEGIN
	SET result=0;
    Set SQL_SAFE_UPDATES= 0;
	START TRANSACTION ;	
	
		select ProxyMasterId,PRM_ProxyTypeId INTO @proxyId,@PtypeId from tbl_ProxyMaster where ProxyName=proxyserver;
		
		select CountryID INTO @coutryId from tbl_CountryMaster where CountryName=proxycountry;
		select DomainId INTO @domainId from tbl_DomainMaster where DomainName=domain;
        
        SELECT count(*) INTO @Proxycount FROM tbl_proxytransactionmaster_tmp WHERE Proxy_Id=@proxyId;
        
        	
         	
		SELECT count(ProxySuccessHits) INTO @successhits FROM tbl_proxytransactionmaster_tmp WHERE Proxy_Id=@proxyId 
		AND ProxyPort=proxyport ORDER BY ProxytransactionId DESC LIMIT 1;
        
        SELECT count(*) INTO @table2count FROM tbl_proxysummary_details_tmp WHERE Proxy_Id=@proxyId;
		
		
		SELECT Proxystatus INTO @PreviousProxystatus FROM tbl_proxytransactionmaster_tmp WHERE Proxy_Id=@proxyId
		AND ProxyPort=proxyport ORDER BY ProxytransactionId DESC LIMIT 1;
		
		
					
		SELECT @PreviousProxystatus;
		
		
		IF @successhits=0 AND pstatus='UnBlocked' THEN
					select 'Print Step1 ';
					INSERT INTO tbl_proxytransactionmaster_tmp (Proxy_Id,Domain_Id,ProxyPort,ProxyAddedDateTime,ProxyFirstUsedTime,ProxyLastusedTime,ProxySuccessHits, 
                    Country_ID,Region_ID,Proxystatus,TimeDiffinMinutes)
					VALUES(@proxyId,@domainId,proxyport,NOW(),NOW(),NOW(),1,@coutryId,1,'UnBlocked',0);
                    
                    If @table2count=0  THEN
					
						INSERT into tbl_proxysummary_details_tmp (Domain_Id,Proxy_Id,ProxyTypeId,Weights,AvgSuccesshits,Country_Id,Status)
						select Domain_Id,Proxy_Id,@PtypeId,1,0,Country_ID,'UnBlocked' As prstatus
						from tbl_proxytransactionmaster_tmp
						where Proxy_Id=@proxyId LIMIT 1;
					END IF;
                    
                    SET result=ROW_COUNT();
						
		ELSEIF @successhits>0 AND @PreviousProxystatus='Blocked' and pstatus='UnBlocked' THEN
					select 'Print Step2 ';					
					INSERT INTO tbl_proxytransactionmaster_tmp (Proxy_Id,Domain_Id,ProxyPort,ProxyAddedDateTime,ProxyFirstUsedTime,ProxyLastusedTime,ProxySuccessHits, 
                    Country_ID,Region_ID,Proxystatus,TimeDiffinMinutes)
					VALUES(@proxyId,@domainId,proxyport,NOW(),NOW(),NOW(),1,@coutryId,1,'UnBlocked',0);
					
						call sp_ProxyWeightCalculations(@domainId,@coutryId,@PtypeId,@proxyId,pstatus);
                    
                    SET result=ROW_COUNT();
					select 'Print Step2 ';
						
 		ELSEIF @successhits>0 AND @PreviousProxystatus='UnBlocked' and pstatus='UnBlocked' THEN
					select 'Print Step3 ';
 					SELECT ProxySuccessHits,ProxytransactionId INTO @successhits,@pid FROM tbl_proxytransactionmaster_tmp WHERE Proxy_Id=@proxyId 						
 					AND ProxyPort=proxyport ORDER BY ProxytransactionId desc LIMIT 1;
 									
 					UPDATE tbl_proxytransactionmaster_tmp SET ProxyLastusedTime=NOW(),ProxySuccessHits=@successhits+1 WHERE Proxy_Id=@proxyId 					
 					AND ProxyPort=proxyport AND ProxyStatus='UnBlocked' and ProxytransactionId=@pid;
					
					SELECT TIME_TO_SEC(TIMEDIFF(ProxyLastusedTime,ProxyFirstusedTime))/60 INTO @hits from tbl_proxytransactionmaster_tmp 
					where ProxytransactionId=@pid;
					UPDATE tbl_proxytransactionmaster_tmp SET TimeDiffinMinutes= @hits where ProxytransactionId=@pid;				
					SET result=ROW_COUNT();
					
				
		ELSEIF @successhits=0 AND pstatus='Blocked' THEN		
					select 'Print Step4 ';
				 	INSERT INTO tbl_proxytransactionmaster_tmp (Proxy_Id,Domain_Id,ProxyPort,ProxyAddedDateTime,ProxyFirstUsedTime,ProxyLastusedTime,ProxySuccessHits, 
                    Country_ID,Region_ID,Proxystatus,TimeDiffinMinutes)
					VALUES(@proxyId,@domainId,proxyport,NOW(),NOW(),NOW(),1,@coutryId,1,'Blocked',0);
					UPDATE tbl_proxysummary_details_tmp set Status='Blocked' where Proxy_Id=@proxyId;
					SET result=ROW_COUNT();
					
		ELSEIF @successhits>0 AND pstatus='Blocked' THEN
					select 'Print Step5 ';
					SELECT ProxyFirstUsedTime,ProxySuccessHits,ProxytransactionId INTO @FirstUsedDate,@successhits,@pid FROM tbl_proxytransactionmaster_tmp 
					WHERE Proxy_Id=@proxyId AND ProxyPort=proxyport order by ProxytransactionId DESC LIMIT 1;
					
					
					UPDATE tbl_proxytransactionmaster_tmp SET ProxyLastusedTime=NOW(),ProxyStatus='Blocked',
					TimeDiffinMinutes=(TIMEDIFF(NOW(),ProxyFirstusedTime))/60 WHERE Proxy_Id=@proxyId
					AND ProxyPort=proxyport AND ProxyStatus='UnBlocked' and ProxytransactionId=@pid;
					
					SELECT TIME_TO_SEC(TIMEDIFF(ProxyLastusedTime,ProxyFirstusedTime))/60 INTO @hits from tbl_proxytransactionmaster_tmp 
					where ProxytransactionId=@pid;
					UPDATE tbl_proxytransactionmaster_tmp SET TimeDiffinMinutes= @hits where ProxytransactionId=@pid;					
					
                    UPDATE tbl_proxysummary_details_tmp set Status='Blocked' where Proxy_Id=@proxyId;
					delete from tbl_proxysummary_details_tmp where Status='Blocked';
                    SET result=ROW_COUNT();
	 
     END IF;    

				
	COMMIT;
     				
   
END ;;
