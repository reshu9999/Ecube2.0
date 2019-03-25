DELIMITER ;;

CREATE PROCEDURE `sp_Add_ProxyMaster1`(

 	IN domain VARCHAR(1000),
 	IN proxyserver VARCHAR(255),
	IN proxyport VARCHAR(100),
 	IN proxycountry VARCHAR(255),
 	IN proxyregion VARCHAR(255),
 	IN pstatus VARCHAR(20),    
    OUT result integer)
BEGIN
	SET result=0;
	START TRANSACTION ;	
		
		
		SELECT ProxyStatus INTO @PreviousProxystatus FROM tbl_Proxyuses WHERE Proxy_Name=proxyserver
		AND Proxy_Port=proxyport ORDER BY id DESC LIMIT 1;
        
        SELECT count(ProxySuccessHits) INTO @successhits FROM tbl_Proxyuses WHERE Proxy_Name=proxyserver 
		AND Proxy_Port=proxyport ORDER BY id DESC LIMIT 1;
		
					
		SELECT @PreviousProxystatus;
		IF @successhits=0 AND pstatus='UnBlocked' THEN
					select 'Print Step1 ';
					INSERT INTO tbl_Proxyuses (Proxy_Name,Proxy_Port,Domain_Name,ProxyAdddedDate,ProxyFirstUsedDate,ProxyLastUsedDate,ProxySuccessHits,Country_Name,Region_Name,ProxyStatus)
					VALUES(proxyserver,proxyport,domain,now(),now(),now(),1,proxycountry,proxyregion,pstatus);
					
                    SET result=ROW_COUNT();
						
		ELSEIF @successhits>0 AND @PreviousProxystatus='Blocked' and pstatus='UnBlocked' THEN
					select 'Print Step2 ';					
					INSERT INTO tbl_Proxyuses (Proxy_Name,Proxy_Port,Domain_Name,ProxyAdddedDate,ProxyFirstUsedDate,ProxyLastUsedDate,ProxySuccessHits,Country_Name,Region_Name,ProxyStatus)
					VALUES(proxyserver,proxyport,domain,now(),now(),now(),1,proxycountry,proxyregion,pstatus);
                    
                    SET result=ROW_COUNT();
					select 'Print Step2 ';
						
 		ELSEIF @successhits>0 AND @PreviousProxystatus='UnBlocked' and pstatus='UnBlocked' THEN
					select 'Print Step3 ';
 					SELECT ProxySuccessHits,id INTO @successhits,@pid FROM tbl_Proxyuses WHERE Proxy_Name=proxyserver 						
 					AND Proxy_Port=proxyport ORDER BY id desc LIMIT 1;
 									
 					UPDATE tbl_Proxyuses SET ProxyLastUsedDate=NOW(),ProxySuccessHits=@successhits+1 WHERE Proxy_Name=proxyserver 					
 					AND Proxy_Port=proxyport AND ProxyStatus='UnBlocked' and id=@pid;
					
					SELECT ROUND(TIME_TO_SEC(TIMEDIFF(ProxyLastUsedDate,ProxyFirstUsedDate))/60) INTO @hits from tbl_Proxyuses 
					where id=@pid;
					UPDATE tbl_Proxyuses SET TimeDiffinMinutes= @hits where id=@pid;				
					SET result=ROW_COUNT();
					
				
		ELSEIF @successhits=0 AND pstatus='Blocked' THEN		
					select 'Print Step4 ';
				 	INSERT INTO tbl_Proxyuses (Proxy_Name,Proxy_Port,Domain_Name,ProxyAdddedDate,ProxyFirstUsedDate,ProxyLastUsedDate,ProxySuccessHits,Country_Name,Region_Name,ProxyStatus)
					VALUES(proxyserver,proxyport,domain,now(),now(),now(),1,proxycountry,proxyregion,pstatus);
						
					SET result=ROW_COUNT();
					
		ELSEIF @successhits>0 AND pstatus='Blocked' THEN
					select 'Print Step5 ';
					SELECT ProxyFirstUsedDate,ProxySuccessHits,id INTO @FirstUsedDate,@successhits,@pid FROM tbl_Proxyuses 
					WHERE Proxy_Name=proxyserver AND Proxy_Port=proxyport order by id DESC LIMIT 1;
					
					
					UPDATE tbl_Proxyuses SET ProxyLastUsedDate=NOW(),ProxyStatus='Blocked',
					TimeDiffinMinutes=(TIMEDIFF(NOW(),ProxyFirstUsedDate))/60 WHERE Proxy_Name=proxyserver
					AND Proxy_Port=proxyport AND ProxyStatus='UnBlocked' and id=@pid;
					
					SELECT ROUND(TIME_TO_SEC(TIMEDIFF(ProxyLastUsedDate,ProxyFirstUsedDate))/60) INTO @hits from tbl_Proxyuses 
					where id=@pid;
					UPDATE tbl_Proxyuses SET TimeDiffinMinutes= @hits where id=@pid;					
					
                    SET result=ROW_COUNT();
	 
     END IF;     
     
	COMMIT;
   
END ;;
