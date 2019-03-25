DELIMITER ;;

CREATE PROCEDURE `sp_Insert_Inputdetails`(IN tab_name VARCHAR(40))
BEGIN
 SET @t1 =CONCAT('CREATE TEMPORARY TABLE table1 SELECT * FROM ',tab_name );
 PREPARE stmt3 FROM @t1;
 EXECUTE stmt3;
 DEALLOCATE PREPARE stmt3;
 
	select count(*) INTO @validurlcount
	from table1 A left join tbl_DomainMaster B on (B.DomainName=SUBSTRING_INDEX(SUBSTRING_INDEX(A.comProductURL,'/',3),'//',-1))
	join tbl_RequestTypeMaster C on (C.RequestTypeName=A.Type)
	and C.RequestTypeId=1 and B.DomainId is Null; 
 
		if @validurlcount=0 then
        
			 insert into tbl_RequestInputDetails (FK_RequestId,RequestURL,FK_DomainId,RequestTypeId,CreatedDateTime,UpdatedDateTime)
			 select RequestId,comProductURL,B.DomainId,C.RequestTypeId,Now(),Now()
			 from table1 A
			 join tbl_DomainMaster B on (B.DomainName=SUBSTRING_INDEX(SUBSTRING_INDEX(A.comProductURL,'/',3),'//',-1))
			 join tbl_RequestTypeMaster C on (C.RequestTypeName=A.Type); 
			 
			 insert into tbl_RequestInputDetails (FK_RequestId,RequestURL,FK_DomainId,RequestTypeId,CreatedDateTime,UpdatedDateTime)
			 select RequestId,comProductURL,A.DomainId,C.RequestTypeId,Now(),Now()
			 from table1 A 
			 join tbl_RequestTypeMaster C on (C.RequestTypeName=A.Type)
			 where A.DomainId>0;
			 
	  
			 SET @t2 =CONCAT('Drop table ',tab_name );
			 PREPARE stmt4 FROM @t2;
			 EXECUTE stmt4;
			 DEALLOCATE PREPARE stmt4;
		end if;	
 drop temporary table table1;
END ;;
