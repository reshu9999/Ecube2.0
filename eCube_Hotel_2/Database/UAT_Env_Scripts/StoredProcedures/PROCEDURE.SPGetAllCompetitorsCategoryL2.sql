DELIMITER ;;

CREATE PROCEDURE `SPGetAllCompetitorsCategoryL2`(
IN L1CategoryId INT
)
BEGIN
	select L2_CategoryId,L2_CategoryName from tbl_Category_L2 where 
    FK_L1CategoryId=L1CategoryId and Active=1
    order by L2_CategoryName;
	

END ;;
