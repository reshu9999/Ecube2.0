DELIMITER ;;

CREATE PROCEDURE `GetCompetitorsByDomains`()
BEGIN
	
    /*Select distinct Com.CompetitorId as Id,Com.CompetitorName as name from tbl_Competitor Com
	inner join tbl_DomainMaster Dom
	on Com.Id = Dom.competitorid
	where Dom.Active =1;
    */
    Select distinct Com.Id as Id,Com.name as name from tbl_Competitor Com
	inner join tbl_DomainMaster Dom
	on -- Com.Id = Dom.competitorid
		Com.Id = Dom.competitorid
	where Dom.Active =1;
END ;;
