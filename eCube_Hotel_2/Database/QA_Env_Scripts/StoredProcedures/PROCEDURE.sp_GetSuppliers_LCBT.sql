DELIMITER ;;

CREATE PROCEDURE `sp_GetSuppliers_LCBT`( 
	 IN  p_SupplierID INT,
IN p_DipBagDynamicId Int  
)
BEGIN 
 
	
	SELECT Id SupplierId, `name` SupplierName 
	FROM tbl_Competitor   
	WHERE Id = p_SupplierID;
    
	SELECT Id SupplierId, `name` SupplierName 
		FROM tbl_Competitor 
		WHERE Id != p_SupplierID;
    
    

	SELECT HotelRelationId, HotelId, HotelRelationComHotelId, 
		isHotelRelationManualMatch, CreatedBy, AdminUserId, 
   MatchDate, 0 as MatchingRunId,0 as MatchedInStepNo,
   0 MatchingScore, 0 HotelNamePer, 0 HotelAddressPer, 
   0 GeoCoordinatesPer ,ModifiedBy,ModifiedDatetime,LastFlagStatus,
		LastFlagStatusDateTime  FROM HotelRelation limit 1;
	
	SELECT ProbableMatchedHotelId,HotelId,ProbableMatchedHotelComHotelId,
		CreatedBy,AdminUserId,MatchDate,MatchingRunId,MatchedInStepNo,
		MatchingScore,MatchType,HotelNamePer,HotelAddressPer,
		GeoCoordinatesPer,ModifiedBy,ModifiedDatetime,LastFlagStatus,
		LastFlagStatusDateTime 
	FROM  ProbableMatchedHotels limit 1; 

END ;;
