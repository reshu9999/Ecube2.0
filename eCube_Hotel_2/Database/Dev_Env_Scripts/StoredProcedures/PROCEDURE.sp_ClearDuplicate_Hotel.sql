DELIMITER ;;

CREATE PROCEDURE `sp_ClearDuplicate_Hotel`()
BEGIN

/*******************************************************************         
'	Name					: sp_ClearDuplicate_Hotel
'	Desc					: Will clear duplicate hotels for the same city and supplier that are matched or Unmatched
								as per PMS# 25830
'	Called by				: sp_ClearDuplicate_Hotel
'	Example of execution	: Call sp_ClearDuplicate_Hotel

INPUT PARAMETRS				Type	

OUTPUT PARAMETRS			Type

'	Created by				: Bhushan Gaud
'	Date of creation		: 05-May-2018

******************************************************************************************************
Change History
******************************************************************************************************
SR.No	Date:			Changed by:				Description:

******************************************************************************************************/

	Declare v_intCounter INT; 
    Declare v_IntDuplicateTotalRecords INT;  
    Declare v_HotelCount INT;  
    Declare v_CompetitorId INT;  
    Declare v_CityId INT;  
    Declare v_HotelName NVARCHAR(512);
    Declare v_WebSiteHotelId NVARCHAR(50);  
    Declare v_StarRatingId INT;  
    Declare v_HotelId INT;  
    Declare v_HotelAddress1 NVARCHAR(255);
	
	SET v_intCounter = 1;
	SET v_IntDuplicateTotalRecords = 0;
	
	
	Drop temporary table if exists TmpMstHotel;
	Create temporary table TmpMstHotel
	(
		SrlNo int unique Key AUTO_INCREMENT NOT NULL,
		HotelCount INT,
		HotelName NVARCHAR(512),
		WebSiteHotelId NVARCHAR(50),
		CompetitorId INT,
		CityId INT,
		StarRatingId nvarchar(5),
		HotelAddress1 NVARCHAR(255)
	);
	
	
	Insert Into TmpMstHotel (`HotelCount`,WebSiteHotelId,`HotelName`,CompetitorId,CityId,StarRatingId, HotelAddress1) -- sangeeta 
	Select Count(HotelId),IFNULL(WebSiteHotelId,'') WebSiteHotelId, HotelName,CompetitorId,CityId,ifnull(StarRatingId,0),ifnull(HotelAddress1,'')
	From Hotels h 
	Group By IFNULL(WebSiteHotelId,''),HotelName,CompetitorId,CityId, ifnull(StarRatingId,0),ifnull(HotelAddress1,'')-- added by sangeeta
	Having Count(HotelId) > 1;
	

 
		
	Select Count(SrlNo) Into v_IntDuplicateTotalRecords From TmpMstHotel; 		
	  
	
	While (v_IntDuplicateTotalRecords >= v_intCounter) Do
	 
		SET v_HotelName = '';
		Set v_WebSiteHotelId = '';
		SET v_CompetitorId = 0;
		SET v_CityId = 0; 
		set v_StarRatingId = '';
		set v_HotelAddress1='';-- sangeeta
					
		Select `HotelCount`
			,HotelName
			,ifnull(RTRIM(WebSiteHotelId),'')-- Added for PMS#41336 by vikas shukla on 06-Jan-2015
			,CompetitorId
			,CityId 
			, ifnull(StarRatingId,0) Into v_HotelCount, v_HotelName, v_WebSiteHotelId, v_CompetitorId, v_CityId, v_StarRatingId-- Added ISNULL command  for PMS#41336 by vikas shukla on 06-Jan-2015
		From TmpMstHotel Where `SrlNo`=v_intCounter;
		
		While (v_HotelCount > 1) Do
		
        Select  
			 IFNULL(a.HotelId,0) 
				,IFNULL(a.WebSiteHotelId,'') Into v_HotelId, v_WebSiteHotelId
			from
			(
				Select 
					IFNULL(h.WebSiteHotelId,'') WebSiteHotelId,-- Added for PMS#41336 by vikas shukla on 06-Jan-2015
					h.HotelId, h.HotelName,h.CompetitorId,h.CityId, IFNULL( h.StarRatingId,0)StarRatingId
				From Hotels h 
				Where h.HotelName = v_HotelName 
					and h.CityId = v_CityId 
					And h.CompetitorId = v_CompetitorId 
					and ifnull(h.StarRatingId, 0) = ifnull(v_StarRatingId, 0)
					AND ifnull(h.WebSiteHotelId, '') = ifnull(v_WebSiteHotelId, '') -- Added for PMS#41336 by vikas shukla on 06-Jan-2015
			)a
			inner join (
				Select 
					IFNULL(i.WebSiteHotelId,'') WebSiteHotelId,i.HotelName,i.CompetitorId,i.CityId, IFNULL( i.StarRatingId,0) StarRatingId
				From Hotels i  
				Where i.HotelName = v_HotelName
					and i.CityId = v_CityId 
					And i.CompetitorId = v_CompetitorId 
					and ifnull(i.StarRatingId, 0) = ifnull(v_StarRatingId, 0)
				 	AND ifnull(i.WebSiteHotelId, '') = ifnull(v_WebSiteHotelId, '') 
				group by IFNULL(i.WebSiteHotelId,'') ,i.HotelName,i.CompetitorId,i.CityId, IFNULL( i.StarRatingId,0)
				
			)x
			on a.HotelName = x.HotelName
				and a.CompetitorId = x.CompetitorId
				and a.CityId = x.CityId
				and ifnull(a.StarRatingId, 0) = ifnull(x.StarRatingId, 0)
				AND A.WebSiteHotelId=x.WebSiteHotelId 
			Order By a.HotelId Desc limit 1;
 								
							
			If(v_HotelId > 0)
			Then					
				
				INSERT INTO HotelRelationCleared
				(HotelRelationId, HotelId, HotelRelationComHotelId, HotelRelationManualMatch,
				 CreatedBy, AdminUserId, MatchDate)
				SELECT HotelRelationId, HotelId, HotelRelationComHotelId, HotelRelationManualMatch,
					CreatedBy, AdminUserId, MatchDate
				FROM HotelRelation hr 
				Where hr.HotelId = v_HotelId or hr.intHotelRelationComHotelid = v_HotelId;

				
				Delete from HotelRelation  Where HotelId = v_HotelId or intHotelRelationComHotelid = v_HotelId;

				-- Print 'Deleting Hotel Id... ' + Cast(@HotelId As Char)
				INSERT INTO  HotelsCleared
				(HotelId,    WebSiteHotelId,    HotelName,    HotelAddress1,    HotelAddress2,
					CityId,    HotelBrandName,    StarRatingId,    HotelPostCode,    CompetitorId,    HotelMatchStatus,
					HotelDescription,    isProceesed,    matchhotelname,    DipBagSyncId,    IsMailed,    RequestId,
					ismailed1,    Active,    CreatedBy,    CreatedDate,    ModifiedBy,    ModifiedDatetime,
					LastAppearnceDate)
				SELECT HotelId,    WebSiteHotelId,    HotelName,    HotelAddress1,    HotelAddress2,
					CityId,    HotelBrandName,    StarRatingId,    HotelPostCode,    CompetitorId,    HotelMatchStatus,
					HotelDescription,    isProceesed,    matchhotelname,    DipBagSyncId,    IsMailed,    RequestId,
					ismailed1,    Active,    CreatedBy,    CreatedDate,    ModifiedBy,    ModifiedDatetime,
					LastAppearnceDate
				FROM Hotels   				
				Where HotelName = v_HotelName 
					AND IFNULL(WebSiteHotelId,'') = v_WebSiteHotelId -- Added for PMS#41336 by vikas shukla on 06-Jan-2015
					and CityId = v_CityId 
					And CompetitorId = v_CompetitorId 
					and ifnull(StarRatingId, 0) = ifnull(v_StarRatingId, 0)
					And HotelId = v_HotelId;
				
				DELETE FROM Hotels
				WHERE HotelName = v_HotelName 
					AND IFNULL(WebSiteHotelId,'') = v_WebSiteHotelId -- Added for PMS#41336 by vikas shukla on 06-Jan-2015
					and CityId = v_CityId 
					And CompetitorId = v_CompetitorId 
					and ifnull(StarRatingId, 0) = ifnull(v_StarRatingId, 0)
					And HotelId = v_HotelId;
				
			End if;				
			SET v_HotelCount = v_HotelCount -1;
		End While;
		-- print @intCounter
		SET v_intCounter = v_intCounter + 1;
	End While;	
   
END ;;
