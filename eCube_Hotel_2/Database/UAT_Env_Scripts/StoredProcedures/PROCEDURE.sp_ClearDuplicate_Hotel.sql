DELIMITER ;;

CREATE PROCEDURE `sp_ClearDuplicate_Hotel`()
sp_lbl:
BEGIN

 

	Declare v_intCounter INT; 
    Declare v_IntDuplicateTotalRecords INT;  
    Declare v_intHotelCount INT;  
    Declare v_intSupplierId INT;  
    Declare v_intCityId INT;  
    Declare v_nvcrHotelName NVARCHAR(512);  
    Declare v_nvcrWebSiteHotelId NVARCHAR(50);  
    Declare v_nvcrHotelStar nvarchar(5);  
    Declare v_intHotelId INT;  
    Declare v_nvcrHotelAddress1 NVARCHAR(255);
	
	SET v_intCounter = 1;
	SET v_IntDuplicateTotalRecords = 0;
	
	 
	Drop temporary table if exists TmpMstHotel;
	Create temporary table TmpMstHotel
	(
		intSrlNo int unique Key AUTO_INCREMENT NOT NULL,
		intHotelCount INT,
		nvcrHotelName NVARCHAR(512),
		nvcrWebSiteHotelId NVARCHAR(50), 
		intSupplierId INT,
		intCityId INT,
		nvcrHotelStar nvarchar(5),
		nvcrHotelAddress1 NVARCHAR(255)-- sangeeta  
	);
	
	
	Insert Into TmpMstHotel (`intHotelCount`,nvcrWebSiteHotelId,`nvcrHotelName`,intSupplierId,intCityId,nvcrHotelStar, nvcrHotelAddress1) -- sangeeta 
	Select Count(HotelId),IFNULL(WebSiteHotelId,'') WebSiteHotelId, HotelName, CompetitorId, CityID, ifnull(StarRatingId,''), ifnull(HotelAddress1,'')
	From Hotels h 
	Group By CompetitorId, CityID, StarRatingId, WebSiteHotelId, HotelName,     HotelAddress1
	Having Count(HotelId) > 1;
	-- End Added nvcrWebSiteHotelId in group by statement for PMS#41336 by vikas shukla on 06-Jan-2015

			
	Select Count(intSrlNo) Into v_IntDuplicateTotalRecords From TmpMstHotel; 		
	-- Select @IntDuplicateTotalRecords=Count(nvcrWebSiteHotelId) From TmpMstHotel 	
	
	
	 

	While (v_IntDuplicateTotalRecords >= v_intCounter) Do
	
		SET v_nvcrHotelName = '';
		Set v_nvcrWebSiteHotelId = '';
		SET v_intSupplierId = 0;
		SET v_intCityId = 0; 
		set v_nvcrHotelStar = '';
		set v_nvcrHotelAddress1='';-- sangeeta
					
		Select `intHotelCount`
			,nvcrHotelName
			,ifnull(RTRIM(nvcrWebSiteHotelId),'')-- Added for PMS#41336 by vikas shukla on 06-Jan-2015
			,IntSupplierID
			,intCityID 
			, ifnull(nvcrHotelStar,'') Into v_intHotelCount, v_nvcrHotelName, v_nvcrWebSiteHotelId, v_intSupplierId, v_intCityId, v_nvcrHotelStar-- Added ISNULL command  for PMS#41336 by vikas shukla on 06-Jan-2015
		From TmpMstHotel Where `intSrlNo`=v_intCounter;
		
		While (v_intHotelCount > 1)
		Do
		 
			Select  
			 IFNULL(a.HotelId,0) 
				,IFNULL(a.WebSiteHotelId,'') Into v_intHotelId, v_nvcrWebSiteHotelId
			from
			(
				Select 
					IFNULL(h.WebSiteHotelId,'') WebSiteHotelId, 
					h.HotelId, h.HotelName,h.CompetitorId,h.CityID, IFNULL(h.StarRatingId,'') StarRatingId
				From Hotels h  
				Where h.HotelName = v_nvcrHotelName 
					and h.CityID = v_intCityId 
					And h.CompetitorId = v_intSupplierId 
					and ifnull(h.StarRatingId, '') = ifnull(v_nvcrHotelStar, '')
					AND ifnull(h.WebSiteHotelId, '') = ifnull(v_nvcrWebSiteHotelId, '') -- Added for PMS#41336 by vikas shukla on 06-Jan-2015
			)a
			inner join (
				Select 
					IFNULL(i.WebSiteHotelId,'') WebSiteHotelId, 
                    i.HotelName, i.CompetitorId,
                    i.CityID, IFNULL( i.StarRatingId,'') StarRatingId
				 
				From Hotels i  
				Where i.HotelName = v_nvcrHotelName
					and i.CityID = v_intCityId 
					And i.CompetitorId = v_intSupplierId 
					and ifnull(i.StarRatingId, '') = ifnull(v_nvcrHotelStar, '')
				 
					AND ifnull(i.WebSiteHotelId, '') = ifnull(v_nvcrWebSiteHotelId, '') 
				group by IFNULL(i.WebSiteHotelId,'') , i.HotelName, i.CompetitorId, i.CityID, IFNULL( i.StarRatingId,'')
				 
			)x
			on a.HotelName = x.HotelName
				and a.CompetitorId = x.CompetitorId
				and a.CityID = x.CityID
				and ifnull(a.StarRatingId, '') = ifnull(x.StarRatingId, '')
				AND a.WebSiteHotelId = x.WebSiteHotelId  
			Order By a.HotelId Desc Limit 1;
            
            -- Select  v_intHotelId;
            
 								
							
			If(v_intHotelId > 0)
			Then	
            
				INSERT INTO HotelRelationCleared
				(HotelRelationId,HotelId,HotelRelationComHotelId,isHotelRelationManualMatch,CreatedBy,AdminUserId,MatchDate,MatchingRunId
					,MatchedInStepNo,MatchingScore,HotelNamePer,HotelAddressPer,GeoCoordinatesPer,ModifiedBy,ModifiedDatetime
                    ,LastFlagStatus,LastFlagStatusDateTime)
				Select 
                HotelRelationId,HotelId,HotelRelationComHotelId,isHotelRelationManualMatch,CreatedBy,AdminUserId,MatchDate,MatchingRunId
					,MatchedInStepNo,MatchingScore,HotelNamePer,HotelAddressPer,GeoCoordinatesPer,ModifiedBy,ModifiedDatetime
                    ,LastFlagStatus,LastFlagStatusDateTime
				FROM HotelRelation hr 
				Where hr.HotelId = v_intHotelId or hr.HotelRelationComHotelid = v_intHotelId;

				-- Update HotelMonitor.HotelRelation set bitisManualunmatch=1 ,sdtmUnmatchdate = getdate()
				Delete from HotelRelation 
				Where HotelId = v_intHotelId or HotelRelationComHotelid = v_intHotelId;

				 
				

				-- Print 'Deleting Hotel Id... ' + Cast(@intHotelId As Char)
				INSERT INTO MSTHotelCleared
				(intHotelId, nvcrWebSiteHotelId, nvcrHotelName, nvcrHotelAddress1, nvcrHotelAddress2,
					intCityId, nvcrHotelBrandName, nvcrHotelStar, nvcrHotelPostCode, intSupplierId, 
                    tintHotelMatchStatus, nvcrHotelDescription, bitisProceesed, nvcrmatchhotelname, 
                    intDipBagSyncId, bitIsMailed, intDiPBagDynamicId,intUsrId,sdtAddedDateTime,
                    sdtCommentsDateTime)
                    
				SELECT HotelId, WebSiteHotelId, HotelName, HotelAddress1, HotelAddress2, CityId,
					HotelBrandName, StarRatingId, HotelPostCode, CompetitorId, HotelMatchStatus,
					HotelDescription, isProceesed, matchhotelname, DipBagSyncId, IsMailed,
					LastRequestRunId, CreatedBy, CreatedDate, Now() sdtCommentsDateTime 
				FROM Hotels  				
				Where HotelName = v_nvcrHotelName 
					AND IFNULL(WebSiteHotelId,'') = v_nvcrWebSiteHotelId -- Added for PMS#41336 by vikas shukla on 06-Jan-2015
					and CityId = v_intCityId 
					And CompetitorId = v_intSupplierId 
					and ifnull(StarRatingId, '') = ifnull(v_nvcrHotelStar, '')
					And HotelId = v_intHotelId;
				 
				DELETE FROM Hotels
				WHERE HotelName = v_nvcrHotelName 
					AND IFNULL(WebSiteHotelId,'') = v_nvcrWebSiteHotelId -- Added for PMS#41336 by vikas shukla on 06-Jan-2015
					and CityId = v_intCityId 
					And CompetitorId = v_intSupplierId 
					and ifnull(StarRatingId, '') = ifnull(v_nvcrHotelStar, '')
					And HotelId = v_intHotelId;
                    
				 
			End if;	 
			
			SET v_intHotelCount = v_intHotelCount -1;
		End While;
		-- print @intCounter
		SET v_intCounter = v_intCounter + 1;
	End While;		
    
LEAVE sp_lbl;

END ;;
