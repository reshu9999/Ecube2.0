DELIMITER ;;

CREATE PROCEDURE `spInsertNewRequestInputDetails`(
IN URL varchar(500), 
IN Req_type_ID INT,
IN Req_ID INT, 
IN Domain_Name VARCHAR(200))
BEGIN
    INSERT INTO `eCube_Centralized_DB`.`tbl_RequestInputDetails`
	(
		`RequestURL`,
		`RequestTypeId`,
		`FK_RequestId`,
		`FK_DomainId`,
		`CreatedDatetime`
	)
	VALUES
	(
		URL,
		Req_type_ID,
		Req_ID,
		(SELECT DomainId FROM tbl_DomainMaster where lower(DomainName) = lower(Domain_Name) and Active = 1 Limit 1),
        
		NOW()
	);
END ;;
