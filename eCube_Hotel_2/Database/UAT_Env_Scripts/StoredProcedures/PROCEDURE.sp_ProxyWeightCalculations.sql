DELIMITER ;;

CREATE PROCEDURE `sp_ProxyWeightCalculations`(
	
	domainId INTEGER,
	CountryId INTEGER,
	TypeId INTEGER,
    proxyId INTEGER,
    pStatus varchar(255))
BEGIN

Set SQL_SAFE_UPDATES= 0;	

			select PRM_ProxyTypeId INTO @PtypeId from tbl_ProxyMaster where ProxyMasterId=proxyId;
		

			CREATE TEMPORARY TABLE IF NOT EXISTS table1 AS (
			select A.Domain_Id,A.Proxy_Id,C.ProxyTypeID,round(SUM(A.ProxySuccessHits)/SUM(TimeDiffinminutes),2) As Avgsuccehitpermin,D.CountryID			
			from tbl_proxytransactionmaster A
			join tbl_ProxyMaster B on (A.Proxy_Id=B.ProxyMasterId)
			join tbl_CountryMaster D on (D.CountryID=A.Country_ID)
			JOIN tbl_ProxyTypeMaster C on (C.ProxyTypeID=B.PRM_ProxyTypeId)		
			where D.CountryID =CountryId  and A.Domain_Id = domainId and C.ProxyTypeID=TypeId            
            and ProxyStatus='Blocked'
			GROUP BY A.Domain_Id,A.Proxy_Id,C.ProxyTypeID,D.CountryID);
						
			CREATE TEMPORARY TABLE IF NOT EXISTS table2 AS (select ProxyTypeID,sum(Avgsuccehitpermin) AS s 
			from table1 GROUP BY ProxyTypeID,CountryID);
            
			CREATE TEMPORARY TABLE IF NOT EXISTS table3 AS
			(select A.Domain_Id,A.Proxy_Id,@PtypeId,
			Case when Sum(B.Avgsuccehitpermin)/ C.s<1 then ROUND((Sum(B.Avgsuccehitpermin)/ C.s)*10) else 1 END As Weight
			,B.Avgsuccehitpermin,A.Country_ID,'UnBlocked' As Status
			from tbl_proxytransactionmaster A
			INNER JOIN table1 B on (A.Proxy_Id=B.Proxy_Id)
			INNER JOIN table2 C on (B.ProxyTypeID=C.ProxyTypeID)
			where ProxyStatus='UnBlocked' and B.ProxyTypeID=@PtypeId
			and A.domain_Id=domainId and A.Country_ID=CountryId
			Group by A.Domain_Id,A.Proxy_Id,A.Country_ID,C.s,B.Avgsuccehitpermin);
		    
				Update tbl_proxysummary_details A
				INNER JOIN table3 B on (A.Proxy_Id=B.Proxy_Id and A.Domain_Id=B.Domain_Id)
				set A.Weights=B.Weight,A.AvgSuccesshits=B.Avgsuccehitpermin;			
		
		
				INSERT into tbl_proxysummary_details (Domain_Id,Proxy_Id,ProxyTypeId,Weights,AvgSuccesshits,Country_Id,Status)
				
                select x.Domain_Id,x.Proxy_Id,@PtypeId,x.Weight,
				x.Avgsuccehitpermin,x.Country_Id,x.Status
                from table3 x
                left join tbl_proxysummary_details y on (x.Proxy_Id=y.Proxy_Id and x.Domain_Id=y.Domain_Id) 
				where y.Proxy_Id is null;
			
                        
		DROP TEMPORARY TABLE table1;
		DROP TEMPORARY TABLE table2;
        DROP TEMPORARY TABLE table3;
			
END ;;
