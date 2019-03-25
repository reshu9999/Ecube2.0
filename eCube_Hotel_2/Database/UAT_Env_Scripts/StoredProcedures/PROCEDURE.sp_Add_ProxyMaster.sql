DELIMITER ;;

CREATE PROCEDURE `sp_Add_ProxyMaster`(

	IN domain VARCHAR(1000),
 	IN proxyserver VARCHAR(255),
	IN proxyport VARCHAR(100),
 	IN proxycountry VARCHAR(255),
 	IN proxyregion VARCHAR(255),
 	IN pstatus VARCHAR(20),
    IN pdate DateTime,
    OUT result varchar(20))
BEGIN
	SET result='';
    Set SQL_SAFE_UPDATES= 0;
    set innodb_lock_wait_timeout=100;
	START TRANSACTION ;	
    
    	select CountryID INTO @coutryId from tbl_CountryMaster where CountryName=proxycountry;
	
    
		select ProxyMasterId,PRM_ProxyTypeId INTO @proxyId,@PtypeId 
        from tbl_ProxyMaster where ProxyName=proxyserver and CountryId=CountryID;
		
	
		select DomainId INTO @domainId from tbl_DomainMaster where DomainName=domain;
        
        SELECT count(*) INTO @Proxycount FROM tbl_proxytransactionmaster WHERE Proxy_Id=@proxyId
		and Domain_Id=@domainId and Country_Id=@coutryId;
        
        	
         	
		SELECT count(ProxySuccessHits) INTO @successhits FROM tbl_proxytransactionmaster WHERE Proxy_Id=@proxyId 
		AND ProxyPort=proxyport and Domain_Id=@domainId and Country_Id=@coutryId ORDER BY ProxytransactionId DESC LIMIT 1;
        
        SELECT count(*) INTO @table2count FROM tbl_proxysummary_details WHERE Proxy_Id=@proxyId
        and Domain_Id=@domainId and Country_Id=@coutryId;
		
		
		SELECT Proxystatus INTO @PreviousProxystatus FROM tbl_proxytransactionmaster WHERE Proxy_Id=@proxyId
		AND ProxyPort=proxyport and Domain_Id=@domainId and Country_Id=@coutryId ORDER BY ProxytransactionId DESC LIMIT 1;
		
		
					
		SELECT @PreviousProxystatus;
		
		
		IF @successhits=0 AND pstatus='UnBlocked' and @proxyId IS NOT NULL THEN
					select 'Print Step1 ';
                    
					INSERT INTO tbl_proxytransactionmaster (Proxy_Id,Domain_Id,ProxyPort,ProxyAddedDateTime,ProxyFirstUsedTime,ProxyLastusedTime,ProxySuccessHits, 
                    Country_ID,Region_ID,Proxystatus,TimeDiffinMinutes)
					VALUES(@proxyId,@domainId,proxyport,NOW(),pdate,pdate,1,@coutryId,1,'UnBlocked',0);
                    
                    If @table2count=0  THEN
						select avg(weights) INTO @weight from tbl_proxysummary_details where Domain_Id=@domainId and Country_Id=@coutryId and ProxyTypeId=@PtypeId;
						INSERT into tbl_proxysummary_details (Domain_Id,Proxy_Id,ProxyTypeId,Weights,AvgSuccesshits,Country_Id,Status)
						select Domain_Id,Proxy_Id,@PtypeId
								,case when weight < 1 then 1
									else Round(weight )
								end
                                ,0,Country_ID,'UnBlocked' As prstatus
						From
                        (select Domain_Id,Proxy_Id
							,	CASE WHEN @weight IS NULL THEN 1 
									    ELSE case when @weight < 1 then @weight * 10 
											else @weight end 
									END as weight
                             ,0,Country_ID
						from tbl_proxytransactionmaster
						where Proxy_Id=@proxyId and Domain_Id=@domainId and Country_Id=@coutryId LIMIT 1
                        )x;
					END IF;
                    
                    SET result='UnBlocked';
						
		ELSEIF @successhits>0 AND @PreviousProxystatus='Blocked' and pstatus='UnBlocked' and @proxyId IS NOT NULL THEN
					select 'Print Step2 ';					
					INSERT INTO tbl_proxytransactionmaster (Proxy_Id,Domain_Id,ProxyPort,ProxyAddedDateTime,ProxyFirstUsedTime,ProxyLastusedTime,ProxySuccessHits, 
                    Country_ID,Region_ID,Proxystatus,TimeDiffinMinutes)
					VALUES(@proxyId,@domainId,proxyport,NOW(),pdate,pdate,1,@coutryId,1,'UnBlocked',0);
					
                    call sp_ProxyWeightCalculations(@domainId,@coutryId,@PtypeId,@proxyId,pstatus);
					
                    
                    SET result='UnBlocked';
					select 'Print Step2 ';
						
 		ELSEIF @successhits>0 AND @PreviousProxystatus='UnBlocked' and pstatus='UnBlocked' and @proxyId IS NOT NULL THEN
					select 'Print Step3 ';
 					SELECT ProxySuccessHits,ProxytransactionId INTO @successhits,@pid FROM tbl_proxytransactionmaster WHERE Proxy_Id=@proxyId 						
 					AND ProxyPort=proxyport and Domain_Id=@domainId and Country_Id=@coutryId ORDER BY ProxytransactionId desc LIMIT 1;
 									
 					UPDATE tbl_proxytransactionmaster SET ProxyLastusedTime=pdate,ProxySuccessHits=@successhits+1 WHERE Proxy_Id=@proxyId 					
 					AND ProxyPort=proxyport AND ProxyStatus='UnBlocked' and ProxytransactionId=@pid;
					
					SELECT ROUND(TIME_TO_SEC(TIMEDIFF(ProxyLastusedTime,ProxyFirstusedTime))/60,3) INTO @hits from tbl_proxytransactionmaster 
					where ProxytransactionId=@pid;
					UPDATE tbl_proxytransactionmaster SET TimeDiffinMinutes= @hits where ProxytransactionId=@pid;				
					SET result='UnBlocked';
					
				
		ELSEIF @successhits=0 AND pstatus='Blocked' and @proxyId IS NOT NULL THEN		
					select 'Print Step4 ';
				 	INSERT INTO tbl_proxytransactionmaster (Proxy_Id,Domain_Id,ProxyPort,ProxyAddedDateTime,ProxyFirstUsedTime,ProxyLastusedTime,ProxySuccessHits, 
                    Country_ID,Region_ID,Proxystatus,TimeDiffinMinutes)
					VALUES(@proxyId,@domainId,proxyport,NOW(),pdate,pdate,1,@coutryId,1,'Blocked',0);
					UPDATE tbl_proxysummary_details set Status='Blocked' where Proxy_Id=@proxyId and Domain_Id=@domainId and Country_Id=@coutryId;
					SET result='Blocked';
					
		ELSEIF @successhits>0 AND pstatus='Blocked' and @proxyId IS NOT NULL THEN
	
					SELECT ProxyFirstUsedTime,ProxySuccessHits,ProxytransactionId INTO @FirstUsedDate,@successhits,@pid FROM tbl_proxytransactionmaster 
					WHERE Proxy_Id=@proxyId AND ProxyPort=proxyport and Domain_Id=@domainId and Country_Id=@coutryId order by ProxytransactionId DESC LIMIT 1;
					
					
					UPDATE tbl_proxytransactionmaster SET ProxyLastusedTime=pdate,ProxyStatus='Blocked',
					TimeDiffinMinutes=ROUND((TIMEDIFF(ProxyLastusedTime,ProxyFirstusedTime))/60,3) WHERE Proxy_Id=@proxyId
					AND ProxyPort=proxyport AND ProxyStatus='UnBlocked' and ProxytransactionId=@pid;
					
					SELECT ROUND(TIME_TO_SEC(TIMEDIFF(ProxyLastusedTime,ProxyFirstusedTime))/60,3) INTO @hits from tbl_proxytransactionmaster 
					where ProxytransactionId=@pid;
					UPDATE tbl_proxytransactionmaster SET TimeDiffinMinutes= @hits where ProxytransactionId=@pid;					
					
                    UPDATE tbl_proxysummary_details set Status='Blocked' where Proxy_Id=@proxyId and Domain_Id=@domainId and Country_Id=@coutryId;
					delete from tbl_proxysummary_details where Status='Blocked';
                    SET result='Blocked';
					select 'Print Step5 ';
	 
     END IF;    

				
	COMMIT;
     				
   
END ;;
