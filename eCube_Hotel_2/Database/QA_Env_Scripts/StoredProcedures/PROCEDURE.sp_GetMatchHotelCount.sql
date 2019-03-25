DELIMITER ;;

CREATE PROCEDURE `sp_GetMatchHotelCount`(
	 In p_EntryMode int,
     In p_RunId INT,
     OUT p_ErrorMessage VARCHAR(500),
     OUT p_Status INT
)
BEGIN

DECLARE v_MatchStart DATETIME;
DECLARE v_MatchEnd DATETIME;


IF (p_EntryMode > 0) THEN 

	 
	set p_ErrorMessage = '';
	set p_Status = 0; 

	SELECT RunStartDateTime, RunEndDateTime INTO v_MatchStart, v_MatchEnd 
	FROM MatchingRunMaster  
	WHERE RunId = p_RunId AND MatchingStatusId = 3
	AND RunStartDateTime IS NOT NULL AND RunEndDateTime IS NOT NULL; 

	SELECT MS.`name` AS Supplier, IFNULL(MH2.MatchedCount,0) AS MatchedCount, IFNULL(MH1.HotelsChecked,0) AS HotelsChecked
	FROM 
	(
		SELECT CompetitorId, COUNT(HotelId) AS HotelsChecked
		FROM Hotels MH   
		WHERE CompetitorId NOT IN (0,1) 	 
		GROUP BY MH.CompetitorId 
	)MH1
	LEFT OUTER JOIN 
	(	
		SELECT SecHotels.CompetitorId, COUNT(HR.HotelRelationComHotelId) AS MatchedCount
		FROM HotelRelation HR  
		INNER JOIN Hotels SecHotels  
		ON HR.HotelRelationComHotelId = SecHotels.HotelId  				
		WHERE HR.MatchDate BETWEEN v_MatchStart AND v_MatchEnd	
		GROUP BY SecHotels.CompetitorId 

	)MH2
	ON MH1.CompetitorId = MH2.CompetitorId
	RIGHT JOIN tbl_Competitor MS  
	ON MH1.CompetitorId = MS.Id
	ORDER BY 1;	
 	
	SET p_Status = 1;
	SET p_ErrorMessage = '';    
End IF;
END ;;
