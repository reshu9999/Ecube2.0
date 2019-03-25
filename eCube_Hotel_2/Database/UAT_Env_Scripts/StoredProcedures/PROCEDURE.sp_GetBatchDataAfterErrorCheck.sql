DELIMITER ;;

CREATE PROCEDURE `sp_GetBatchDataAfterErrorCheck`(                        
	 p_RequestRunId Int 
	,p_nvcrSupplierID longtext 
)
BEGIN              
	
	declare v_RequestId int;
	declare v_nvcrReportEmailId NVARCHAR(100);
	declare v_RequestName varchar(50);
    Declare v_NvcrSupplier Longtext Default ''; 
    Declare v_NvcrAdltChild Longtext Default '';
	Declare v_NvcrAdlt Longtext Default '';
	Declare v_NvcrChild Longtext Default '';
	
    Set v_nvcrReportEmailId = '';
	Set v_RequestId=0;
	set v_RequestName='';
    
		 
	Select d.FK_RequestId Into v_RequestId
	From RequestRunDetail d inner join tbl_RequestMaster b 
		on d.FK_RequestId = b.RequestId
	where d.RequestRunId = p_RequestRunId; 	 
	
    
    
	Drop Temporary Table if exists tmpQACheckList ;                
	CREATE TEMPORARY TABLE tmpQACheckList                        
	(
		intBatchID INT,
		nvcrBatchName NVARCHAR(50),
		IntCheckListID int,
		vcrComment LONGTEXT
	);   	 
    
    Call sp_split(p_nvcrSupplierID,',');
    Drop Temporary Table if exists temp_Supplier;     
    Create Temporary Table temp_Supplier (IntSupplierID int);
    
    Insert into temp_Supplier(IntSupplierID)
    Select items from SplitValue;
	
    Drop Temporary Table if exists temp_BatchCrawlData;     
    Create Temporary Table temp_BatchCrawlData 
    As
	Select Distinct nvcrHotelStar, nvcrHotelName, nvcrHotelLocation 
	From BatchCrawlData  Where intDiPBagDynamicId = p_RequestRunId
	And intSupplierId in (Select IntSupplierID From temp_Supplier);	 
	
	Select d.FK_RequestId, b.RequestName Into v_RequestId, v_RequestName
	From RequestRunDetail d inner join tbl_RequestMaster b 
		on d.FK_RequestId = b.RequestId
	where d.RequestRunId = p_RequestRunId;	
	 
    
	CALL sp_LastResult(v_RequestId, p_RequestRunId,p_nvcrSupplierID);
	 	
    
	
    
    INSERT INTO tmpQACheckList (intBatchID, nvcrBatchName, IntCheckListID, vcrComment)                       
    SELECT v_RequestId,v_RequestName,69, 'Hotel Name have more than 250 chars'
	from temp_BatchCrawlData  BCD
	where Char_length(rtrim(BCD.nvcrHotelName)) > 250 limit 1;    
	
    INSERT INTO tmpQACheckList (intBatchID, nvcrBatchName, IntCheckListID, vcrComment)                       
    SELECT v_RequestId,v_RequestName,70, 'Hotel Name have less than 3 chars'
		from temp_BatchCrawlData  BCD  
	where Char_length(rtrim(BCD.nvcrHotelName)) < 3 Limit 1;		 
	
	INSERT INTO tmpQACheckList (intBatchID, nvcrBatchName, IntCheckListID, vcrComment)                       
    SELECT Distinct  v_RequestId,v_RequestName,245, CONCAT('Hotel Name contain only special characters i:e ' , Ifnull(nvcrHotelName,''))
	from temp_BatchCrawlData  BCD               
	where nvcrHotelName  LIKE   '%`~@#$%^*=+{};/?%'
	And Ifnull(nvcrHotelName,'') != '';	  
	
	INSERT INTO tmpQACheckList (intBatchID, nvcrBatchName, IntCheckListID, vcrComment)                       
    SELECT v_RequestId,v_RequestName, 75, 'HotelAddress contain junk characters'
	from temp_BatchCrawlData  BCD              
	where BCD.nvcrHotelLocation Like '%<%' Or nvcrHotelLocation Like '%>%' Or nvcrHotelLocation Like '%=%'
    Limit 1; 

	Insert into tmpQACheckList (intBatchID, nvcrBatchName, IntCheckListID, vcrComment)  
	Select Distinct  v_RequestId,v_RequestName,238, CONCAT('Room Code :-' , Ifnull(RoomCode,'')) 
	from LastResultQACheck  BCD 
	Where intDipBagDynamicId = p_RequestRunId 
	And Ifnull(RoomCode,'') NOt in ('SUI', 'STU', 'DBT', 'SGL', 'X01', 'CTG', 'VIL', 'FAM', 'APT' , 'JSU', 'X09'); 
	  
    INSERT INTO tmpQACheckList (intBatchID, nvcrBatchName, IntCheckListID, vcrComment)  
	Select Distinct v_RequestId,v_RequestName,80, CONCAT('Price is Greater than 30000 for ' , Company)  
		from LastResultQACheck BCD  Where intDiPBagDynamicId = p_RequestRunId     
		And fn_IsNumeric(Price) = 1
		And Price != ''
    And CAST(Price as Decimal(11,4)) > 30000;
	
	
	INSERT INTO tmpQACheckList (intBatchID, nvcrBatchName, IntCheckListID, vcrComment)                                       
	SELECT v_RequestId,v_RequestName,91, 'Room Type value is less than 3 char'                       
		FROM LastResultQACheck  BCD              
		WHERE  intDipBagDynamicId = p_RequestRunId And Char_length(rtrim(Ltrim(Rtrim(BCD.RoomType)))) <  3 
		Limit 3;
	 
	
	INSERT INTO tmpQACheckList (intBatchID, nvcrBatchName, IntCheckListID, vcrComment)                                       
	SELECT v_RequestId,v_RequestName,92, 'Room Type value is greater than 240 char'                       
		FROM LastResultQACheck  BCD               
		WHERE  intDipBagDynamicId = p_RequestRunId And Char_length(rtrim(Ltrim(Rtrim(BCD.RoomType)))) >  240 
		limit 1;
	
	
	INSERT INTO tmpQACheckList (intBatchID, nvcrBatchName, IntCheckListID, vcrComment)                                       
	SELECT v_RequestId,v_RequestName,94, 'Promotion Description Length is greater than 240'                       
		FROM LastResultQACheck  BCD               
		WHERE  intDipBagDynamicId = p_RequestRunId 
		And Char_length(rtrim(Ltrim(Rtrim(BCD.nvcrPromotionDescription)))) >  240 
		lIMIT 1;
	    
	  
	INSERT INTO tmpQACheckList (intBatchID, nvcrBatchName, IntCheckListID, vcrComment)                                       
	SELECT Distinct v_RequestId,v_RequestName,235, CONCAT('Account Display :- ' , Ifnull(Company,'') , '-' , Ifnull(BCD.nvcrAccountName,''))   
	From  LastResultQACheck  BCD              
			 WHERE  intDipBagDynamicId = p_RequestRunId;
	
	INSERT INTO tmpQACheckList (intBatchID, nvcrBatchName, IntCheckListID, vcrComment)                                       
	SELECT Distinct v_RequestId,v_RequestName,237, CONCAT('Pax is ' , Ifnull(nvcrAdult,''))
	From  LastResultQACheck  BCD
			 WHERE  intDipBagDynamicId = p_RequestRunId;
			
	INSERT INTO tmpQACheckList (intBatchID, nvcrBatchName, IntCheckListID, vcrComment)                                       
	SELECT Distinct v_RequestId,v_RequestName,236, CONCAT('Lead Time is ' , ifnull(BCD.nvcrLeadTime,''))
	From  LastResultQACheck  BCD                         
			 WHERE  intDipBagDynamicId = p_RequestRunId;	
	
	Delete From BatchCrawlPNFStopperData
	where intBatchID = v_RequestId;
	
    
	
	insert into BatchCrawlPNFStopperData
	(intBatchId, ncvrBatchName, nvcrComment)
	Select intBatchID, nvcrBatchName, vcrComment	
	From tmpQACheckList; 	
	
	
    Drop Temporary Table If Exists Temp_QACheck1;
	Create Temporary Table Temp_QACheck1
    As
	Select ncvrCheckListName, Status, A.Comment From 
	(
		Select  
			Ifnull(MS.ncvrCheckListName,'') ncvrCheckListName , Case When MS.intCheckList in (235,236,237,238)  Then '' Else 'Fail' End Status, QA.vcrComment Comment
			, MS.intDisplayOrder
		From tmpQACheckList QA  Left Join MstCheckList MS 
		On QA.IntCheckListID = MS.intCheckList And MS.nvcrCheckListType = 'QACheck'
	) A
	Order by intDisplayOrder;
    
    
    Drop Temporary Table If Exists Temp_QACheck2;
	Create Temporary Table Temp_QACheck2
    As
	Select ncvrCheckListName, Status, A.Comment From 
	(		 
		Select Mst.ncvrCheckListName, 'Pass' Status, '' Comment, Mst.intDisplayOrder
		From MstCheckList Mst  WHere Mst.intCheckList not in 
        (Select t.IntCheckListID From tmpQACheckList t)
		And nvcrCheckListType = 'QACheck' And Mst.bitCheckList = 1
	) A
	Order by intDisplayOrder;
	 
    insert into TempQA_ECUBE_MDM_5 (QA_Checks, Status, nvcrComment)
    Select * From Temp_QACheck1
    union 
    Select * From Temp_QACheck2;
	 
    -- Select * From TempQA_ECUBE_MDM_5; 
	
	 
END ;;
