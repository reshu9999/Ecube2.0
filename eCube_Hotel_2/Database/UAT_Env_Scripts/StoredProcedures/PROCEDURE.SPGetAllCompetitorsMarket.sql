DELIMITER ;;

CREATE PROCEDURE `SPGetAllCompetitorsMarket`(
IN CompId INT
)
BEGIN
		
        select A.CountryId,CountryCode from tbl_CountryMaster A
        join tbl_CompetitorMaster B on (A.CountryId=B.FK_CountryId)
		where A.Active=1 and B.CompetitorId=compId
		order by CountryCode;       
        
END ;;
