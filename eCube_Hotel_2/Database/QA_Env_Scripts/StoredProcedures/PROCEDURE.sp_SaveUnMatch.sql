DELIMITER ;;

CREATE PROCEDURE `sp_SaveUnMatch`(

In p_HotelRelationId bigint(20),
In p_UserId	int
)
BEGIN

	If exists(Select HotelRelationId From HotelRelation Where HotelRelationId = p_HotelRelationId Limit 1
		) Then
    
    
    
    INSERT INTO Unmatch (`HotelId`,`ComHotelId`,`CreatedBy`,
	`AdminUserId`,`MatchDate`,`MatchingRunId`,`MatchedInStepNo`,
	`MatchingScore`,`HotelNamePer`,`HotelAddressPer`,`GeoCoordinatesPer`,
	`ModifiedBy`,`ModifiedDatetime`,`LastFlagStatus`,`LastFlagStatusDateTime`)
	Select HotelId, HotelRelationComHotelId, p_UserId, null, Now(),
		MatchingRunId, MatchedInStepNo, MatchingScore, 
		HotelNamePer, HotelAddressPer, GeoCoordinatesPer,
		ModifiedBy, ModifiedDatetime, LastFlagStatus,
		LastFlagStatusDateTime 
	From HotelRelation Where HotelRelationId = p_HotelRelationId;

	Delete From HotelRelation Where HotelRelationId = p_HotelRelationId;
    
	   
    End IF;

END ;;
