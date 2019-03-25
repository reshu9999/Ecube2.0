DELIMITER ;;

CREATE PROCEDURE `sp_GetDetailsToSendMatchingMail`(	
     
)
BEGIN
	
	DECLARE v_SendMatchingMail TINYINT;
	DECLARE v_RunMatchingAtFixTime TINYINT;
	DECLARE v_RunMatchingTime varchar(20);
	DECLARE v_MatchingMailPath VARCHAR(255);
	DECLARE v_CrawlControllerMailTo VARCHAR(1000);
	DECLARE v_CrawlerCode varchar(10);
	DECLARE v_SendBatchWiseMatchingMail Tinyint;	
	
	 
	
	SELECT  CrawlerCode,
			IFNULL(SendMatchingMail,0),
			IFNULL(RunMatchingAtFixTime,1),
		 Ifnull(RunMatchingTime,'23'),
		 ifnull(MatchingMailPath,''),
		 IFNULL(CrawlControllerMailTo,''),
		 SendBatchWiseMatchingMail INTO 
	v_CrawlerCode, v_SendMatchingMail, v_RunMatchingAtFixTime, 
    v_RunMatchingTime, v_MatchingMailPath, v_CrawlControllerMailTo, 
    v_SendBatchWiseMatchingMail
	FROM ProcessInfo
	where Processid = 1;
	
     
    
    
	SELECT 	v_CrawlerCode `Process`,
			v_SendMatchingMail SendMatchingMail, 
			v_RunMatchingAtFixTime RunMatchingAtFixTime,
			v_RunMatchingTime RunMatchingTime,
			v_MatchingMailPath TemplatePath,
			v_CrawlControllerMailTo CrawlControllerMailTo,
			v_SendBatchWiseMatchingMail SendBatchWiseMatchingMail;
	
	
	
	 

END ;;
