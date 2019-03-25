DELIMITER ;;

CREATE PROCEDURE `sp_GetTimeZoneWiseProxy`(
	IN CountryName VARCHAR(255),
	IN TypeID INTEGER,
	IN Domain VARCHAR(1000))
BEGIN		
			
			select SUBSTRING(TimeZone,2) into @timezone from tbl_CountryMaster where CountryName=CountryName limit 1;
            
            
			
			CREATE TEMPORARY TABLE IF NOT EXISTS table2 AS (
			select distinct b.Proxy_Id 
				from tbl_ProxyMaster a 
				join tbl_proxysummary_details b on (a.CountryId=b.Country_Id) 
				join tbl_CountryMaster c on (c.CountryID=b.Country_Id)
				and c.timeZone between  CONCAT('+',DATE_FORMAT(TIMEDIFF('08:45','01:00'),'%H:%i')) 
				and  CONCAT('-',DATE_FORMAT(TIMEDIFF('08:45','-01:00'),'%H:%i'))
                and b.Status='UnBlocked'
                AND c.CountryName!=CountryName and PRM_ProxyTypeId=TypeID);
			
			select D.DomainName,P.ProxyName,PT.ProxyTypeName,Weights,C.CountryName,'UnBlocked' AS Status,
            P.ProxyUserName,P.ProxyPassword,P.ProxyPort
			from tbl_proxysummary_details A
			INNER JOIN tbl_DomainMaster D on (A.Domain_Id=D.DomainId)
			INNER JOIN tbl_ProxyMaster P on (A.Proxy_Id=P.ProxyMasterId)
			INNER JOIN tbl_ProxyTypeMaster PT on (A.ProxyTypeId=PT.ProxyTypeId)
			INNER JOIN tbl_CountryMaster C on (A.Country_Id=C.CountryID)
			INNER JOIN table2 B on (A.Proxy_Id=B.Proxy_Id) 
			where D.DomainName=Domain and A.ProxyTypeId=TypeID  order by Weights limit 1 ;

	Drop temporary table table2;	  
END ;;
