DELIMITER ;;

CREATE PROCEDURE `sp_TruncateMatchingRecords`(
	In p_EntryMode int
)
BEGIN

IF (p_EntryMode > 0) THEN   

delete from ProbableMatchedHotels where ProbableMatchedHotelId  in(

(select A.ProbableMatchedHotelId From 
  (SELECT ProbableMatchedHotelId,ProbableMatchedHotelComHotelId  FROM ProbableMatchedHotels
    WHERE MatchType = 3
  GROUP BY ProbableMatchedHotelId,ProbableMatchedHotelComHotelId) A
 Inner Join

    (SELECT ProbableMatchedHotelId,ProbableMatchedHotelComHotelId  FROM ProbableMatchedHotels
    WHERE MatchType = 4
  GROUP BY ProbableMatchedHotelId,ProbableMatchedHotelComHotelId) B
  
  ON A.ProbableMatchedHotelComHotelId = B.ProbableMatchedHotelComHotelId
 GROUP BY A.ProbableMatchedHotelId
  ));
End IF; 
 -- call `HotelMonitor`.`Delete_Hotels_withsameNameAndWebsitedID_Matched`;
END ;;
