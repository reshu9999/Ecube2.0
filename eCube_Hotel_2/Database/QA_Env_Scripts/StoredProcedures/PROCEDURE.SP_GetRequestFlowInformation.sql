DELIMITER ;;

CREATE PROCEDURE `SP_GetRequestFlowInformation`(IN prmReqId int, IN prmDataSeqNumber int)
BEGIN
/***********************************************************                                             
**          Name            :	SP_GetRequestFlowInformation
**          Description     :   To get data from tables for given Request ID
**          Called by       :  	Code file Name of website OR Service (Consumer.py)
**          Created by      :   Bhavin.Dhimmar
** Example of execution   	:   CALL SP_GetRequestFlowInformation(550,1);
** Input Parameters         :
			prmReqId int
            prmDataSeqNumber int
** Output Parameters        :
**        Date of creation	:	04-APR-2018
Change History    
************************************************************    
#SrNo   Date:           Changed by:         Description:
1      	DD-MMM-YYYY		Developer2			Comment out the where condition
************************************************************/
	Declare varGroupId int default 0;
    Declare varReqRunId int default 0;
    
    If prmDataSeqNumber = 1 then
		SELECT * FROM eCube_Centralized_DB.tbl_RequestMaster where requestid = prmReqId;
    End if;
    
    If prmDataSeqNumber = 2 then
		SELECT * FROM eCube_Centralized_DB.tbl_RequestInputDetails where FK_RequestId = prmReqId;
	End if;
	
    If prmDataSeqNumber = 3 then
		SELECT FK_GroupId into varGroupId FROM eCube_Centralized_DB.tbl_RequestMaster where requestid = prmReqId;
		SELECT * FROM eCube_Centralized_DB.tbl_Field_Group_Master where GroupId = varGroupId;
    End if;
	
    If prmDataSeqNumber = 4 then
		SELECT FK_GroupId into varGroupId FROM eCube_Centralized_DB.tbl_RequestMaster where requestid = prmReqId;
		SELECT * FROM eCube_Centralized_DB.tbl_FieldGroupMappingDetails where FGMD_GroupID  = varGroupId;
    End if;
	
	If prmDataSeqNumber = 5 then
		SELECT * FROM eCube_Centralized_DB.tbl_RequestRunDetail 
		where FK_RequestId = prmReqId order by RequestRunId desc limit 1;
    End if;
	
    If prmDataSeqNumber = 6 then
		SELECT RequestRunId into varReqRunId FROM eCube_Centralized_DB.tbl_RequestRunDetail 
		where FK_RequestId = prmReqId order by RequestRunId desc limit 1;
	
		Select * from eCube_Centralized_DB.tbl_CrawlRequestDetail where RequestRunId = varReqRunId;
	End if;
	
    If prmDataSeqNumber = 7 then
		SELECT RequestRunId into varReqRunId FROM eCube_Centralized_DB.tbl_RequestRunDetail 
		where FK_RequestId = prmReqId order by RequestRunId desc limit 1;
		
		Select * from eCube_Centralized_DB.tbl_ReportRunDetail where RID_RequestRunId = varReqRunId;
	End if;
END ;;
