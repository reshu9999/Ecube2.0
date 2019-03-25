DELIMITER ;;

CREATE PROCEDURE `sp_GetBatchDataAfterErrorCheck_HBA`(                        
	 p_intDipBagDynamicId Int 
	,p_nvcrSupplierID longtext 
)
BEGIN   	
	
    declare v_nvcrReportEmailId NVARCHAR(100);
	declare v_batchId int;
	declare v_nvcrBatchName varchar(50);
    Declare v_NvcrSupplier Longtext Default '';  
	Declare v_NvcrAdltChild Longtext Default '';
	Declare v_NvcrAdlt Longtext Default '';
	Declare v_NvcrChild Longtext Default '';
    
    
	Drop Temporary Table If Exists tmpQACheckList;
	CREATE TEMPORARY TABLE tmpQACheckList                        
	(
		intBatchID INT,
		nvcrBatchName NVARCHAR(50),
		IntCheckListID int,
		vcrComment LONGTEXT
	);   
	 
	
    Call sp_split(p_nvcrSupplierID,',');
    
    Drop Temporary Table If Exists temp_Supplier;
    Create Temporary Table temp_Supplier
    As
    Select items As IntSupplierID From SplitValue;    
    
    
    Drop Temporary Table If Exists temp_BatchCrawlData;
    Create Temporary Table temp_BatchCrawlData
    As
	Select Distinct nvcrHotelStar, nvcrHotelName, nvcrHotelLocation 
	From BatchCrawlData Where intDiPBagDynamicId = p_intDipBagDynamicId
	And intSupplierId in (Select IntSupplierID From temp_Supplier);

	
    Set  v_nvcrReportEmailId = '';
	Set  v_batchId=0;
	set v_nvcrBatchName='';	 
		
	Select d.FK_RequestId, b.RequestName Into v_batchId, v_nvcrBatchName
	From  tbl_RequestRunDetail d 
			inner join tbl_RequestMaster b  
				on d.FK_RequestId = b.RequestId
	where d.RequestRunId = p_intDipBagDynamicId;   
    
	
     
    
	INSERT INTO tmpQACheckList (intBatchID, nvcrBatchName, IntCheckListID, vcrComment)                       
    SELECT  v_batchId,v_nvcrBatchName,69, 'Hotel Name have more than 250 chars'
	from temp_BatchCrawlData  BCD                            
	where Char_length(rtrim(BCD.nvcrHotelName)) > 250 Limit 1;
    
	INSERT INTO tmpQACheckList (intBatchID, nvcrBatchName, IntCheckListID, vcrComment)                       
    SELECT v_batchId,v_nvcrBatchName,70, 'Hotel Name have less than 3 chars'
	from temp_BatchCrawlData  BCD                            
	where Char_length(rtrim(BCD.nvcrHotelName)) < 3 Limit 1;
	
	INSERT INTO tmpQACheckList (intBatchID, nvcrBatchName, IntCheckListID, vcrComment)                       
    SELECT Distinct  v_batchId,v_nvcrBatchName,245, CONCAT('Hotel Name contain only special characters i:e ' , Ifnull(nvcrHotelName,''))
	from temp_BatchCrawlData  BCD                            
	where nvcrHotelName  LIKE   '%`~@#$%^*=+{};/?%'
	And Ifnull(nvcrHotelName,'') != '';
	
	INSERT INTO tmpQACheckList (intBatchID, nvcrBatchName, IntCheckListID, vcrComment)                       
    SELECT v_batchId,v_nvcrBatchName, 75, 'HotelAddress contain junk characters'
	from temp_BatchCrawlData  BCD                            
	where BCD.nvcrHotelLocation Like '%<%' Or nvcrHotelLocation Like '%>%' Or nvcrHotelLocation Like '%=%'
		Limit 1;
	 
	
	Drop Temporary Table If Exists Temp_QACheck1;
	Create Temporary Table Temp_QACheck1
    As    
	Select ncvrCheckListName, `Status`, A.Comment From 
	(
	Select  
		Ifnull(MS.ncvrCheckListName,'') ncvrCheckListName , Case When MS.intCheckList in (235,236,237,238)  Then '' Else 'Fail' End Status, QA.vcrComment Comment
		, MS.intDisplayOrder
	From tmpQACheckList QA   Left Join MstCheckList_HBA MS  
	On QA.IntCheckListID = MS.intCheckList And MS.nvcrCheckListType = 'QACheck'
	 
	) A
	Order by intDisplayOrder; 
    
    
    Drop Temporary Table If Exists Temp_QACheck2;
	Create Temporary Table Temp_QACheck2
    As
	Select ncvrCheckListName, `Status`, A.Comment From 
	(
	 Select Mst.ncvrCheckListName, 'Pass' Status, '' Comment, Mst.intDisplayOrder
	From MstCheckList_HBA Mst WHere Mst.intCheckList not in (Select IntCheckListID From tmpQACheckList)
	And nvcrCheckListType = 'QACheck' And Mst.bitCheckList = 1
	) A
	Order by intDisplayOrder; 
    
    insert into TempQA_ECUBE_MDM_Hotel_Avail (QA_Checks, Status, nvcrComment)
    Select * From Temp_QACheck1
    union 
    Select * From Temp_QACheck2;
	
	 
END ;;
