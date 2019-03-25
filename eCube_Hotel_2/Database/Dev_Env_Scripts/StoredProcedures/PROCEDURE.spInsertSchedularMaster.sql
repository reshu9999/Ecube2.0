DELIMITER ;;

CREATE PROCEDURE `spInsertSchedularMaster`(IN StartDate DATE, IN EndDate DATE,TriggerDay varchar(10), Time time,IN ReqID INT)
BEGIN
	
    
    INSERT INTO `eCube_Centralized_DB`.`tbl_ScheduleMaster`
	(
	`StartDate`,
	`EndDate`,
	`TriggerDayDate`,
	`Time`,
	`Active`,
	`SM_ScheduleTypeId`,
	`SM_RequestId`,
	`CreatedDate`
	)
	VALUES
	(
	StartDate,
	EndDate,
	TriggerDayDate,
	Time,
	1,
	1,
	ReqID,
	NOW()
    );

END ;;
