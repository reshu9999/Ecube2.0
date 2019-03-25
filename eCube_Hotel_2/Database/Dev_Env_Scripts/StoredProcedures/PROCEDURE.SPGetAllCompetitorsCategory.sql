DELIMITER ;;

CREATE PROCEDURE `SPGetAllCompetitorsCategory`(
IN compeid INT,
IN marketid INT
)
BEGIN
	select L1_CategoryId,L1_CategoryName from tbl_Category_L1 where FK_CompetitorId=compeid
    and FK_CountryId=marketid and Active=1
    order by L1_CategoryName;
	

END ;;
