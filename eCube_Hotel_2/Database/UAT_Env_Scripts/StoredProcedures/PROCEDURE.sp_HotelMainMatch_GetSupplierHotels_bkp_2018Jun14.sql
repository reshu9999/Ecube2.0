DELIMITER ;;

CREATE PROCEDURE `sp_HotelMainMatch_GetSupplierHotels_bkp_2018Jun14`( In
                PrimarySupplierId INT(11),
                CityId int(11),
                PrimaryHotelIDs NVARCHAR(4000),
                SecondarySupplierIDs NVARCHAR(1000),
                HotelStatusID NVARCHAR(1000),
                MatchingStatusID NVARCHAR(1000)
)
BEGIN
/***********************************************************                                             
**          Name          :               sp_HotelMainMatch_GetSupplierHotels                                      
**          Description   :              Display Match unmatch records on Manual matching screen 
**          Called by     :               Hotel/views.py -> API : root.py
**          Created by    :               Bhushan Gaud/Vishesh
** Example of execution   :               
call sp_HotelMainMatch_GetSupplierHotels (1, 1, '1', '2','1','1' );

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
1         DD-MMM-YYYY	Developer2                           Comment out the where condition
*********************************************************** */
DROP TEMPORARY TABLE IF EXISTS Temp_MatchingStatus;
DROP TEMPORARY TABLE IF EXISTS Temp_HotelStatus;
DROP TEMPORARY TABLE IF EXISTS Temp_PrimaryHotel;
DROP TEMPORARY TABLE IF EXISTS Temp_SecSupplier;
DROP TEMPORARY TABLE IF EXISTS TempRelation;
DROP TEMPORARY TABLE IF EXISTS TEMP_HotelMatching;



Create Temporary Table Temp_PrimaryHotel(HotelID int); 
Create Temporary Table Temp_MatchingStatus (IntID Int(11),  MatchingStatus Varchar(200));
Create Temporary Table Temp_HotelStatus (StatusID Int(11), HotelStatus Varchar(200));
Create Temporary Table Temp_SecSupplier(SupplierID int); 

If (MatchingStatusID = '') Then
                Insert into Temp_MatchingStatus Values (1, 'Matched');
                Insert into Temp_MatchingStatus Values (2, 'Unmatched');   
End If;


If (HotelStatusID = '') Then
                Insert into Temp_HotelStatus (StatusID, HotelStatus)
    Select HotelStatusID, HotelStatus From  HotelStatus; 
End If;

If (HotelStatusID != '') Then
                Insert into Temp_HotelStatus (StatusID, HotelStatus)
    Select HotelStatusID, HotelStatus From  HotelStatus hs 
    Where hs.HotelStatusID in (HotelStatusID) ; 
End If;

Insert into Temp_PrimaryHotel (HotelID)
Select HotelId From Hotels Where HotelID in (PrimaryHotelIDs); 
 
Insert into Temp_SecSupplier (SupplierID)
Select Id From tbl_Competitor Where Id in (SecondarySupplierIDs); 


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
                                CASE 
                                                 WHEN (isHotelRelationManualMatch=0 ) -- AND IsManualUnmatch=0) 
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
                                FROM HotelRelation AS HotelRel          
                                INNER JOIN 
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
                                                  WHERE HPH.CompetitorId = PrimaryHotelIDs
                                                                                AND HPH.CityId = CityId
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
                                                  WHERE CityId = CityId              
                                ) ComHotel         
                                ON ComHotel.Hotelid = HotelRel.HotelRelationComHotelId
        INNER JOIN tbl_Competitor AS ComSup
                                ON ComHotel.CompetitorId = ComSup.Id;

/* need to R&D for deleting duplicate record
Delete From TempRelation Where HotelRelationId IN
(
	Select A.HotelRelationId  From
	(
					Select  @rownum := @rownum + 1 AS RowID, 
									HotelRelationId
					From TempRelation, (SELECT @rownum := 0) r
	)A
	Where A.RowID > 1
);
        */
        

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
WHERE HPH.CompetitorId = PrimarySupplierId AND HPH.CityId = CityId;

 Select * From TEMP_HotelMatching;

/*
UPDATE  A
SET 
	A.HotelRelationid = TR.HotelRelationid,
	A.Hotelid = TR.Hotelid,
	A.HotelRelationComHotelId = TR.HotelRelationComHotelId ,
	A.UsrId = TR.UsrId,
	A.AdminUsrId = TR.AdminUsrId,
	A.HotelRelationManualMatch = TR.HotelRelationManualMatch,
	A.IsManualUnmatch = TR.IsManualUnmatch,
	A. MatchDate = TR. MatchDate,
	A. UnmatchDate = TR. UnmatchDate,
	A.ComWebSiteHotelId = TR.comhotelcode ,
	A.ComSupplierid = TR.ComSupplierid ,
	A.ComSupplierName = TR.ComSupplierName ,
	A.ComHotelAddress1 = Case When TR.IsManualUnmatch = 0 then TR.ComHotelAddress1 else '' end,
	A.ComHotelAddress2 = Case When TR.IsManualUnmatch = 0 then TR.ComHotelAddress2 else '' end,
	A.ComLatitude = Case When TR.IsManualUnmatch = 0 then TR.ComLatitude else '' end,
	A.ComLongitude = Case When TR.IsManualUnmatch = 0 then TR.comLongitude else '' end,
	A.Comhotel =  TR.Comhotel ,
	A.RelationStatus =  TR.RelationStatus ,
	A.MatchDate = TR.MatchDate, 
	A.UnmatchDate = TR.UnMatchDate,      
	A.MatchUnMatchDate =  TR.UnMatchDate                                         
From TEMP_HotelMatching A
	INNER JOIN TempRelation TR 
	ON A.CityId = TR.CityId 
	AND A.SupplierId = TR.SupplierId 
	AND A.ComSupplierid = TR.ComSupplierid
	AND A.HotelId = TR.HotelId;
*/
/*
                                INSERT TEMP_HotelMatching
                                (
                                                                `HotelRelationId`, `HotelRelationComHotelId`, `HotelRelationManualMatch`, `UsrId`, `AdminUsrId`, `IsManualUnmatch`,
                                                                ` MatchDate`, ` UnmatchDate`, `HotelId`, ` WebSiteHotelId`,`ComWebSiteHotelId`, ` HotelName`, ` HotelAddress1`, ` HotelAddress2`,
                                                                ` Latitude`,` Longitude`,
                                                                `CityId`, `SupplierId`, ComSupplierid, ComSupplierName, Comhotel, ComHotelAddress1, ComHotelAddress2,ComLatitude, ComLongitude, RelationStatus 
                                                                , MatchDate, UnmatchDate, MatchUnMatchDate                           
                                )
                                SELECT 
                                                                HotelRelationid , HotelRelationComHotelId, HotelRelationManualMatch, UsrId, AdminUsrId, IsManualUnmatch,
                                                                MatchDate,  UnmatchDate, HotelId, hotelcode AS  WebSiteHotelId, comhotelcode as [ComWebSiteHotelId],  HotelName,  HotelAddress1,
                                                                HotelAddress2, Latitude,` Longitude`, CityId, SupplierId, ComSupplierid, ComSupplierName, Comhotel, ComHotelAddress1, ComHotelAddress2,ComLatitude,ComLongitude, RelationStatus                  
                                                                , MatchDate, UnmatchDate, MatchUnMatchDate            -- Added By Bhushan Gaud
                                FROM TempRelation TR; WITH(NOLOCK)
                                WHERE TR.HotelRelationId NOT IN(SELECT IFNULL(HotelRelationId,0) FROM TEMP_HotelMatching WITH(NOLOCK))

                                
                                
                                -- Added by Bhushan Gaud Start
                                Delete  From TEMP_HotelMatching Where HotelRelationId in 
                                (
                                                Select T2.HotelRelationId From TEMP T1 Inner Join TEMP T2 
                                                On T1.HotelId = T2.HotelId And T1.MatchDate = T2.UnmatchDate And T1.SupplierId = T2.SupplierId  And T1.ComSupplierid = T2.ComSupplierid
                                                And T1.IsManualUnmatch = 0 And T2.IsManualUnmatch = 1
                                );
*/                           
        /* Need to do r & D for Row number partition
                                Delete From TEMP Where HotelRelationId in 
                                (
                                                Select HotelRelationId From 
                                                (
                                                                -- SELECT ROW_NUMBER() Over(Partition BY hotelID, SupplierId Order By MatchUnMatchDate desc) RowNo ,  * FROM #TEMP
                                                                --             Where HotelRelationId != 0
                                                                                Select 
                                                                                ROW_NUMBER() Over(Partition BY T1.hotelID, T1.SupplierId Order By T1.MatchUnMatchDate desc) RowNo ,
                                                                  T2.*     From #TEMP T1 Inner Join #TEMP T2 
                                                                On T1.HotelId = T2.HotelId And T1.MatchDate != T2.UnmatchDate And T1.SupplierId = T2.SupplierId And T1.ComSupplierid = T2.ComSupplierid
                                                                And T1.IsManualUnmatch = 0 And T2.IsManualUnmatch = 1
                                                                                
                                                                                
                                                ) A -- Where A.RowNo > 1
                                );
                                -- Added by Bhushan Gaud End */
                                
/*                           
                                Alter Table TEMP_HotelMatching Add Column sdtLastAppearnceDate DateTime  
*/                           
                                /*Need creat function
        Update TEMP_HotelMatching  Set sdtLastAppearnceDate = [HotelMonitor].[fn_GetHotelLastApperanceDate](HotelRelationComHotelId);
                                */
/*                           
                                Update TEMP_HotelMatching  Set RelationStatus = 'Unmatched' Where RelationStatus Is Null;
*/
                                /* Need to do r & D for Row number partition
                                Delete; A From
                                (
                                                Select ROW_NUMBER() Over(Partition by Hotelid Order by sdtLastAppearnceDate Desc) Sr_No,
                                                                * From #temp Where  RelationStatus = 'Unmatched'
                                ) A
                                Where Sr_No > 1
        */

                                
/*
                                SELECT  DISTINCT
                                                                A.SRNO AS Counter,
                                                                IFNULL(A.HotelRelationid,0) HotelRelationid, 
                                                                A.Hotelid, 
                                                                A.HotelRelationComHotelId, 
                                                                A.UsrId, 
                                                                A.AdminUsrId,
                                                                A.HotelRelationManualMatch, 
                                                                A.IsManualUnmatch, 
                                                                A. MatchDate,
                                                                A. UnmatchDate,
                                                                A. Latitude,
                                                                A. Longitude,
                                                                A. HotelName, 
                                                                A. Hoteladdress1, 
                                                                IFNULL(A. WebSiteHotelId,'NA') AS hotelcode, 
                                                                IFNULL(A.ComWebSiteHotelId,'NA') AS comhotelcode, 
                                                                A. Hoteladdress2, 
                                                                A.SupplierId, 
                                                                A.CityId,                               
                                                                A.ComSupplierid, 
                                                                B. SupplierName AS ComSupplierName,
                                                                
                                                                A.Comhotel, 
                                                                A.ComHotelAddress1, 
                                                                A.ComHotelAddress2,   
                                                                A.ComLatitude,
                                                                A.ComLongitude,             
                                                                IFNULL(A.RelationStatus,'Unmatched'   ) RelationStatus,
                                                                MHS.vcrStatus HotelStatus,-- Added by Bhushan Gaud for two more filter Hotel and matching status
                                                                
                                                                
                                
                                                                DATE_FORMAT(A.sdtLastAppearnceDate ,105) AS LastAppearance 
                                
                                                                
                                FROM TEMP_HotelMatching A INNER JOIN tbl_com B
                                                ON A.ComSupplierid = B.SupplierId 
                                                -- Added by Bhushan Gaud For two more filter Start
                                                Inner Join HotelMonitor.MSTHotel MH 
                                                On MH.HotelId = A.HotelId 
                                                Inner Join HotelMonitor.MstHotelStatus MHS
                                                On MH.StatusID = MHS.StatusID
                                Where IFNULL(A.RelationStatus,'Unmatched'); in 
                                (Select  MatchingStatus From #Temp_MatchingStatus Where ID in (Select Items From split(p_MatchingStatusID,',')))
                                And MH.StatusID in (Select Items From dbo.split(p_HotelStatusID,','))--                and A.HotelRelationComHotelId<>0
                                                -- Added by Bhushan Gaud For two more filter End
                                
                                ORDER BY A. HotelName ASC
                                */
                                DROP TABLE TEMP_HotelMatching;
                                DROP TABLE TempRelation;


END ;;
