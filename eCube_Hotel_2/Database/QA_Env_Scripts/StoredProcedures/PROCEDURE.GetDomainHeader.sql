DELIMITER ;;

CREATE PROCEDURE `GetDomainHeader`(
domainName varchar(500)
)
BEGIN
Select Id, t2.DomainId, HeaderName, HeaderValue  from tbl_DomainMaster t1, tbl_DomainHeaderMapping t2 where t2.DomainId = t1.DomainId And t1.DomainName = domainName;


END ;;
