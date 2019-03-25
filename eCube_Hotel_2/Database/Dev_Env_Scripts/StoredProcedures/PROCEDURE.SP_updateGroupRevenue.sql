DELIMITER ;;

CREATE PROCEDURE `SP_updateGroupRevenue`()
BEGIN
  Set SQL_SAFE_UPDATES= 0;

	CREATE TEMPORARY TABLE IF NOT EXISTS table1 AS (
	select BLI_GRP_Id,sum(Revenue) As GroupRevenue
	from tbl_BliMaster
	group by BLI_GRP_Id);

	select sum(Revenue) INTO @TotalRevenue from  tbl_BliMaster;
	select @TotalRevenue;


    Update tbl_Bli_GroupMaster A
    INNER JOIN table1 B ON (A.Id=B.BLI_GRP_Id)
    set A.GroupRevenue=B.GroupRevenue,
    Weight=Round((B.GroupRevenue*100)/@TotalRevenue,2),
    TotalRevenue=@TotalRevenue;

    select TotalRevenue,Weight,TotalRevenue from  tbl_Bli_GroupMaster;

Drop Temporary Table table1;

END ;;
