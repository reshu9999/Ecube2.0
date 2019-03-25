DELIMITER ;;

CREATE PROCEDURE `sp_Service_GetWeeklyMatchingSchedule`(  
    OUT p_ErrMsg  Varchar(500),
    OUT p_Status  TINYINT 
)
BEGIN


                                
DECLARE v_IntervalId int(11);
DECLARE v_WeekDay Varchar(20);
DECLARE v_MatchSchTime VARCHAR(10);
DECLARE v_RunId INT(11);
Declare v_MatchingWorkflowMasterId INT(11) Default 1;

SET p_ErrMsg = '';
SET p_Status = 0;
SET v_IntervalId = 0;
SET v_RunId = 0;

SELECT IntervalID, WeekDay, MatchSchTime, matchingworkflowmasterid 
	INTO v_IntervalId, v_WeekDay, v_MatchSchTime, v_MatchingWorkflowMasterId
FROM MatchingWeeklyInterval  
WHERE Active = 1 AND WeekDay = DAYNAME(NOW());
                           
Delete from MatchingRunMaster;                           
                           
IF (v_IntervalId > 0) THEN
	IF NOT EXISTS (SELECT RunId FROM MatchingRunMaster WHERE MatchingStatusId = 2 limit 1) Then
		
        
        
		SET p_Status = 1;
		INSERT INTO  MatchingRunMaster
		   (`MatchingStatusId`
		   ,`RunStartDateTime`
		   ,`RunEndDateTime`
		   ,`CreatedBy`
		   ,`CreatedDateTime`
		   ,`ModifiedBy`
		   ,`UpdatedDateTime`
		   ,`MatchingWorkflowMasterId`
		   ,`IntervalID`)
		VALUES
		   (2, NOW(), null, 1, NOW(),1, null, 
			v_MatchingWorkflowMasterId, v_IntervalId);

		
		SELECT RunId INTO v_RunId FROM MatchingRunMaster  
		WHERE `MatchingStatusId` = 2  order by RunId desc limit 1;                                                                                
																										
		SELECT v_IntervalId AS IntervalId, v_WeekDay AS  WeekDay, v_MatchSchTime AS MatchSchTime, v_RunId AS RunId;                                                                                          
				
		Truncate Table ProbableMatchedHotels;  
        			 
	END IF;
	 
END IF;

END ;;
