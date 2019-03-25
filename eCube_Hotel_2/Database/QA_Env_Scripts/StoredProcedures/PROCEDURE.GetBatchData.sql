DELIMITER ;;

CREATE PROCEDURE `GetBatchData`(
IN BliId int(11),
IN uid int(11)
)
BEGIN
/*******************************************************************         
'	Name					: GetBatchData
'	Desc					: To 
'	Called by				: 
'	Example of execution	: 
INPUT PARAMETRS		 	 
	BliId int,
	uid int
Retruns

'	Created by				: 
'	Date of creation		: 

******************************************************************************************************
Change History
******************************************************************************************************
Sr.No.		Date:			Changed by:			Description:
1			11-Jun-2018		Bhavin.Dhimmar		Add new input parameter uid
******************************************************************************************************/	
/*select round(t1.CompletedRequests/t1.TotalRequests*100) as Percent, Case t4.StatusId when 5 Then 'Running' else t4.StatusTitle end as Status, t2.RequestName, date_format(t2.CreatedDatetime,"%m/%d/%Y") as Date, date_format(t2.CreatedDatetime,"%l:%i:%s %p") as Time from tbl_RequestRunDetail t1
join tbl_RequestMaster t2 on t1.FK_RequestId = t2.RequestId
join tbl_BliMaster t3 on t2.FK_BLIId =  t3.BliId
join tbl_StatusMaster t4 on t1.FK_StatusId = t4.StatusId
where t3.BliId = BliId
order by t2.CreatedDatetime desc
Limit 4;
*/
	select round((100*(t1.CompletedRequests + t1.PNFCounts))/t1.TotalRequests) as Percent, Case t4.StatusId when 5 Then 'Running' else t4.StatusTitle end as Status, t2.RequestName, date_format(t2.CreatedDatetime,"%m/%d/%Y") as Date, date_format(t2.CreatedDatetime,"%l:%i:%s %p") as Time 
	from tbl_RequestRunDetail t1
	join tbl_RequestMaster t2 on t1.FK_RequestId = t2.RequestId
	join tbl_BliMaster t3 on t2.FK_BLIId =  t3.BliId
	join tbl_StatusMaster t4 on t1.FK_StatusId = t4.StatusId
	where t3.BliId = BliId
		and t2.CreatedBy = uid 
	order by t2.CreatedDatetime  desc
	Limit 5;

END ;;
