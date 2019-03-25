DELIMITER ;;

CREATE PROCEDURE `sp_Fetch_Proxydetails`(

 	IN domain VARCHAR(1000),
 	IN country VARCHAR(255))
BEGIN
		
		SELECT DomainId INTO @DomainId from tbl_DomainMaster  where DomainName= domain;
		SELECT CountryId INTO @countryId from tbl_CountryMaster where CountryName= country;
		        
        
		select DomainName,ProxyName,B.ProxyTypeName,Weights,CountryName,'UnBlocked' AS Status,
        tp.ProxyUserName,tp.ProxyPassword,tp.ProxyPort
		from tbl_proxysummary_details  A       
		INNER JOIN tbl_ProxyMaster tp ON(tp.ProxyMasterId=A.Proxy_ID)
		INNER JOIN tbl_DomainMaster D ON(D.DomainId=A.Domain_Id)
		INNER JOIN tbl_ProxyTypeMaster B ON(B.ProxyTypeID=A.ProxyTypeID)
		INNER JOIN tbl_CountryMaster C ON(C.CountryId=A.Country_ID)
		where A.Domain_Id= @DomainId and A.Country_Id=@countryId
        and A.Status='UnBlocked';
    
		
END ;;
