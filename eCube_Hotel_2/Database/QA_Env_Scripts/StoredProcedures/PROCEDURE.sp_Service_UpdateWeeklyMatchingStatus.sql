DELIMITER ;;

CREATE PROCEDURE `sp_Service_UpdateWeeklyMatchingStatus`(	
    IN p_Status INT,       
    IN p_RunId INT
)
BEGIN

-- select * from matchingrunmaster
  					
		IF(p_Status = 6)		-- Matching Fail
			THEN
				UPDATE MatchingRunMaster
				SET MatchingStatusId = 6 , 
					RunEndDateTime = NOW() 					
				WHERE RunId = p_RunId;
		ELSEIF (p_Status = 3)  -- Matching Started
			THEN
				UPDATE MatchingRunMaster
				SET MatchingStatusId = 3,
				RunStartDateTime = NOW() 					
				WHERE RunId = p_RunId AND MatchingStatusId = 2;
		ELSEIF (p_Status = 4)		-- Matching Completed
			THEN
				UPDATE MatchingRunMaster
				SET MatchingStatusId = 4,
					RunEndDateTime = NOW() 					
				WHERE RunId = p_RunId AND MatchingStatusId = 3;
		END IF;	
		
END ;;
