DELIMITER ;;

CREATE PROCEDURE `sp_DeleteDuplicateProbableHotels`(

	In p_EntryMode int
)
BEGIN

Declare v_RunId Int Default 0;

IF (p_EntryMode > 0) THEN 
    

	-- --Added by Bhushan Gaud on 09 Nov 2017 as facing issue with matching date time start
	
	Select RunId Into v_RunId  From  MatchingRunMaster  
		order by 1 desc limit 1;
  

	Update HotelRelation B
    Inner Join HotelRelation A	
    On A.HotelRelationComHotelId = B.HotelRelationComHotelId
	And A.HotelId = B.HotelId
    And Ifnull(B.MatchingRunId,0) < v_RunId
    And Ifnull(A.MatchingRunId,0) = v_RunId
    
    Set B.MatchingRunId = (Ifnull(A.MatchingRunId,1) * -1),
				 B.GeoCoordinatesPer = A.GeoCoordinatesPer,
				 B.HotelAddressPer = A.HotelAddressPer,
				 B.HotelNamePer = A.HotelNamePer,
				 B.MatchingScore = A.MatchingScore,
				 B.MatchedInStepNo = A.MatchedInStepNo;


	Delete A 
	From HotelRelation A
		Inner Join HotelRelation B	
	On A.HotelRelationComHotelId = B.HotelRelationComHotelId
	And A.HotelId = B.HotelId
    And A.MatchingRunId = v_RunId
    And B.MatchingRunId < v_RunId;
	 
	-- --Added by Bhushan Gaud on 09 Nov 2017 as facing issue with matching date time End



	
	Delete   From HotelRelation   Where  HotelRelationId In
	(
		Select HotelRelationId From 
        (
			Select t2.HotelRelationId
			From	HotelRelation As t2 Inner Join
						Unmatch As t1
			on		t1.HotelId = t2.HotelId and t1.ComHotelId = t2.HotelRelationComHotelId		
        ) A
	) ;	
   
     
	
	
	-- Added By Bhushan Gaud  For Deleting duplicate record on 07Aug2015 Start 
	-- Deleting Duplicate Record Automatch and Manual Match Start
	Delete From HotelRelation  Where HotelRelationId in 
	(
		Select HotelRelationId From 
        (
			Select HR.HotelRelationId 
			From HotelRelation HR Inner Join  HotelRelation HR1
			On HR.HotelId = HR1.HotelId And HR.HotelRelationComHotelId = HR1.HotelRelationComHotelId
			  And HR.isHotelRelationManualMatch = 0 
			  And HR1.isHotelRelationManualMatch = 1
		) B
	);
	-- Deleting Duplicate Record Automatch and Manual Match Start
	
	-- Deleting Duplicate Automatch Match Record Start
	Delete From HotelRelation Where HotelRelationId in 
	(
		Select HotelRelationId From 
		(
			Select Min(HotelRelationId) HotelRelationId, HotelRelationComHotelId, HotelId  From HotelRelation
			Where isHotelRelationManualMatch = 0
			Group By HotelRelationComHotelId, HotelId
			Having COUNT(HotelRelationId) > 1
		) A
	)
	And isHotelRelationManualMatch = 0;
	-- Deleting Duplicate Automatch Match Record End
	-- Added By Bhushan Gaud  For Deleting duplicate record on 07Aug2015 End



 Drop Temporary Table If Exists Temp_HotelRelation;
 
 CREATE Temporary TABLE Temp_HotelRelation (
  HotelRelationId bigint(20) NOT NULL ,
  HotelId bigint(20) NOT NULL,
  HotelRelationComHotelId bigint(20) NOT NULL,
  isHotelRelationManualMatch tinyint(1) NOT NULL,
  CreatedBy int(11) NOT NULL,
  AdminUserId int(11) NOT NULL,
  MatchDate datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  MatchingRunId int(11) DEFAULT NULL,
  MatchedInStepNo int(11) DEFAULT NULL,
  MatchingScore decimal(5,2) DEFAULT NULL,
  HotelNamePer decimal(5,2) DEFAULT NULL,
  HotelAddressPer decimal(5,2) DEFAULT NULL,
  GeoCoordinatesPer decimal(5,2) DEFAULT NULL,
  ModifiedBy int(11) DEFAULT NULL,
  ModifiedDatetime datetime DEFAULT NULL,
  LastFlagStatus int(11) NOT NULL DEFAULT '0',
  LastFlagStatusDateTime datetime DEFAULT NULL
  );


Insert into Temp_HotelRelation
Select * From HotelRelation R  Where isHotelRelationManualMatch = 0  
And MatchingRunId = v_RunId;  




Alter Table Temp_HotelRelation Add PrimaryHotelAddress   Varchar(4000) Default '';
Alter Table Temp_HotelRelation Add SecondaryHotelAddress Varchar(4000) Default '';
Alter Table Temp_HotelRelation Add PrimaryHotelName Varchar(4000) Default '';
Alter Table Temp_HotelRelation Add SecondaryHotelName Varchar(4000) Default '';
Alter Table Temp_HotelRelation Add MatchingPercentage   Decimal(9,2) Default 0;
Alter Table Temp_HotelRelation Add NameMatchingPercentage   Decimal(9,2) Default 0;
Alter Table Temp_HotelRelation Add PriCompetitorId     BigInt(20)		  Default 0;
Alter Table Temp_HotelRelation Add SecCompetitorId     BigInt(20)		  Default 0;
Alter Table Temp_HotelRelation Add SecMatchingCount  Int		  Default 0;
Alter Table Temp_HotelRelation Add PriMatchingCount  Int		  Default 0;


  
Update Temp_HotelRelation TT Inner Join Hotels P 
On TT.HotelId = P.HotelId Inner Join Hotels S 
On TT.HotelRelationComHotelId = S.HotelId Set 
	TT.PrimaryHotelAddress   = IFNULL(P.MatchHotelAddress1,''),
	TT.SecondaryHotelAddress = IFNULL(S.MatchHotelAddress1,''),
	TT.PriCompetitorId     = P.CompetitorId,
	TT.SecCompetitorId     = S.CompetitorId,
	TT.PrimaryHotelName     = Ifnull(P.matchhotelname, ''),
	TT.SecondaryHotelName   = Ifnull(S.matchhotelname, '');


Update Temp_HotelRelation TT Inner Join Hotels P 
On TT.HotelId = P.HotelId Inner Join Hotels S 
On TT.HotelRelationComHotelId = S.HotelId Set 
	TT.SecMatchingCount = (	Select COUNT(1) Cnt From HotelRelation R 
							Where  R.HotelRelationComHotelId = TT.HotelRelationComHotelId  
                           ),
	TT.PriMatchingCount = (Select COUNT(1) From HotelRelation HR Inner Join Hotels MH
								On HR.HotelRelationComHotelId = MH.HotelId 
                                Where MH.CompetitorId=TT.SecCompetitorId And
								  HR.HotelId = TT.HotelId   
								);
 

-- select * from ProbableMatchedHotels
INSERT INTO ProbableMatchedHotels
           (HotelId
           ,ProbableMatchedHotelComHotelId
           ,CreatedBy
           ,AdminUserId
           ,MatchDate
           ,MatchingRunId
           ,MatchedInStepNo
           ,MatchingScore
           ,MatchType
           ,HotelNamePer
           ,HotelAddressPer
           ,GeoCoordinatesPer)
select R.HotelId, R.HotelRelationComHotelId, R.CreatedBy, R.AdminUserId, R.MatchDate, R.MatchingRunId, R.MatchedInStepNo, 
	 R.MatchingScore, 4 MatchType, R.HotelNamePer, R.HotelAddressPer, R.GeoCoordinatesPer	
from Temp_HotelRelation R WHere Ifnull(PriMatchingCount,0) > 1;


/*Delete x From HotelRelation x Where x.HotelRelationId in 
(
	Select HotelRelationId From Temp_HotelRelation 
		WHere Ifnull(PriMatchingCount,0) > 1
);*/

	DELETE x 
    from HotelRelation x inner join 
		(Select HotelRelationId From Temp_HotelRelation 
		WHere Ifnull(PriMatchingCount,0) > 1) y on x.HotelRelationId = y.HotelRelationId;
    



INSERT INTO ProbableMatchedHotels
           (HotelId
           ,ProbableMatchedHotelComHotelId
           ,CreatedBy
           ,AdminUserId
           ,MatchDate
           ,MatchingRunId
           ,MatchedInStepNo
           ,MatchingScore
           ,MatchType
           ,HotelNamePer  
           ,HotelAddressPer
           ,GeoCoordinatesPer)
select R.HotelId, R.HotelRelationComHotelId, R.CreatedBy, R.AdminUserId, R.MatchDate, R.MatchingRunId, R.MatchedInStepNo, 
	 R.MatchingScore, 4 MatchType, R.HotelNamePer, R.HotelAddressPer, R.GeoCoordinatesPer	
from Temp_HotelRelation R WHere Ifnull(SecMatchingCount,0) > 1;


Delete From HotelRelation Where HotelRelationId in 
(
	Select HotelRelationId From Temp_HotelRelation WHere Ifnull(SecMatchingCount,0) > 1
);

  

-- Started:Added by sumeet helchal on 13th oct 2017
INSERT INTO ProbableMatchedHotels
           (HotelId
           ,ProbableMatchedHotelComHotelId
           ,CreatedBy
           ,AdminUserId
           ,MatchDate
           ,MatchingRunId
           ,MatchedInStepNo
           ,MatchingScore
           ,MatchType
           ,HotelNamePer
           ,HotelAddressPer
           ,GeoCoordinatesPer)
select R.HotelId, R.HotelRelationComHotelId, R.CreatedBy, R.AdminUserId, R.MatchDate, R.MatchingRunId, R.MatchedInStepNo, 
	 R.MatchingScore, 4 MatchType, R.HotelNamePer, R.HotelAddressPer, R.GeoCoordinatesPer	
from HotelRelation R  Where MatchingRunId = v_RunId;
-- Ended:Added by sumeet helchal on 13th oct 2017


-- --Added by Bhushan Gaud on 09 Nov 2017 as facing issue with matching date time start
INSERT INTO ProbableMatchedHotels
           (HotelId
           ,ProbableMatchedHotelComHotelId
           ,CreatedBy
           ,AdminUserId
           ,MatchDate
           ,MatchingRunId
           ,MatchedInStepNo
           ,MatchingScore
           ,MatchType
           ,HotelNamePer
           ,HotelAddressPer
           ,GeoCoordinatesPer)
select R.HotelId, R.HotelRelationComHotelId, R.CreatedBy, R.AdminUserId, R.MatchDate, (R.MatchingRunId * -1), R.MatchedInStepNo, 
	 R.MatchingScore, 4 MatchType, R.HotelNamePer, R.HotelAddressPer, R.GeoCoordinatesPer	
from HotelRelation R  
Where MatchingRunId = (v_RunId * -1);
-- --Added by Bhushan Gaud on 09 Nov 2017 as facing issue with matching date time End



DELETE FROM ProbableMatchedHotels  WHERE ProbableMatchedHotelId IN
(
	Select ProbableMatchedHotelId  From 
    (
		SELECT ProbableMatchedHotelId FROM ProbableMatchedHotels AS HW1  WHERE ProbableMatchedHotelId >
		(
			SELECT MIN(ProbableMatchedHotelId) ProbableMatchedHotelId FROM ProbableMatchedHotels AS HW2   
			WHERE  HW1.HotelId = HW2.HotelId  
			AND HW1.ProbableMatchedHotelComHotelId = HW2.ProbableMatchedHotelComHotelId  
			AND HW1.MatchType = HW2.MatchType  
		) 
	) A
);

	
Delete From ProbableMatchedHotels  Where ProbableMatchedHotelId In 
(
	Select ProbableMatchedHotelId From
    (
		Select	T1.ProbableMatchedHotelId
		From	ProbableMatchedHotels As T1  Inner Join
					Unmatch As T2
		on		T1.HotelId = T2.HotelId and T1.ProbableMatchedHotelComHotelId = T2.ComHotelId
	) A
);



-- -Delete Records from probable table because hotels does not exist in msthotel Start
	Delete P
	-- Select * 
	From ProbableMatchedHotels P Left Join Hotels MH
		On P.HotelId = MH.HotelId
		Where MH.HotelId Is Null;


	Delete P
	-- Select * 
	From ProbableMatchedHotels P Left Join Hotels MH
		On P.ProbableMatchedHotelComHotelId = MH.HotelId
		Where MH.HotelId Is Null;
        
        
-- -------Done-------------
  
	/*
	Delete A From 
	(
		Select ROW_NUMBER() Over(Partition By ProbableMatchedHotelComHotelId Order By MatchingScore Desc) SR_No, * 
			From ProbableMatchedHotels  Where   
			MatchType = 4
	)A Where SR_No > 4  
    */
    
    
Set @rn1 = 1;
 Set @ProbableMatchedHotelComHotelId = 0;
 Set @HotelId = 0;
      
   -- Select @@Version;   
    Delete P From ProbableMatchedHotels P Where P.ProbableMatchedHotelId in
    (
		Select ProbableMatchedHotelId From 
		(
			Select 
			@rn1 := 
				if(@ProbableMatchedHotelComHotelId = A.ProbableMatchedHotelComHotelId, 
					If(@HotelId = A.HotelId,@rn1,@rn1 +1)
				,  1) As Rank,  
				
				@ProbableMatchedHotelComHotelId := A.ProbableMatchedHotelComHotelId,
				@HotelId := A.HotelId
				HotelId, ProbableMatchedHotelComHotelId, ProbableMatchedHotelId
			From (
			SELECT  ProbableMatchedHotelId, HotelId, ProbableMatchedHotelComHotelId
				FROM ProbableMatchedHotels P
				ORDER BY  ProbableMatchedHotelComHotelId   
			) A
		) B  Where Rank > 4
	);
    
    


-- --Added by Bhushan Gaud on 09 Nov 2017 as facing issue with matching date time start
		Delete P
			From ProbableMatchedHotels P Left Join Hotels MH
				On P.ProbableMatchedHotelComHotelId = MH.HotelId
				Where P.MatchingRunId = v_RunId And MH.CompetitorId in (25,6);
-- --Added by Bhushan Gaud on 09 Nov 2017 as facing issue with matching date time End
 
-- ----------------------For Probable matches------------------------------
End If;

END ;;
