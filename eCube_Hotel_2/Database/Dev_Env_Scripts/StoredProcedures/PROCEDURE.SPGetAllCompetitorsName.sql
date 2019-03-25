DELIMITER ;;

CREATE PROCEDURE `SPGetAllCompetitorsName`()
BEGIN
		
        select CompetitorId,CompetitorName from tbl_CompetitorMaster
		where Active=1
		order by CompetitorName;       
        
END ;;
