DELIMITER ;;

CREATE PROCEDURE `spGetRequestRunDetail`()
BEGIN
#set  @StatusId = (Select StatusId from tbl_StatusMaster where StatusTitle = 'InQue' limit 1);

# select * from tbl_RequestRunDetail where FK_StatusId = 3;

	select a.*,b.RequestModeId 
    from tbl_RequestRunDetail as a inner join tbl_RequestMaster as b
		on b.RequestId=a.FK_RequestId 
    where  a.FK_StatusId = 3;

END ;;
