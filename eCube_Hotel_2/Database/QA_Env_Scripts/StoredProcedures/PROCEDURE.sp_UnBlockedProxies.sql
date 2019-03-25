DELIMITER ;;

CREATE PROCEDURE `sp_UnBlockedProxies`(

	IN factor INTEGER
)
BEGIN  
			START TRANSACTION ;
			
					
				
				CREATE TEMPORARY TABLE IF NOT EXISTS tblProxyIds AS (select Proxy_Id from tbl_proxytransactionmaster where Proxystatus ='Blocked' Group	By Proxy_Id);
				CREATE TEMPORARY TABLE IF NOT EXISTS tblProxyIdsData AS (select t.* from tbl_proxytransactionmaster t inner join tblProxyIds i on t.Proxy_Id = i.Proxy_Id);
				CREATE TEMPORARY TABLE IF NOT EXISTS tblProxyIdsNotUsed AS (select * from tblProxyIdsData a where Proxystatus = 'UnBlocked');

                INSERT INTO tbl_proxytransactionmaster (Proxy_Id,Domain_Id,ProxyPort,ProxyAddedDateTime,ProxyFirstUsedTime,
					ProxyLastusedTime,  ProxySuccessHits,Country_ID,Region_ID,ProxyStatus,TimeDiffinMinutes)			
				SELECT * FROM 
				(
				 SELECT m.Proxy_Id,Domain_Id,ProxyPort,NOW() As ProxyAddedDateTime,NOW() AS ProxyFirstUsedTime,NOW(),
								1,Country_ID,Region_ID,'UnBlocked' As Status,0  			
									FROM tbl_proxytransactionmaster m inner join 
				(
                    select b.Proxy_Id from tblProxyIds b left join tblProxyIdsNotUsed a 
                    on b.Proxy_Id = a.Proxy_Id where   a.Proxy_Id is null 
                   
                    )  x
					on m.Proxy_ID = x.Proxy_ID
					where ROUND(TIME_TO_SEC(TIMEDIFF(NOW(),ProxyLastusedTime))/60)>=1440
								
				 ORDER BY ProxyLastusedTime 
				) as t1
				GROUP BY Proxy_Id,Domain_Id,ProxyPort,ProxyFirstUsedTime,NULL,1,Country_ID,Region_ID,Status;
						
				/*SELECT * FROM 
				(
				 SELECT m.Proxy_Id,Domain_Id,ProxyPort,NOW() As ProxyAddedDateTime,NOW() AS ProxyFirstUsedTime,NULL,
								1,Country_ID,Region_ID,'UnBlocked' As Status,0  			
									FROM tbl_proxytransactionmaster m inner join (select Proxy_Id from tbl_proxytransactionmaster where Proxystatus !='UnBlocked' Group	 By Proxy_Id) x on m.Proxy_ID = x.Proxy_ID
									where ROUND(TIME_TO_SEC(TIMEDIFF(NOW(),ProxyLastusedTime))/60)>=0
								
				 ORDER BY ProxyLastusedTime 
				) as t1;*/
				
                COMMIT;
                
                
                INSERT into tbl_proxysummary_details (Domain_Id,Proxy_Id,ProxyTypeId,Weights,AvgSuccesshits,Country_Id,Status)
				 select B.Domain_Id,B.Proxy_Id,A.PRM_ProxyTypeId,1,0,B.Country_ID,'UnBlocked' As prstatus
				from tbl_proxytransactionmaster B 
				inner join tbl_ProxyMaster A on (B.Proxy_Id=A.ProxyMasterId)
                left join tbl_proxysummary_details d on d.Proxy_Id = B.Proxy_Id
				where ProxyStatus='UnBlocked' and d.Proxy_Id is null;
                
                
				

END ;;
