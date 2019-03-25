DELIMITER ;;

CREATE PROCEDURE `sp_HotelMainMatch_GetSupplierHotels`( In
                                p_PrimarySupplierId INT(11),
                                p_CityId int(11),
                                p_PrimaryHotelIDs NVARCHAR(4000),
                                p_SecondarySupplierIDs NVARCHAR(1000),
                                p_HotelStatusID NVARCHAR(1000),
                                p_MatchingStatusID NVARCHAR(1000)
)
BEGIN
/***********************************************************                                             
**          Name          :               sp_HotelMainMatch_GetSupplierHotels                                      
**          Description   :              Display Match unmatch records on Manual matching screen 
**          Called by     :               Hotel/views.py -> API : root.py
**          Created by    :               Bhushan Gaud/Vishesh
** Example of execution   :               
call sp_HotelMainMatch_GetSupplierHotels (1, 40, '86380', '19','','' );

** Input Parameters       :               
                PrimarySupplierId INT(11),
                CityId int(11),
                PrimaryHotelIDs NVARCHAR(4000),
                SecondarySupplierIDs NVARCHAR(1000),
                HotelStatusID NVARCHAR(1000),
                MatchingStatusID NVARCHAR(1000)

** Output Parameters        :
**        Date of creation      :               26-Apr-2018
Change History    
************************************************************    
#SrNo     Date:         Changed by:                          Description:
1         DD-MMM-YYYY     Developer2                           Comment out the where condition
*********************************************************** */



DROP TEMPORARY TABLE IF EXISTS TempRelation;
DROP TEMPORARY TABLE IF EXISTS TEMP_HotelMatching; 



 
	DROP TEMPORARY TABLE IF EXISTS Temp_MatchingStatus;
	Create Temporary Table Temp_MatchingStatus (IntID Int(11),  MatchingStatus Varchar(200));
	If (p_MatchingStatusID = '') Then
		Insert into Temp_MatchingStatus Values (1, 'Matched');
		Insert into Temp_MatchingStatus Values (2, 'Unmatched');   
	Else
		Call sp_split(p_MatchingStatusID,',');    
		Insert into Temp_MatchingStatus 	
		Select items, case when items = 1 Then 'Matched' Else 'Unmatched' End IntID from SplitValue;
	End If;
	 
 
	
    Call sp_split(p_HotelStatusID,',');
	DROP TEMPORARY TABLE IF EXISTS Temp_HotelStatus;
    Create Temporary Table Temp_HotelStatus (StatusID Int(11), HotelStatus Varchar(200));
	Insert into Temp_HotelStatus
    Select HotelStatusID, HotelStatus From  HotelStatus Where HotelStatusID in 
	(Select items from SplitValue); 





If (p_HotelStatusID = '') Then
	Insert into Temp_HotelStatus (StatusID, HotelStatus)
	Select HotelStatusID, HotelStatus From  HotelStatus; 
End If;

Call sp_split(p_PrimaryHotelIDs,',');
DROP TEMPORARY TABLE IF EXISTS Temp_PrimaryHotel;
Create Temporary Table Temp_PrimaryHotel(HotelID int); 
Insert into Temp_PrimaryHotel (HotelID)
Select HotelId From Hotels Where HotelID in (Select items from SplitValue);
 

Call sp_split(p_SecondarySupplierIDs,',');
DROP TEMPORARY TABLE IF EXISTS Temp_SecSupplier;
Create Temporary Table Temp_SecSupplier(SupplierID int);
Insert into Temp_SecSupplier (SupplierID)
Select items from SplitValue;
 


Drop Temporary Table If Exists TempRelation;   
Create Temporary Table TempRelation   
SELECT  HotelRel.HotelRelationid, 
		HotelRel.Hotelid, 
        HotelRel.HotelRelationComHotelId, 
        HotelRel.CreatedBy, 
        HotelRel.AdminUserId,
		HotelRel.isHotelRelationManualMatch, 
        -- 0 IsManualUnmatch, 
        HotelRel.MatchDate as  MatchDate,
		-- null as  UnmatchDate,            
		MH.HotelName, MH.Hoteladdress1, 
        IFnull(MH.WebSiteHotelId,'NA') AS hotelcode, 
        MH.Hoteladdress2, MH.CompetitorId, MH.CityId,    
		MH.Longitude,MH.Latitude,         
		ComSup.Id AS ComSupplierid, 
        ComSup.`name` AS ComSupplierName,
        IFnull(ComHotel.WebSiteHotelId,'NA') AS comhotelcode,    
		ComHotel.HotelName AS Comhotel, 
        ComHotel.Hoteladdress1 AS ComHotelAddress1, 
        ComHotel.Hoteladdress2  AS ComHotelAddress2,
		ComHotel.Longitude comLongitude,
        ComHotel.Latitude ComLatitude, 
		CASE WHEN (isHotelRelationManualMatch=0 ) -- AND IsManualUnmatch=0) 
			 OR (isHotelRelationManualMatch=1 ) -- AND IsManualUnmatch=0) 
             THEN 'Matched'
			WHEN (isHotelRelationManualMatch=0 ) -- AND IsManualUnmatch=1) 
			OR (isHotelRelationManualMatch=1) -- AND IsManualUnmatch=1) 
            THEN 'Unmatched'                   
		END AS RelationStatus 
		-- , HotelRel.MatchDate MatchDate -- Added By Bhushan Gaud
		-- , HotelRel.UnmatchDate UnMatchDate -- Added By Bhushan Gaud
	   ,  HotelRel.MatchDate  MatchUnMatchDate -- Case When HotelRel.IsManualUnmatch = 0 Then HotelRel.MatchDate 
                                                   -- Else IFnull(HotelRel.UnmatchDate, '1900-01-01') End MatchUnMatchDate  -- Added By Bhushan Gaud
                                               -- MatchUnMatchDate      
		FROM HotelRelation AS HotelRel INNER JOIN 
        (
			SELECT 
				HPH.HotelId, 
				WebSiteHotelId, 
				HotelName, 
				HotelAddress1, 
				HotelAddress2, 
				CityId, 
				CompetitorId, 
				CreatedBy,
				Longitude,
				Latitude                               
			FROM Hotels AS HPH   
				INNER JOIN  Temp_PrimaryHotel PR
				ON HPH.HotelId = PR.HotelID
			WHERE  HPH.CityId = p_CityId
		)MH                      
		ON HotelRel.HotelId = MH.HotelId 
		INNER JOIN 
		(
			  SELECT 
				HSH.HotelId, 
				WebSiteHotelId, 
				HotelName, 
				HotelAddress1, 
				HotelAddress2, 
				CityId, 
				CompetitorId, 
				CreatedBy,
				Longitude,
				Latitude                               
			  FROM Hotels AS HSH   
				INNER JOIN Temp_SecSupplier SecSup
				ON SecSup.SupplierID = HSH.CompetitorId             
			  WHERE CityId = p_CityId              
		) ComHotel         
		ON ComHotel.Hotelid = HotelRel.HotelRelationComHotelId
        INNER JOIN tbl_Competitor AS ComSup
		ON ComHotel.CompetitorId = ComSup.Id;
  
   
  
    DROP TEMPORARY TABLE IF EXISTS TempDeleteDuplicate;
	Create Temporary Table  TempDeleteDuplicate
	(`HotelId` bigint(20) NOT NULL);
  
  	Set @rn1 = 1;
	Set @HotelId = 0;
	Set @HotelRelationComHotelId = 0;
	Set @HotelRelationId = 0;
	Set @CompetitorId = 0;   
    
	Truncate Table TempDeleteDuplicate;    
    Insert into TempDeleteDuplicate (HotelId)
    Select B.HotelId From 
    (
		Select 
		@rn1 := 
			if(@HotelId = A.HotelId, 
				If(@HotelRelationComHotelId = A.HotelRelationComHotelId,@rn1,@rn1 +1)
			,  1) As Rank, 
			@HotelId := A.HotelId,
			@HotelRelationComHotelId := A.HotelRelationComHotelId,
			@HotelRelationId := A.HotelRelationId,
            A.HotelId
		From (
		SELECT   HotelId, HotelRelationComHotelId, HotelRelationId
			FROM TempRelation  
			ORDER BY  HotelId, HotelRelationComHotelId ASC , HotelRelationId DESC
		) A
    ) B Where Rank > 1;
     
    
    
	DELETE T 
	FROM TempRelation T 
	INNER JOIN TempDeleteDuplicate D                                                 
	ON T.HotelId = D.HotelId;
  

CREATE TEMPORARY TABLE TEMP_HotelMatching
(
	SRNO int unique key auto_increment ,
	`HotelRelationId` int  NULL,
	`HotelRelationComHotelId` int  NULL,
	`HotelRelationManualMatch` Tinyint  NULL,
	`UsrId` int  NULL,
	`AdminUsrId` int  NULL,
	`IsManualUnmatch` Tinyint  NULL,
	-- `MatchDate` varchar(30)  NULL,
	-- `UnmatchDate` varchar(30) NULL,
	`HotelId` int NOT NULL,
	`WebSiteHotelId` nvarchar(50) NULL,
	`ComWebSiteHotelId` nvarchar(50) NULL,
	`HotelName` nvarchar(512) NOT NULL,
	`HotelAddress1` nvarchar(255) NULL,
	`HotelAddress2` nvarchar(255) NULL,                                                     
	`Latitude` nvarchar(255) NULL,                                                   
	`Longitude` nvarchar(255) NULL,
	`CityId` int NOT NULL,
	`SupplierId` int NOT NULL,
	ComSupplierid   int NOT NULL,
	ComSupplierName NVARCHAR(255),
	Comhotel nvarchar(512) NULL,
	ComHotelAddress1 nvarchar(255) NULL,
	ComHotelAddress2 nvarchar(255) NULL,
	ComLatitude nvarchar(255) NULL,                                                            
	ComLongitude nvarchar(255) NULL,
	RelationStatus NVARCHAR(50) NULL,
	`MatchDate` DateTime ,  
	`UnmatchDate` DateTime ,  
	MatchUnMatchDate DateTime  
); 
    

INSERT INTO TEMP_HotelMatching
(
	`HotelRelationId`, `HotelRelationComHotelId`, `HotelRelationManualMatch`, `UsrId`, `AdminUsrId`, `IsManualUnmatch`,
	`MatchDate`, `UnmatchDate`, `HotelId`, `WebSiteHotelId`,`ComWebSiteHotelId`, `HotelName`, `HotelAddress1`, `HotelAddress2`,
	`Latitude`,`Longitude`,
	`CityId`, `SupplierId`, ComSupplierid, ComSupplierName, Comhotel, ComHotelAddress1, ComHotelAddress2,ComLatitude,ComLongitude, RelationStatus     
)

SELECT 
	0 HotelRelationid , 0 HotelRelationComHotelId, 0 HotelRelationManualMatch, 0 UsrId, 0 AdminUsrId, 0 IsManualUnmatch,
	NULL MatchDate, NULL UnmatchDate, HPH.HotelId, HPH.WebSiteHotelId,null ComWebSiteHotelId, HPH.HotelName, HPH.HotelAddress1,
	HPH.`HotelAddress2`,HPH.Latitude,HPH.Longitude, HPH.CityId, HPH.CompetitorId, B.SupplierID AS ComSupplierid, NULL ComSupplierName, NULL Comhotel,
	NULL ComHotelAddress1, NULL ComHotelAddress2,null ComLatitude,null ComLongitude, NULL RelationStatus        
FROM Hotels HPH 
  INNER JOIN  Temp_PrimaryHotel PR
  ON HPH.HotelId=PR.HotelID     
  CROSS JOIN Temp_SecSupplier B                                           
WHERE HPH.CompetitorId = p_PrimarySupplierId AND HPH.CityId = p_CityId;

  

    	

      
	UPDATE  TEMP_HotelMatching A INNER JOIN TempRelation TR 
		ON A.CityId = TR.CityId 
		AND A.SupplierId = TR.CompetitorId  -- change to int Supllierid 
		AND A.ComSupplierid = TR.ComSupplierid
		AND A.HotelId = TR.HotelId
	SET 
	A.HotelRelationid = TR.HotelRelationid,
	A.Hotelid = TR.Hotelid,
	A.HotelRelationComHotelId = TR.isHotelRelationManualMatch ,
	A.UsrId = TR.CreatedBy,
	A.AdminUsrId = TR.AdminUserId,
	A.HotelRelationManualMatch = TR.isHotelRelationManualMatch,
	-- A.IsManualUnmatch = TR.IsManualUnmatch, as per bhushan commented this code 
	A. MatchDate = TR. MatchDate,
   --  A. UnmatchDate = TR. UnmatchDate,           --change as per bhushan commented this code 
	A.ComWebSiteHotelId = TR.comhotelcode ,
	A.ComSupplierid = TR.ComSupplierid ,
	A.ComSupplierName = TR.ComSupplierName ,
   --  A.ComHotelAddress1 = Case When TR.IsManualUnmatch = 0 then TR.ComHotelAddress1 else '' end,
	-- A.ComHotelAddress2 = Case When TR.IsManualUnmatch = 0 then TR.ComHotelAddress2 else '' end,
	-- A.ComLatitude = Case When TR.IsManualUnmatch = 0 then TR.ComLatitude else '' end,
   --  A.ComLongitude = Case When TR.IsManualUnmatch = 0 then TR.comLongitude else '' end,
	A.Comhotel =  TR.Comhotel ,
	A.RelationStatus =  TR.RelationStatus ,
	A.MatchDate = TR.MatchDate; 
               --  A.UnmatchDate = TR.UnMatchDate,      
               --  A.MatchUnMatchDate =  TR.UnMatchDate;          
               


	Drop temporary table if exists TEMP_HotelMatching_TEMP;
	CREATE TEMPORARY TABLE TEMP_HotelMatching_TEMP LIKE TEMP_HotelMatching;
	INSERT INTO TEMP_HotelMatching_TEMP SELECT * FROM TEMP_HotelMatching;

                
	INSERT TEMP_HotelMatching
	(
		`HotelRelationId`, `HotelRelationComHotelId`, `HotelRelationManualMatch`, `UsrId`, `AdminUsrId`, -- `IsManualUnmatch`,-- commented as per bhavin
		`MatchDate`,  `HotelId`, `WebSiteHotelId`,`ComWebSiteHotelId`, `HotelName`, `HotelAddress1`, `HotelAddress2`,
		`Latitude`,`Longitude`,
		`CityId`, `SupplierId`, ComSupplierid, ComSupplierName, Comhotel, ComHotelAddress1, ComHotelAddress2,ComLatitude, ComLongitude, RelationStatus 
		,   MatchUnMatchDate     -- MatchDate not in TEMP struc  -- UnmatchDate,                    
	)
	SELECT 
		HotelRelationid , HotelRelationComHotelId, isHotelRelationManualMatch, CreatedBy, AdminUserId, -- IsManualUnmatch,      -- commented as per bhavin             
		MatchDate,   HotelId, hotelcode AS  WebSiteHotelId, comhotelcode as ComWebSiteHotelId,  HotelName,  HotelAddress1,
		HotelAddress2, Latitude,`Longitude`, CityId, CompetitorId, ComSupplierid, ComSupplierName, Comhotel, ComHotelAddress1, ComHotelAddress2,ComLatitude,ComLongitude, RelationStatus                  
		,   MatchUnMatchDate      -- UnmatchDate,,  -- commented as per bhavin          -- Added By Bhushan Gaud
	FROM TempRelation TR
	WHERE TR.HotelRelationId NOT IN(SELECT IFNULL(HotelRelationId,0) FROM TEMP_HotelMatching_TEMP);

          

-- Select * From TEMP_HotelMatching;

 
	Drop temporary table if exists TEMP_HotelMatching_TEMP1;
	CREATE TEMPORARY TABLE TEMP_HotelMatching_TEMP1 LIKE TEMP_HotelMatching;
	INSERT INTO TEMP_HotelMatching_TEMP1 SELECT * FROM TEMP_HotelMatching;


	 

	Delete  From TEMP_HotelMatching Where HotelRelationId in 
	(
		Select T2.UnmatchId From TEMP_HotelMatching_TEMP1 T1 Inner Join Unmatch T2 
		On T1.HotelId = T2.HotelId 
		And T1.MatchDate = T2.MatchDate 
		-- And T1.CompetitorId = T2.SupplierId   -- need to do work on this
		-- And T1.ComSupplierid = T2.ComSupplierid 
		-- And T1.IsManualUnmatch = 0 And T2.IsManualUnmatch = 1
	);

               
              
              
 
 
 

 
	Alter Table TEMP_HotelMatching Add Column sdtLastAppearnceDate DateTime;  
	Update TEMP_HotelMatching  Set sdtLastAppearnceDate = fn_GetHotelLastApperanceDate(HotelRelationComHotelId);
	Update TEMP_HotelMatching  Set RelationStatus = 'Unmatched' Where RelationStatus Is Null;
 
		/* Need to do r & D for Row number partition
		Delete; A From
		(
			Select ROW_NUMBER() Over(Partition by Hotelid Order by sdtLastAppearnceDate Desc) Sr_No,
			* From #temp Where  RelationStatus = 'Unmatched'
		) A
		Where Sr_No > 1     
        
		*/

	Set @rn1 = 1;
	Set @sdtLastAppearnceDate = now();
	Set @Hotelid = 0;
	 
    
    
    Truncate Table TempDeleteDuplicate;
    
    INsert into TempDeleteDuplicate (HotelId)
    Select B.HotelId From 
    (
		Select 
		@rn1 := 
			if(@Hotelid = A.Hotelid , 
				If(@sdtLastAppearnceDate = A.sdtLastAppearnceDate,@rn1,@rn1 +1)
			,  1) As Rank,  
		 
			@sdtLastAppearnceDate := A.sdtLastAppearnceDate,		 
			@HotelId := A.HotelId,
            A.Hotelid
		From (
		SELECT   HotelId, sdtLastAppearnceDate
			FROM TEMP_HotelMatching  
			ORDER BY  HotelId asc, sdtLastAppearnceDate Desc
		) A
    ) B Where Rank > 1;


    DELETE TH 
	FROM TEMP_HotelMatching TH 
	INNER JOIN TempDeleteDuplicate T                                                 
	ON TH.HotelId = T.HotelId;



  -- Select * From TEMP_HotelMatching;	
 
 
	SELECT  DISTINCT
			-- A.SRNO AS Counter,
			IFNULL(A.HotelRelationid,0) HotelRelationid, 
			
			A.HotelRelationComHotelId, 
            A.HotelRelationManualMatch, 
			A.UsrId, 
			A.AdminUsrId,
			
			A.IsManualUnmatch, 
			'' MatchDate, -- A.MatchDate,
			'' UnmatchDate, -- A.UnmatchDate,
            A.Hotelid,
            
            IFNULL(A. WebSiteHotelId,'NA') AS hotelcode, 
            IFNULL(A.ComWebSiteHotelId,'NA') AS comhotelcode, 
			A.HotelName, 
            A.Hoteladdress1, 
			A.Hoteladdress2, 
			A.Latitude,
			A.Longitude,
		    A.CityId,   
			A.ComSupplierid, 
			
			
			A.SupplierId, 
			                            
			
			B.`name` AS ComSupplierName,
			
			A.Comhotel, 
            
			A.ComHotelAddress1, 
			A.ComHotelAddress2,   
			A.ComLatitude,
			A.ComLongitude,             
			IFNULL(A.RelationStatus,'Unmatched'   ) RelationStatus,
            
			MHS.HotelStatus HotelStatus,-- Added by Bhushan Gaud for two more filter Hotel and matching status
			
			

			DATE_FORMAT(A.sdtLastAppearnceDate ,105) AS LastAppearance
            
				FROM TEMP_HotelMatching A INNER JOIN tbl_Competitor B
		ON A.ComSupplierid = B.Id 		 
		
        Inner Join Hotels MH 
		On MH.HotelId = A.HotelId 
		Left Join HotelStatus MHS
		On MH.HotelStatusId = MHS.HotelStatusId
	Where IFNULL(A.RelationStatus,'Unmatched') in (Select  MatchingStatus From Temp_MatchingStatus)
	And Ifnull(MH.HotelStatusId,7) in (Select T.StatusID From Temp_HotelStatus T)
	ORDER BY A. HotelName ASC 
    ;
                                 
	-- Select  * From Temp_HotelStatus;
                              
                               


END ;;
