DELIMITER ;;

CREATE PROCEDURE `spInsertNewRequest`(
IN FileName varchar(2000), 
IN RequestTitle VARCHAR(30),
IN RequestDesc VARCHAR(50),
IN User_ID INT,
IN BLiID INT,
OUT ReqID VARCHAR(50)
)
BEGIN
		INSERT INTO `eCube_Centralized_DB`.`tbl_RequestMaster`
		(
			`RequestFile`,
            `RequestName`,
			`RequestDescription`,
            `FK_BliId`,
			`CreatedBy`,
			`CreatedDatetime`
		)
		VALUES
		(
			FileName,
			RequestTitle,
            RequestDesc,
            BLiID,
			User_ID,
			Now()
		);
        

		Select RequestId INTO ReqID from eCube_Centralized_DB.tbl_RequestMaster 
        where CreatedBy = User_ID
        order by RequestId DESC
		Limit 1;
        
        select ReqID;


END ;;
