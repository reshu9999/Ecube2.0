DELIMITER ;;

CREATE PROCEDURE `sp_SaveExcatMatch`(

In p_HotelId bigint(20),
In p_ComHotelId bigint(20),
In p_UserId	int


)
BEGIN

	If not exists(Select * From HotelRelation Where HotelId = p_HotelId
		And HotelRelationComHotelId = p_ComHotelId
    ) Then
        
    INSERT INTO `HotelRelation` 
	(`HotelId`,`HotelRelationComHotelId`,
	`isHotelRelationManualMatch`,`CreatedBy`,`AdminUserId`,`MatchDate`,
	`MatchingRunId`,`MatchedInStepNo`,`MatchingScore`,`HotelNamePer`,
	`HotelAddressPer`,`GeoCoordinatesPer`,`ModifiedBy`,`ModifiedDatetime`,
	`LastFlagStatus`,`LastFlagStatusDateTime`)
	Select p_HotelId, p_ComHotelId, 1, p_UserId, p_UserId, Now(),
		null MatchingRunId, null MatchedInStepNo, null MatchingScore, 
		null HotelNamePer, null HotelAddressPer, null GeoCoordinatesPer,
		null ModifiedBy, null ModifiedDatetime, 0 LastFlagStatus,
		null LastFlagStatusDateTime;
	
    
    End IF;

END ;;
