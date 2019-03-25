DELIMITER ;;

CREATE PROCEDURE `sp_GetReportUploadUpdate_BKP_27_JUN_18`(
	p_RequestId INT,
	p_RequestRunId INT,
	p_nvcrSupplierID longtext 
)
BEGIN

	DECLARE v_nvcrBatchName VARCHAR(100);	 
    declare v_nvcrReportEmailId NVARCHAR(100);
	declare v_batchId int;
    Declare v_NvcrAdltChild Longtext Default '';
	Declare v_NvcrAdlt Longtext Default '';
	Declare v_NvcrChild Longtext Default '';
    Declare v_CompetitorIds Longtext Default '';
 

	Drop Temporary Table If Exists tmpReportUploadUpdate; 
	CREATE Temporary  TABLE tmpReportUploadUpdate(intBatchId INT,nvcrBatchName VARCHAR(100),nvcrComment VARCHAR(100), 
		IntStatus Int Default 0, IntCheckListID int Default 0); 
	
    Drop Temporary Table If Exists Temp_Supplier; 
	CREATE Temporary  TABLE Temp_Supplier(intSupplierID Int);
    
	call sp_split(p_nvcrSupplierID, ',');
    
    Insert into Temp_Supplier
    Select items from SplitValue;   
    
     
    Drop Temporary Table If Exists temp_BatchCrawlData; 
	CREATE Temporary TABLE temp_BatchCrawlData
    As
	Select Distinct nvcrHotelName, Cast(dtmCrawlDateTime As DATE) dtmCrawlDateTime    
		From BatchCrawlData  Where intDiPBagDynamicId = p_RequestRunId
	And intSupplierId in (Select intSupplierID From Temp_Supplier);	
	
	
    Set  v_nvcrReportEmailId = '';
	Set  v_batchId=0;
	set v_nvcrBatchName='';
	
	
	Select d.FK_RequestId, b.RequestName Into v_batchId, v_nvcrBatchName
	From RequestRunDetail d inner join tbl_RequestMaster b 
				on d.FK_RequestId = b.RequestId
	where d.RequestRunId = p_RequestRunId;
		
	
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Lead Time column is null/blank', 1 IntStatus, 114 
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                           
   	And ifnull(BCD.nvcrLeadTime,'')='' limit 1;
   	
    
   	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select p_RequestId,v_nvcrBatchName,'Event Type column is null/blank', 1 IntStatus, 115  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                           
   	And ifnull(BCD.nvcrEventType,'')='' Limit 1;
	
    
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select p_RequestId,v_nvcrBatchName,'Money Rate is null/blank ', 1 IntStatus, 116  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.Price,'')='' Limit 1;

	
		 
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select p_RequestId,v_nvcrBatchName,'City is null/blank ', 117  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.City,'')='' Limit 1;    
    
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select p_RequestId,v_nvcrBatchName,'Country is null/blank ', 118  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.Country,'')='' Limit 1;
        
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select p_RequestId,v_nvcrBatchName,'State is not null/blank ', 119  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.State,'') !='' Limit 1;
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Rcode is not null/blank ', 120  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And (ifnull(BCD.Rcode,'')!='' And ifnull(BCD.Rcode,'')!='0') Limit 1;
	
    
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select p_RequestId,v_nvcrBatchName,'CancellationPolicy is not null/blank ', 240   
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.CancellationPolicy,'') !='' Limit 1;


		
	
		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select p_RequestId,v_nvcrBatchName,'CancellationPolicy is not null/blank ', 121   
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.CancellationPolicy,'')!='' And
		Company in (Select `name` From tbl_Competitor  WHere Id Not In (1, 6, 25)) 
        Limit 1; 
 
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Uniquecode is not null/blank ', 241  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.Uniquecode,'')!='' Limit 1;

	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Uniquecode is not null/blank ', 122  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.Uniquecode,'')!='' And
	Company in (Select `name` From tbl_Competitor  WHere Id Not In (1, 6, 25)) 
    Limit 1;
	
   
   
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select p_RequestId,v_nvcrBatchName,'ComOfici is not null/blank ', 242  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.ComOfici,'')!='' Limit 1;


 
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'ComOfici is not null/blank ', 215  
	 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.ComOfici,'')!='' And
		Company in (Select `name` From tbl_Competitor  WHere Id Not In (1, 6, 25)) 
	Limit 1;
	
	
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Classification is not null/blank ', 226  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.Classification,'')!='' And
		Company in (Select `name` From tbl_Competitor  WHere Id Not In (1, 6, 25)) 
	Limit 1;
    
		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'SellingPriceMandatory is not null/blank ', 227  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.nvcrSellingPriceMandatory,'')!='' And
		Company in (Select `name` From tbl_Competitor  WHere Id Not In (1, 6, 25)) 
        Limit 1;

	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'ComCanal is not null/blank ', 243  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.ComCanal,'')!='' Limit 1;

 
	 
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'ComCanal is not null/blank ', 123  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.ComCanal,'')!='' And
		Company in (Select `name` From tbl_Competitor  WHere Id Not In (1, 6, 25)) 
	Limit 1;

	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select p_RequestId,v_nvcrBatchName,'ComNeta is not null/blank ', 244  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.ComNeta,'')!=''  Limit 1;
        


	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'ComNeta is not null/blank ', 124  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.ComNeta,'')!='' And
		Company in (Select `name` From tbl_Competitor  WHere Id Not In (1, 6, 25)) 
        Limit 1;

	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'POS is null/blank ', 125  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.PointOfSale,'')='' Limit 1;
		

	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Multiple POS exist', 224  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		 Having Count(Distinct ifnull(BCD.PointOfSale,'')) > 1 Limit 1;
         
		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Multiple Country exist', 225  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
		 Having Count(Distinct ifnull(BCD.Country,'')) > 1    Limit 1;                     
		 
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Daily Rate is null/blank ', 1 IntStatus, 126  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.DailyRate,'')=''  Limit 1;	 
	
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'HotelName is null/blank ', 1 IntStatus, 127  
		from temp_BatchCrawlData BCD                              
		where ifnull(BCD.nvcrHotelName,'')='' Limit 1;
	
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Currency is null/blank ', 1 IntStatus, 128  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.Currency,'')=''  Limit 1;
		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)                       
    SELECT Distinct v_batchId,v_nvcrBatchName, 'Hotel Name contain junk characters i:e ',0 IntStatus ,71 
	from temp_BatchCrawlData  BCD                            
	where nvcrHotelName Like '%<%' Or nvcrHotelName Like '%>%' Or nvcrHotelName Like '%=%';
	
	
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)                       
    SELECT Distinct v_batchId,v_nvcrBatchName, 'Hotel Name contain Blank i:e ',1 IntStatus ,71 
	from temp_BatchCrawlData  BCD                            
	where  Ifnull(nvcrHotelName,'')='';


	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
    Select   v_batchId,v_nvcrBatchName,'Promotion Description contain HTML characters',0 IntStatus,95 
	 from LastResultQACheck  BCD                            
	where intDiPBagDynamicId = p_RequestRunId 
	And (nvcrPromotionDescription Like '%<%' Or nvcrPromotionDescription Like '%>%' Or nvcrPromotionDescription Like '%=%')
    Limit 1;
		
		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)                                            
    Select   v_batchId,v_nvcrBatchName, 'Promotion Description contain only special characters',0 IntStatus,96
	from LastResultQACheck  BCD                             
	where intDiPBagDynamicId = p_RequestRunId 
	And nvcrPromotionDescription Not Like  '%a-zA-Z%' And nvcrPromotionDescription Not Like  '%0-9%'
    Limit 1;
 
		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)  -- -balnk or null YOO                                          
    Select v_batchId,v_nvcrBatchName, 'Room Type contain only special characters',0 IntStatus,93
	 from LastResultQACheck  BCD
	where intDiPBagDynamicId = p_RequestRunId 
	and  RoomType Not Like  '%a-z%' and RoomType not like '%A-Z%'  And RoomType Not Like  '%0-9%' 
	Limit 1; 
	
	 			
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)  -- -balnk or null YOO                                          
    Select   v_batchId,v_nvcrBatchName, 'Room Type contain blank characters',1 IntStatus,93
	 from LastResultQACheck  BCD                         
	where intDiPBagDynamicId = p_RequestRunId 
	and ifnull(BCD.RoomType,'')=''
	Limit 1; 	
	
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select   v_batchId,v_nvcrBatchName, 'Room Type contain HTML characters',0 IntStatus,90
	from LastResultQACheck  BCD
	where intDiPBagDynamicId = p_RequestRunId And (RoomType Like '%<%' Or RoomType Like '%>%' Or RoomType Like '%=%')
	Limit 1;
		
	
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select v_batchId,v_nvcrBatchName, 'Invalid wrong Currency' , 0 IntStatus, 221                       
	 from LastResultQACheck  BCD                            
    where intDiPBagDynamicId = p_RequestRunId
    And (Currency Like '%<%' Or Currency Like '%>%'  Or Currency Like '%=%' 
    Or (Currency Not Like  '%a-zA-Za-zA-Za-zA-Z%' And Currency Not Like  '%0-9%')
    Or (Currency Not Like  '%a-zA-Za-zA-Za-zA-Z%' And Currency Like  '%0-9%')
    Or (Char_length(rtrim(Ltrim(Rtrim(BCD.Currency)))) <  3))
    Limit 1;
    
   
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  v_batchId,v_nvcrBatchName, 'Invalid Currency' , 1 IntStatus, 221                       
	from LastResultQACheck  BCD                            
	where intDiPBagDynamicId = p_RequestRunId
	and  ( (Char_length(rtrim(Ltrim(Rtrim(BCD.Currency)))) <  3)
	or ifnull(BCD.Currency,'')='') Limit 1;



	
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Room Type is null/blank ', 1 IntStatus, 133  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.RoomType,'')='' Limit 1;
		
	 
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Promotion is other than Y/N', 0 IntStatus, 135  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.nvcrPromotion,'') Not in ('Y','N') Limit 1;
		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Promotion : Value Y but blank desc', 0 IntStatus, 233  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.nvcrPromotion,'') in ('Y') And Ifnull(nvcrPromotionDescription,'') = ''
		Limit 1;
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Promotion : Value N but Non blank desc', 0 IntStatus, 234  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.nvcrPromotion,'') in ('N') And Ifnull(nvcrPromotionDescription,'') != ''
	Limit 1;		
	 
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Board value Contain other than BB,HB,FB,RO and AI', 1 IntStatus, 137  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And IFNULL(BCD.Board,'') Not in ('BB','HB','FB','RO','AI')
	Limit 1;
	
     
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)                          
	Select v_batchId,v_nvcrBatchName,'MNYRate contain zero Value', 0 IntStatus, 138
	 from LastResultQACheck  BCD
	where intDiPBagDynamicId = p_RequestRunId  And (Price = '0' or Price = '0.00')
    Limit 1;

	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)                          
	Select v_batchId,v_nvcrBatchName,'MNYRate contain single digit Value', 0 IntStatus, 248
	 from LastResultQACheck  BCD                            
	where intDiPBagDynamicId = p_RequestRunId  And CHAR_LENGTH(RTRIM(Price))=1
    Limit 1;

	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)                          
	Select   v_batchId,v_nvcrBatchName,'MNYRate contain null/blank Value', 1 IntStatus, 138
	from LastResultQACheck  BCD
	where intDiPBagDynamicId = p_RequestRunId  and IFNULL(BCD.Price,'') ='' 
    Limit 1;

	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)                          
	Select   v_batchId,v_nvcrBatchName,'Daily Rate contain zero Value', 0 IntStatus, 139
	from LastResultQACheck  BCD
	where intDiPBagDynamicId = p_RequestRunId  and (DailyRate = '0.00' or DailyRate = '0')
	Limit 1;

	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)                          
	Select v_batchId,v_nvcrBatchName,'Daily Rate contain null/blank Value', 1 IntStatus, 139
	 from LastResultQACheck  BCD
	where intDiPBagDynamicId = p_RequestRunId  and IFNULL(BCD.DailyRate,'') ='' Limit 1;

		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Account Name is blank for primary supplier', 1 IntStatus, 140  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And IFNULL(nvcrAccountName,'') = '' And
		Company in (Select `name` From tbl_Competitor  WHere Id in (1, 6, 25))
        Limit 1;
		
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Account Name is not blank for secondary supplier', 1 IntStatus, 141  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And IFNULL(nvcrAccountName,'') != '' And
		Company in (Select `name` From tbl_Competitor  WHere Id Not In (1, 6, 25)) 
        Limit 1;	
 
		
		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'OpaqueRate is not blank for secondary supplier', 0 IntStatus, 143  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And IFNULL(nvcrOpaqueRate,'') != '' And
		Company in (Select `name` From tbl_Competitor  WHere Id Not In (1, 6, 25)) 
	Limit 1;
		
	 	
		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select   p_RequestId,v_nvcrBatchName,'Integration is not blank for secondary supplier', 0 IntStatus, 145  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And IFNULL(Integration,'') != '' And
		Company in (Select `name` From tbl_Competitor  WHere Id Not In (1, 6, 25)) 
        Limit 1;
		
	 	
		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Commision is not blank for secondary supplier', 0 IntStatus, 147  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And IFNULL(nvcrCommision,'') != '' And
		Company in (Select `name` From tbl_Competitor  WHere Id Not In (1, 6, 25))
        Limit 1;
		
	 	
		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'SellingPrice is not blank for secondary supplier', 0 IntStatus, 149  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And IFNULL(nvcrSellingPrice,'') != '' And
		Company in (Select `name` From tbl_Competitor  WHere Id Not In (1, 6, 25)) 
        Limit 1;
		
		
	 	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'NetPrice is not blank for secondary supplier', 0 IntStatus, 151  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And IFNULL(nvcrNetPrice,'') != '' And
		Company in (Select `name` From tbl_Competitor  WHere Id Not In (1, 6, 25))
        Limit 1;
		
			
	 	
		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'ContractName is not blank for secondary supplier', 0 IntStatus, 156  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And IFNULL(ContractName,'') != '' And
		Company in (Select `name` From tbl_Competitor  WHere Id Not In (1, 6, 25))
        Limit 1;
		
		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select   p_RequestId,v_nvcrBatchName,'Supplier Hotel URL is blank for Muchoviaje and Travel republic.', 0 IntStatus, 153  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And IFNULL(nvcrSupplierHotelURL,'') = '' And 
	hotelid > 0 And  
		Company in (Select `name` From tbl_Competitor  WHere Id In (77,80))  Limit 1;

	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select   p_RequestId,v_nvcrBatchName,'Supplier Hotel URL is not blank for secondary supplier.', 0 IntStatus, 154  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And IFNULL(nvcrSupplierHotelURL,'') != '' And
		Company Not in (Select `name` From tbl_Competitor  WHere Id In (77,80,10,7)) Limit 1;
	
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select   p_RequestId,v_nvcrBatchName,'RoomAvailability is not blank for secondary supplier', 0 IntStatus, 155  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And IFNULL(nvcrRoomAvailability,'') != '' And
		Company in (Select `name` From tbl_Competitor  WHere Id Not In (1, 6, 25,2,20)) Limit 1;
		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'RoomAvailability is null/blank for primary supplier', 0 IntStatus, 228  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And IFNULL(nvcrRoomAvailability,'') = '' And
		Company in (Select `name` From tbl_Competitor  WHere Id In (1, 6, 25)) Limit 1;
		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select p_RequestId,v_nvcrBatchName,'Invalid value in BreakFast.', 0 IntStatus, 157  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And IFNULL(Ltrim(Rtrim(BreakFast)),'') != 'No'   Limit 1; 
		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Invalid value in Available.', 0 IntStatus, 158  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And IFNULL(Ltrim(Rtrim(Availability)),'') != 'Available' Limit 1; 	

	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select p_RequestId,v_nvcrBatchName,'Invalid value in Status.', 0 IntStatus, 159  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And IFNULL(Ltrim(Rtrim(Status)),'') != 'Completed'  Limit 1; 
    

	 
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID) 
    Select  v_batchId,v_nvcrBatchName, 'Dynamic Property is not blank for supplier other than GMH1,GMH3' , 0 IntStatus, 160                
	 from LastResultQACheck  BCD                          
    where intDiPBagDynamicId = p_RequestRunId And Company Not IN (Select `name` From tbl_Competitor  WHere Id in (10,63) )
	And IFNULL(nvcrDynamicProperty,'') != '' Limit 1;
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID) 
	Select  v_batchId,v_nvcrBatchName, 'Dynamic Property is blank for supplier GMH1,GMH3' , 0 IntStatus, 161                      
	 from LastResultQACheck  BCD                             
    where intDiPBagDynamicId = p_RequestRunId And Company IN (Select `name` From tbl_Competitor  WHere Id in (10,63) )
	And IFNULL(nvcrDynamicProperty,'') = ''  Limit 1;
	
	
	Select Distinct Concat(Ifnull(A.Adult,'')  , ' Adt'), Concat(Ifnull(C.Child,'') , ' Chd') 
		Into v_NvcrAdlt, v_NvcrChild 
	 From tbl_hotelrequestinputdetails BD Left join Adults A 
     On BD.AdultId = A.AdultId Left join Children C
     On BD.ChildID = C.ChildID
     WHere RequestId = p_RequestId;
     
	Set v_NvcrAdltChild = CONCAT(v_NvcrAdlt , v_NvcrChild);
	
	If (v_NvcrChild != '0 Chd')
	Then
		Set v_NvcrAdltChild = CONCAT(v_NvcrAdlt , ' + ' , v_NvcrChild);
	Else
		Set v_NvcrAdltChild = v_NvcrAdlt;  
	End if;	
		
		
	if  (v_NvcrAdltChild='4 Adt')
	then
		set v_NvcrAdltChild='2 Adt + 2 Chd';
	end if;			
	if  (v_NvcrAdltChild='3 Adt')
	then
		set v_NvcrAdltChild='2 Adt + 1 Chd';
	end if;	
		
	if  (v_NvcrAdltChild='2 Adt')
	then
		set v_NvcrAdltChild='2 Adt';
	end if;		
	
	if  (v_NvcrAdltChild='1 Adt')
	then
		set v_NvcrAdltChild='1 Adt';
	end if;
	
	
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select Distinct p_RequestId,v_nvcrBatchName,CONCAT('Invalid Adult' , nvcrAdult), 220  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And IFNULL(nvcrAdult,'') != v_NvcrAdltChild;
	
	
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select p_RequestId,v_nvcrBatchName,'TimeStamp is not as current date', 168  
		from temp_BatchCrawlData BCD                              
		where Cast(dtmCrawlDateTime As Date)!= Cast(NOW() As Date) Limit 1;
        
	
    
	Select Group_Concat(Distinct CompetitorIds) into v_CompetitorIds 
		From  tbl_hotelrequestinputdetails Where RequestId = p_RequestId; 
        
	call sp_Split(v_CompetitorIds,',');
    
    Drop Temporary Table if Exists Temp_Competitor;
    Create Temporary Table Temp_Competitor
    As
    Select items As SupplierId, `name` SupplierName 
		from SplitValue S inner join tbl_Competitor C
	on S.items = C.Id;
    
    
    
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select Distinct p_RequestId,v_nvcrBatchName,CONCAT('Competitor does not exist in batch.' , SupplierName), 169  
		 from LastResultQACheck BCD Right Join Temp_Competitor BD 
		On BCD.Company = BD.SupplierName  
		And intDiPBagDynamicId = p_RequestRunId 
		Where  BCD.Company Is Null;
	
	
	
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)	
	Select  p_RequestId,v_nvcrBatchName,CONCAT('Missing Date: ' , Date_format(CheckInDate, 106)), 170  
		 from LastResultQACheck BCD 
		   Right Join 
	(Select CheckInDate, RequestId From tbl_HotelCrawlRequestDetail RDD  Where RequestId = p_RequestId) BD
		On Cast(BCD.Dates As Date) = Cast(BD.CheckInDate As Date)
		And intDiPBagDynamicId = p_RequestRunId 
		Where  BCD.Dates Is Null And 
		BD.RequestId = p_RequestId;
		 
	
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)	
	Select  p_RequestId,v_nvcrBatchName,'Night does not exist in batch/Incorrect nights selected.', 171  
		 from LastResultQACheck BCD Right Join 
		(Select RentalLength, RequestId From tbl_HotelCrawlRequestDetail RDD  Where RequestId = p_RequestId) BDD
		On BCD.Nights = BDD.RentalLength
		And intDiPBagDynamicId = p_RequestRunId  
		Where  BCD.Nights Is Null Limit 1;
	
	
	
	
		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)	
	Select Distinct p_RequestId,v_nvcrBatchName, CONCAT('Missing Search: ' , Date_format(BD.CheckInDate, 106) , ' Supplier:- ' , BD.CompetitorName , '. Nights:- ' , BD.RentalLength), 239  
		 from LastResultQACheck BCD 
			  Right Join 
		(Select RentalLength, CheckInDate, CompetitorName, RequestId From tbl_HotelCrawlRequestDetail RDD  Where RequestId = p_RequestId) BD 
			On BCD.Company = BD.CompetitorName  
			And Cast(BCD.Dates As Date)= Cast(BD.CheckInDate As Date)
			And BCD.Nights = BD.RentalLength
			And intDiPBagDynamicId = p_RequestRunId
			Where  BCD.Dates Is Null Or BCD.Company Is Null;
	
	 
    
		
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Direct Payment is other than Y or N', 172  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And IFNULL(nvcrDirectPayment,'') Not in ('Y', 'N')  Limit 1;
    
    
    
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select p_RequestId,v_nvcrBatchName,'Price is non numeric', 0 IntStatus, 173  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And fn_IsNumeric(Price) = 0 Limit 1; 
    
     INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Hotel order appreance is non numeric', 174  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And fn_IsNumeric(nvcrHotelCount) = 0 Limit 1;
    
    
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Hotel order appreance is Null/Blank', 175  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And Ifnull(nvcrHotelCount,'') = '' Limit 1;     
    
    
    INSERT INTO tmpReportUploadUpdate (intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select   p_RequestId,v_nvcrBatchName,'Daily Rate is Non numeric', 0 IntStatus, 176   -- YOO 
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
   And fn_IsNumeric(DailyRate) = 0 Limit 1;
    
    
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)     -- -YOO
	Select  p_RequestId,v_nvcrBatchName,'Daily Rate is Greater than mnyrate for ', 0 IntStatus, 177  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
		And fn_IsNumeric(DailyRate) = 1
		And DailyRate != ''
    And cast(DailyRate as decimal(11,2)) > cast(Price as decimal(11,2))
    Limit 1;
       
    
     INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Tax is Non numeric', 178  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
   And fn_IsNumeric(Tax) = 0
    and TAX IS NOT NULL 
    And  Tax != '' Limit 1;   
    
    
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Hotel ID is negative for primary supplier', 179  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
    And Company in (Select `name` From tbl_Competitor  WHere Id In (1,25,6))
    And (HotelId < 0 or  IFNULL(HotelId,'') = '') Limit 1;
    
 

	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    Select  v_batchId,v_nvcrBatchName, 'Hotel Code is blank', 180                       
	 from LastResultQACheck  BCD                             
    where intDiPBagDynamicId = p_RequestRunId 
	And IFNULL(HotelCode,'') = '' Limit 1;
	 
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    Select  v_batchId,v_nvcrBatchName, 'Hotel Code is non numeric', 181
	 from LastResultQACheck  BCD                            
    where intDiPBagDynamicId = p_RequestRunId 
	And fn_IsNumeric(HotelCode) = 0 Limit 1;
	
	-- changes done by Bhushan gaud for 
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    Select  v_batchId,v_nvcrBatchName, 'Hotel Code is negative for primay supplier blank', 182                       
	 from LastResultQACheck  BCD                            
    where intDiPBagDynamicId = p_RequestRunId 
    And fn_IsNumeric(HotelCode) = 1
	And IFNULL(HotelCode,'') < 0
	And Company in (Select `name` From tbl_Competitor  WHere Id In (1, 25,6)) Limit 1;
	
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    Select  v_batchId,v_nvcrBatchName, 'Hotel ID is non numeric', 183                       
	 from LastResultQACheck  BCD                            
    where intDiPBagDynamicId = p_RequestRunId 
	And fn_IsNumeric(HotelId) = 0 Limit 1;
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    Select  v_batchId,v_nvcrBatchName, 'Hotel ID is negative for primay supplier', 184                       
	 from LastResultQACheck  BCD                           
    where intDiPBagDynamicId = p_RequestRunId 
	And IFNULL(HotelId,'') < 0
	And Company in (Select `name` From tbl_Competitor  WHere Id In (1,6,25)) Limit 1;
	
	  
 
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select Distinct p_RequestId,v_nvcrBatchName,CONCAT('Tax is present for unmatch hotels for ', Company), 186  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId  
		And HotelId < 0 
    And Company in (Select `name` From tbl_Competitor  WHere Id In (20, 2, 59))
    And Ifnull(Tax,'') != '' And Ifnull(Tax,'') != '0';
    
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID)
	Select p_RequestId,v_nvcrBatchName,'Supplier Hotel name column is blank.', 1 IntStatus, 187  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId  
    And Ifnull(Supplier,'') = ''  Limit 1;
    
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    SELECT Distinct v_batchId,v_nvcrBatchName, CONCAT('Supplier is blank for website TR, TC, TA, Expedia or Alpha or Mucho for match hotels' , Company), 188                       
	 from LastResultQACheck  BCD                             
    where intDiPBagDynamicId = p_RequestRunId 
    And Company in (Select `name` From tbl_Competitor  WHere Id in (39,77,80,83,2,84)) 
    And Ltrim(Rtrim(Ifnull(strSupplier,''))) = '' and HotelId > 0;
    
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    SELECT v_batchId,v_nvcrBatchName, CONCAT('Supplier is not blank for Other website' , Company), 189                       
	 from LastResultQACheck  BCD                             
    where intDiPBagDynamicId = p_RequestRunId 
    And Company Not in (Select `name` From tbl_Competitor  WHere Id in (39,77,80,83,2,84)) 
    And Ltrim(Rtrim(Ifnull(strSupplier,''))) != '' ;
    
    
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    Select  v_batchId,v_nvcrBatchName, 'Page URL is blank.', 190
	 from LastResultQACheck  BCD                            
    where intDiPBagDynamicId = p_RequestRunId 
    And Company Not in (Select `name` From tbl_Competitor  WHere Id in (60,19,10,56)) 
      And Ltrim(Rtrim(Ifnull(Replace(PageURL,'=HYPERLINK("","info")',''),''))) = '' 
      Limit 1;
    
    
 
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    Select  v_batchId,v_nvcrBatchName, 'Event type exist other than free and fixed', 192
	 from LastResultQACheck  BCD                             
    where intDiPBagDynamicId = p_RequestRunId 
    And ifnull(BCD.nvcrEventType,'') Not in ('Free', 'Fixed') Limit 1;
	 
	 
    
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  v_batchId,v_nvcrBatchName, 'Invalid Lead Time', 193
	 from LastResultQACheck  BCD   inner join tbl_HotelCrawlRequestDetail D 
	On BCD.intDiPBagDynamicId = D.RequestRunId inner join tbl_RequestMaster MB 
	On D.RequestId = MB.RequestId inner join  MstLeadTimeTemplate MT 
	On MB.RequestName = MT.nvcrBatchName 
	And BCD.Dates = Case When MT.smdtCheckindate != '1900-01-01 00:00:00' 
		Then cast(MT.smdtCheckindate As DATE) Else TIMESTAMPADD(Day, MT.intLTime,cast(MT.nvcrBookingDate As date)) End
	And BCD.Nights = MT.intNights
	And BCD.nvcrLeadTime != MT.nvcrLeadTime
	And MT.nvcrBatchName = v_nvcrBatchName
	WHERE  BCD.intDiPBagDynamicId = p_RequestRunId Limit 1;
    
    
    
    
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  v_batchId,v_nvcrBatchName, 'Invalid Event type', 194
		from LastResultQACheck  BCD  inner join tbl_HotelCrawlRequestDetail D 
		On BCD.intDiPBagDynamicId = D.RequestRunId inner join tbl_RequestMaster MB 
		On D.RequestId = MB.RequestId inner join  MstLeadTimeTemplate MT 
		On MB.RequestName = MT.nvcrBatchName 
		And BCD.nvcrLeadTime = MT.nvcrLeadTime
		And BCD.nvcrEventType != MT.nvcrEventType
		And MT.nvcrBatchName = v_nvcrBatchName
		WHERE  BCD.intDiPBagDynamicId = p_RequestRunId 
		Limit 1;
	
    
    
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	SELECT Distinct v_batchId,v_nvcrBatchName, CONCAT('Multiple Event Type exist:- ' , Dates) , 195
		from LastResultQACheck  BCD                            
		where intDiPBagDynamicId = p_RequestRunId 
		Group by Company, Dates, Nights
		Having Count(Distinct nvcrEventType) > 1;
    
    
     
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  v_batchId,v_nvcrBatchName, CONCAT('Multiple Event Type exist' , Dates), 222
		from LastResultQACheck  BCD                           
		where intDiPBagDynamicId = p_RequestRunId 
		Group by Company, Dates
		Having Count(Distinct Nights) > 1
	And Count(Distinct nvcrEventType) =  1 Limit 1;
   
  
    
    
    
    INSERT INTO tmpReportUploadUpdate (intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    Select  v_batchId,v_nvcrBatchName, 'Invalid Competitor Hotel For Primary', 229
	 from LastResultQACheck  BCD                            
    where intDiPBagDynamicId = p_RequestRunId 
    And  IFNULL(nvcrCompetitorHotelID,'') != ''  
    And Company in (Select `name` From tbl_Competitor  WHere Id In (1, 6, 25)) Limit 1;
    

    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    Select v_batchId,v_nvcrBatchName, 'Invalid Competitor Hotel For Secondary', 230
	 from LastResultQACheck  BCD                            
    where intDiPBagDynamicId = p_RequestRunId 
    And  IFNULL(nvcrCompetitorHotelID,'') = ''  
    And Company Not in (Select `name` From tbl_Competitor  WHere Id In (1, 6, 25,10))
    Limit 1;
    
     INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    Select  v_batchId,v_nvcrBatchName, 'Junk Value in Competitor For Primary', 231
	 from LastResultQACheck  BCD                            
    where intDiPBagDynamicId = p_RequestRunId 
    And  IFNULL(nvcrCompetitorHotelID,'') != ''  
    And Company in (Select `name` From tbl_Competitor  WHere Id In (1, 6, 25)) 
    And  nvcrCompetitorHotelID Not Like  '%a-zA-Za-zA-Za-zA-Z%' And nvcrCompetitorHotelID Not Like  '%0-9%' 
	Limit 1;
	
        
    
    
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    Select v_batchId,v_nvcrBatchName, 'Multiple city exist', 200
	 from LastResultQACheck  BCD                           
    where intDiPBagDynamicId = p_RequestRunId 
    Having Count(Distinct City) > 1 Limit 1; 

    
     
    
    
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    SELECT Distinct v_batchId,v_nvcrBatchName, Dates , 202
	 from LastResultQACheck  BCD                            
    where intDiPBagDynamicId = p_RequestRunId 
    Group by Company, Dates, Nights
    Having Count(Distinct nvcrLeadTime) > 1;
    
    
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	SELECT Distinct v_batchId,v_nvcrBatchName, Dates, 213
	 from LastResultQACheck  BCD                             
    where intDiPBagDynamicId = p_RequestRunId 
    Group by Company, Dates
    Having Count(Distinct Nights) > 1
    And Count(Distinct ifnull(nvcrLeadTime,'')) = 1;
      
    
	
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    Select  v_batchId,v_nvcrBatchName, 'Multiple Adult exist', 203
	 from LastResultQACheck  BCD                            
    where intDiPBagDynamicId = p_RequestRunId 
	Having Count(Distinct BCD.nvcrAdult) > 1 Limit 1;
	
	
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID) -- -YOO
    Select  v_batchId,v_nvcrBatchName, 'Multiple currency exist' , 0 IntStatus, 204
	 from LastResultQACheck  BCD                            
    where intDiPBagDynamicId = p_RequestRunId 
    Group by Company
	Having Count(Distinct BCD.Currency) > 1 Limit 1;
    
	 
   
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    Select  v_batchId,v_nvcrBatchName, 'Tax is greater than price', 207
	 from LastResultQACheck  BCD                            
    where intDiPBagDynamicId = p_RequestRunId 
     And fn_IsNumeric(Ifnull(Tax,0)) = 1
     And fn_IsNumeric(Ifnull(Price,0)) = 1
    And Cast(Ifnull(Tax,0) As Decimal(18,4))> Cast(Ifnull(Price,0) As Decimal(18,4)) 
    Limit 1;
   
 
   
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    SELECT Distinct v_batchId,v_nvcrBatchName, CONCAT('Multiple account present for :' , Company) , 208
	 from LastResultQACheck  BCD                           
    where intDiPBagDynamicId = p_RequestRunId 
    Group by Company
    Having Count(Distinct nvcrAccountName) > 1;
    
     
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    Select  v_batchId,v_nvcrBatchName, CONCAT('Multiple Supplier present against:' , nvcrAccountName), 223
	 from LastResultQACheck  BCD
    where intDiPBagDynamicId = p_RequestRunId 
    And Company in (Select `name` From tbl_Competitor  WHere Id In (1,6,25))
    Group by nvcrAccountName
    Having Count(Distinct Company) > 1 Limit 1;
    
    
	
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Room Code is null/blank ', 209  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.RoomCode,'') =''  Limit 1;
	
 
 	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	SELECT Distinct v_batchId,v_nvcrBatchName
    , CONCAT('Single Room Code present :-' , A.Company , '-' , A.Dates ,'-' , A.Nights ,'-',RoomCode)
    , 210
	   From 
	(select Company, Dates, Nights, RoomCode  from LastResultQACheck  BCD                             
    where intDiPBagDynamicId = p_RequestRunId) A 
	inner join  
	(select Company, Dates, Nights  from LastResultQACheck  `BCD`                            
    where intDiPBagDynamicId = p_RequestRunId 
    and BCD.Company not in ('TripAdvisor') 
    Group by Company, Dates, Nights
    Having Count(Distinct RoomCode) =1)B
    On A.Company=B.Company   
    and A.Dates=B.Dates
    and A.Nights=B.Nights;
    

	-- -Add new condition on 30-12-2016 as per ops prachi 

	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select p_RequestId,v_nvcrBatchName,'Room Code is SGL other than primary ', 246  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId     
		and GetNumbersFromText(nvcrAdult)>'1' and RoomCode='SGL'
    and Company  not in (Select `name` From tbl_Competitor  WHere Id In (1, 6, 25))  Limit 1;
     


    
    INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
    Select Distinct v_batchId,v_nvcrBatchName
    ,CONCAT('Matching hotel does not exist' , B.Dates , '-' , B.Company) , 211  
    From   
	(
		Select Distinct HotelId, Dates, Company  from LastResultQACheck where intDiPBagDynamicId = p_RequestRunId And  HotelId > 0
	) A
	Right Join 
	(
		Select Distinct  Dates, Company  from LastResultQACheck  where intDiPBagDynamicId = p_RequestRunId 
	) B On A.Dates = B.Dates And A.Company = B.Company
	Group by  B.Dates, B.Company
	Having COUNT(HotelId) = 0;
	
    
    Call sp_split('1EST|2EST|3EST|4EST|5EST|6EST|7EST|H1_5|H2_5|H3_5|H4_5|H5_5|H6_5|H7_5|Pendi','|');
    
	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntCheckListID)
	Select  p_RequestId,v_nvcrBatchName,'Invalid start rating.', 212  
		 from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId                              
		And ifnull(BCD.StarRating,'') Not In (
	Select items From SplitValue
	) Limit 1;
		
	

	-- -----Add new two conditions for REVUKTR  as  per ops prachi 

	IF exists (Select  Company  from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId  and   Company = 'TravelRepublic' Limit 1) Then

	INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID) 
		Select v_batchId,v_nvcrBatchName, 'account name against primary for TR batch is not â€˜REVTRUK', 0 IntStatus, 247 
		from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId
		and nvcrAccountName != 'REVTRUK'
		and Company = 'Hotelbeds' Limit 1;

	END If; 
        
        
	IF not exists (Select  Company  from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId       
			and   Company = 'TravelRepublic' Limit 1) Then 	             
		INSERT INTO tmpReportUploadUpdate(intBatchId,nvcrBatchName,nvcrComment, IntStatus, IntCheckListID) 
		  Select v_batchId,v_nvcrBatchName, 'account name against primary is â€˜REVTRUK', 0 IntStatus, 249 
		   from LastResultQACheck BCD Where intDiPBagDynamicId = p_RequestRunId
		and nvcrAccountName = 'REVTRUK'
		 and Company = 'Hotelbeds'
         Limit 1;

	END If; 

    
    Drop temporary Table if Exists Temp_MandoryCheck1;
    Create temporary table Temp_MandoryCheck1
    As
	Select  
	ncvrCheckListName, `Status`, A.Comment, A.IntStatus 
	From 
	(
		Select  Ifnull(MS.ncvrCheckListName,'') ncvrCheckListName , Case when IntCheckListID = 169 Then 'Warning' Else 'Fail' End Status, QA.nvcrComment Comment, QA.IntStatus
		, MS.intDisplayOrder
		From tmpReportUploadUpdate QA  Left Join MstCheckList MS 
		On QA.IntCheckListID = MS.intCheckList And nvcrCheckListType = 'BatchStop'
		 
	)A
	Order by intDisplayOrder;
    
    
    Drop temporary Table if Exists Temp_MandoryCheck2;
    Create temporary table Temp_MandoryCheck2
    As
	Select  
	ncvrCheckListName, `Status`, A.Comment, A.IntStatus 
	From 
	(
		 
		Select Mst.ncvrCheckListName, 'Pass' Status, '' Comment, 0  IntStatus, Mst.intDisplayOrder
		From MstCheckList Mst  WHere Mst.intCheckList not in (Select t.IntCheckListID From tmpReportUploadUpdate t )
		And nvcrCheckListType = 'BatchStop'
		And Mst.bitCheckList = 1
	)A
	Order by intDisplayOrder;
	
	
	Drop Temporary Table If Exists TempQAStop_ECUBE_MDM_5;
    Create Temporary Table TempQAStop_ECUBE_MDM_5
    As
	Select ncvrCheckListName QA_Checks, `Status`, `Comment` nvcrComment,IntStatus  From 
	(
		Select ncvrCheckListName, `Status`, `Comment`,IntStatus From Temp_MandoryCheck1
		Union 
		Select ncvrCheckListName, `Status`, `Comment`,IntStatus From Temp_MandoryCheck2
	) A;

	
	Select * From TempQAStop_ECUBE_MDM_5;
	 
 
END ;;
