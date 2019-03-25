DELIMITER ;;

CREATE PROCEDURE `GetBatchData_BKP_08JUN18`(
IN BliId int(11)
)
BEGIN
select round(t1.CompletedRequests/t1.TotalRequests*100) as Percent, Case t4.StatusId when 5 Then 'Running' else t4.StatusTitle end as Status, t2.RequestName, date_format(t2.CreatedDatetime,"%m/%d/%Y") as Date, date_format(t2.CreatedDatetime,"%l:%i:%s %p") as Time from tbl_RequestRunDetail t1
join tbl_RequestMaster t2 on t1.FK_RequestId = t2.RequestId
join tbl_BliMaster t3 on t2.FK_BLIId =  t3.BliId
join tbl_StatusMaster t4 on t1.FK_StatusId = t4.StatusId
where t3.BliId = BliId
order by t2.CreatedDatetime desc
Limit 4;
END ;;
