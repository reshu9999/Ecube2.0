DELIMITER ;;

CREATE PROCEDURE `GetTableData_Hotel_Avail_Last_Result_SEC`(
  p_intBatchId INT 
	,p_vcrBatchName VARCHAR(500)
	,p_sdtmDiPBagDynamicRecordDT VARCHAR(50)
	,p_Status VARCHAR(50)
	,p_intDipBagDynamicId INT
	,p_intSourceMDM_BatchesId INT
	,p_dtmTimestamp datetime 
    ,p_bitRenameFlag int 
    ,p_nvcrSupplierID NVARCHAR (500)
    ,p_BitIsPNFStopper NVARCHAR(50)      
    ,p_intpartialuploadid int       
    -- ,OUT p_FileName VARCHAR(500) 
    )
This_SP:BEGIN

 Declare p_FileName nvarchar (50);

/*
 DECLARE p_FileName nvarchar(100);   
 DECLARE v_id INT;   
 declare p_bitRenameFlag int default 0;
declare p_vcrBatchName nvarchar(50) default 'ABCDEFG' ;
declare p_intDipBagDynamicId int; 
declare p_intSourceMDM_BatchesId int ; 
declare p_intBatchId int default 101;
Declare p_sdtmDiPBagDynamicRecordDT nvarchar(50);
DECLARE v_Start VARCHAR(50) DEFAULT 'Start';
declare v_intDipBagDynamicId int DEFAULT 101;
DECLARE v_DipbagDynamicDT DATETIME(3) DEFAULT LEFT(p_sdtmDiPBagDynamicRecordDT, position('.' in p_sdtmDiPBagDynamicRecordDT) - 1); 
Declare p_nvcrSupplierID nvarchar(50) default '';	
declare p_BitIsPNFStopper    tinyint(4) default 0;
 
 declare v_stop nvarchar(50);
 DECLARE v_intStatusId INT DEFAULT 6;
declare p_dtmTimestamp datetime(6); 
declare p_vcrStatus nvarchar (50);
declare v_nvcrSupplierID NVARCHAR (500);
 /*
