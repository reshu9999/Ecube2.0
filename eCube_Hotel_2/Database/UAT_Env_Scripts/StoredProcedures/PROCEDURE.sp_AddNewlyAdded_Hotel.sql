DELIMITER ;;

CREATE PROCEDURE `sp_AddNewlyAdded_Hotel`(
	p_intDiPBagDynamicId int
)
begin
	declare v_intUserId int;
 
	Drop Temporary Table If Exists Temp_BatchCrawlData;
	Create temporary Table Temp_BatchCrawlData
    As
	Select Distinct intDiPBagDynamicId, LTRIM(RTRIM(nvcrHotelCode)) nvcrHotelCode, LTRIM(RTRIM(nvcrHotelName)) nvcrHotelName, LTRIM(RTRIM(nvcrCity)) nvcrCity, 
		LTRIM(RTRIM(nvcrHotelAddress)) nvcrHotelAddress, intSupplierId, nvcrHotelLocation, 
		nvcrCompetitorHotelID, nvcrLongitude, nvcrLatitude,nvcrHotelStar, Cities.CityId, nvcrMultipleZoneCheck  	
	 From BatchCrawlData BCD  inner join Cities  
				on Cities.CityName= BCD.nvcrCity
			inner join tbl_CountryMaster Country   
				on Country.CountryName= BCD.nvcrHotelAddress
				and Cities.CountryID = Country.CountryID  
	WHere intDiPBagDynamicId = p_intDiPBagDynamicId;    
    
	Update Temp_BatchCrawlData Set nvcrCompetitorHotelID = Null Where Ltrim(Rtrim(nvcrCompetitorHotelID)) in ('-1','0');	
	
	update RequestRunDetail set `Status` = 2 where RequestRunId = p_intDiPBagDynamicId;   	
		
    
    Drop Temporary Table If exists Temp_Hotels;
    Create Temporary Table Temp_Hotels
    As
	Select HOTEL.HotelId, HOTEL.HotelName , CRAWL.nvcrHotelName  From 
    Hotels HOTEL INNER JOIN  Temp_BatchCrawlData CRAWL 	
		ON HOTEL.WebSiteHotelId = CRAWL.nvcrHotelCode
        AND CRAWL.intSupplierId = HOTEL.CompetitorId		
        INNER JOIN Cities CITY  
			ON LTRIM(RTRIM(CITY.CityName)) = LTRIM(RTRIM(CRAWL.nvcrCity))
            AND HOTEL.CityId = CITY.CityId
	-- SET HOTEL.HotelName = CRAWL.nvcrHotelName	
	WHERE HOTEL.CompetitorId IN(1,6,25,37,46,70,71,72) 	
		AND HOTEL.HotelName IS NOT NULL 
		AND	HOTEL.HotelName <> CRAWL.nvcrHotelName
		AND	CRAWL.nvcrHotelCode IS NOT NULL
		AND	CRAWL.intDiPBagDynamicId = p_intDiPBagDynamicId;
		
    Update Hotels H inner Join Temp_Hotels T  
		On H.HotelId = T.HotelId
	Set H.HotelName = T.nvcrHotelName;
    
       
	 	
	Drop Temporary Table If exists Temp_Hotels;
    Create Temporary Table Temp_Hotels
    As
    Select HOTEL.HotelId, HOTEL.HotelAddress1, CRAWL.nvcrHotelLocation     
	From Hotels HOTEL  INNER JOIN Cities CITY
	ON HOTEL.CityId = CITY.CityId	INNER JOIN Temp_BatchCrawlData CRAWL 
			ON LTRIM(RTRIM(CITY.CityName)) = LTRIM(RTRIM(CRAWL.nvcrCity))
		AND CRAWL.intSupplierId = HOTEL.CompetitorId
		and CRAWL.nvcrHotelName=HOTEL.HotelName
		And  Case WHen CRAWL.intSupplierId not in (1,6,25) 
				  Then Ifnull(HOTEL.WebSiteHotelId,'') 
			 Else '1' 
			 End = Case when  CRAWL.intSupplierId not in (1,6,25)
						Then Ifnull(CRAWL.nvcrCompetitorHotelID,'')
					Else '1' 
					End 
		
	WHERE HOTEL.HotelName IS NOT NULL 
		AND HOTEL.CompetitorId NOT IN(1,6,25,37,46,70,71,72) 
		AND (HOTEL.HotelAddress1 IS NULL OR LTRIM(RTRIM(HOTEL.HotelAddress1)) = '') 
		AND	HOTEL.HotelName = CRAWL.nvcrHotelName
		AND	CRAWL.intDiPBagDynamicId = p_intDiPBagDynamicId;
        
	Update Hotels H inner Join Temp_Hotels T  
		On H.HotelId = T.HotelId
	set H.HotelAddress1 = T.nvcrHotelLocation ;
        
			 		
 
	Drop Temporary Table If exists Temp_NewHotel;
	Create Temporary Table Temp_NewHotel
	As
	SELECT DISTINCT CRAWL.nvcrHotelName, CITY.CityId , CRAWL.intSupplierId, CRAWL.intDiPBagDynamicId , 
		LTRIM(RTRIM(CRAWL.nvcrCompetitorHotelID)) nvcrCompetitorHotelID, CRAWL.nvcrHotelLocation 
	FROM Temp_BatchCrawlData CRAWL 	
		INNER JOIN Cities CITY  
		ON CITY.CityName = CRAWL.nvcrCity
		INNER JOIN tbl_CountryMaster Country   
		ON Country.CountryName = CRAWL.nvcrHotelAddress
		AND CITY.CountryID = Country.CountryID  
	WHERE CRAWL.intDiPBagDynamicId = p_intDiPBagDynamicId;
            
           
            
    Drop Temporary Table If exists Temp_Hotels;
    Create Temporary Table Temp_Hotels
    As
    Select HOTEL.HotelId, HOTEL.WebSiteHotelId, BCD.nvcrCompetitorHotelID
	From Hotels HOTEL INNER JOIN  Temp_NewHotel BCD
	ON HOTEL.CityId = BCD.CityId					
	AND HOTEL.CompetitorId = BCD.intSupplierId
	AND LTRIM(RTRIM(HOTEL.HotelName)) = LTRIM(RTRIM(BCD.nvcrHotelName))	
	WHERE BCD.intDiPBagDynamicId = p_intDiPBagDynamicId
		AND HOTEL.CompetitorId NOT IN(1,6,25,37,46,70,71,72,73,74,75,76)  
		AND	HOTEL.HotelName IS NOT NULL 						
		AND	IFNULL(HOTEL.WebSiteHotelId, '') = ''						
		AND	IFNULL(BCD.nvcrCompetitorHotelID, '') <> ''				
		AND	LTRIM(RTRIM(BCD.nvcrCompetitorHotelID)) REGEXP '^[a-zA-Z0-9]+$';
	
    
    Update Hotels H inner Join Temp_Hotels T  
		On H.HotelId = T.HotelId
	SET H.WebSiteHotelId = T.nvcrCompetitorHotelID;
    
    
			
        
	Drop Temporary Table If exists Temp_NewHotel;
	Create Temporary Table Temp_NewHotel
	As
	SELECT DISTINCT CRAWL.nvcrHotelName, CITY.CityId , CRAWL.intSupplierId, CRAWL.intDiPBagDynamicId , 
		CRAWL.nvcrCompetitorHotelID, CRAWL.nvcrHotelLocation 
	FROM Temp_BatchCrawlData CRAWL 	
		INNER JOIN Cities CITY  
			ON CITY.CityName = CRAWL.nvcrCity
		INNER JOIN tbl_CountryMaster Country   
			ON Country.CountryName = CRAWL.nvcrHotelAddress
			AND CITY.CountryID = Country.CountryID  
		WHERE CRAWL.intDiPBagDynamicId = p_intDiPBagDynamicId;
        
      
       
	UPDATE Hotels HOTEL INNER JOIN Temp_NewHotel BCD
		ON HOTEL.CityId = BCD.CityId					
		AND HOTEL.CompetitorId = BCD.intSupplierId
		AND LTRIM(RTRIM(HOTEL.HotelName)) = LTRIM(RTRIM(BCD.nvcrHotelName))
		
		SET HOTEL.WebSiteHotelId = BCD.nvcrCompetitorHotelID
	WHERE BCD.intDiPBagDynamicId = p_intDiPBagDynamicId
		AND HOTEL.CompetitorId IN (10)  
		AND	HOTEL.HotelName IS NOT NULL 						
		AND	IFNULL(HOTEL.WebSiteHotelId, '') = ''						
		AND	IFNULL(BCD.nvcrCompetitorHotelID, '') != '';	



	Drop Temporary Table If exists Temp_NewHotel;
	Create Temporary Table Temp_NewHotel
	As
	SELECT DISTINCT LTRIM(RTRIM(CRAWL.nvcrHotelName)) nvcrHotelName, CRAWL.CityId , CRAWL.intSupplierId, CRAWL.intDiPBagDynamicId , CRAWL.nvcrLongitude, 
		CRAWL.nvcrLatitude, CRAWL.nvcrHotelLocation   
		,nvcrCompetitorHotelID
	FROM Temp_BatchCrawlData CRAWL 	 
	WHERE	CRAWL.intDiPBagDynamicId = p_intDiPBagDynamicId;

	

	Drop Temporary Table If exists Temp_Hotels;
    Create Temporary Table Temp_Hotels
    As
    Select HOTEL.HotelId,  HOTEL.Longitude, 
		(CASE WHEN IFNULL(HOTEL.Longitude, '') = '' And fn_IsNumeric(BCD.nvcrLongitude) = 1 THEN BCD.nvcrLongitude      
				ELSE HOTEL.Longitude
		END ) BCD_Longitude, HOTEL.Latitude,
        (CASE WHEN IFNULL(HOTEL.Latitude, '') = '' And fn_IsNumeric(BCD.nvcrLatitude) = 1 THEN BCD.nvcrLatitude      
				ELSE HOTEL.Latitude
		END ) BCD_Latitude        
    From Hotels HOTEL INNER JOIN  Temp_NewHotel BCD
		ON HOTEL.CityId = BCD.CityId		 						
		AND HOTEL.CompetitorId = BCD.intSupplierId
		AND HOTEL.HotelName = BCD.nvcrHotelName	
		And  Case WHen BCD.intSupplierId not in (1,6,25) 
				  Then Ifnull(HOTEL.WebSiteHotelId,'') 
			 Else '1' 
			 End = Case when BCD.intSupplierId not in (1,6,25)
						Then Ifnull(BCD.nvcrCompetitorHotelID,'')  
				   Else '1' End                
	
	WHERE BCD.intDiPBagDynamicId = p_intDiPBagDynamicId 
	AND HOTEL.CompetitorId NOT IN(1,6,25,37,46,70,71,72,73,74,75,76)  
	AND	(IFNULL(HOTEL.Longitude, '') = '' OR IFNULL(HOTEL.Latitude, '') = '')
	AND HOTEL.HotelName IS NOT NULL;


	Update Hotels H inner Join Temp_Hotels T  
		On H.HotelId = T.HotelId 	 
	SET H.Longitude = BCD_Longitude,
		H.Latitude = BCD_Latitude;
    
    
    Select Group_Concat(CityID) into @CityId From Temp_BatchCrawlData;
    
    Select Group_Concat(intSupplierId) into @intSupplierId From Temp_BatchCrawlData;
    
    
    Drop Temporary Table If Exists Temp_Hotels_City_Sup; 
	Create Temporary Table Temp_Hotels_City_Sup
    As
    Select * From Hotels Where CityId in (@CityId) and CompetitorId in (@intSupplierId);
    
	            
    


 
	insert into Hotels
	(
	WebSiteHotelId, 
	HotelName, 
	HotelAddress1, 
	HotelAddress2, 
	HotelPostCode, 
	CityId, 
	StarRatingId, 
	CompetitorId, 
	HotelMatchStatus, 
	HotelDescription, 
	CreatedBy,
	LastRequestRunId 
	)

	select distinct CRAWL.nvcrHotelCode as nvcrWebSiteHotelId, 
		CRAWL.nvcrHotelName as nvcrHotelName,
		CRAWL.nvcrHotelLocation as nvcrHotelAddress1,	 
		
		null as nvcrHotelAddress2, 
		null as nvcrHotelPostCode, 
		Cities.CityId as intCityId,  
		null as nvcrHotelStar, 
		CRAWL.intSupplierId as intSupplierId, 
		0 as tintHotelMatchStatus , 
		Hotel.HotelName as nvcrHotelDescription, 
		85 as intUsrId , 
		p_intDiPBagDynamicId as intDiPBagDynamicId				

	from Temp_BatchCrawlData as CRAWL   
	inner join Cities  
		on Cities.CityName= CRAWL.nvcrCity
	inner join tbl_CountryMaster Country   
		on Country.CountryName= CRAWL.nvcrHotelAddress
		and Cities.CountryID = Country.CountryID  
	left outer Join Temp_Hotels_City_Sup as Hotel  
		on	CRAWL.intSupplierId = Hotel.CompetitorId 
		and Hotel.CityId = Cities.CityId
		and ifnull(CRAWL.nvcrHotelCode,0) = ifnull(Hotel.WebSiteHotelId,0)
		
	Where	CRAWL.intDiPBagDynamicId = p_intDiPBagDynamicId  
	and		Hotel.WebSiteHotelId IS NULL 
	and		CRAWL.nvcrHotelCode IS NOT NULL	
	and CRAWL.nvcrHotelName is not null;  

		
	Drop Temporary Table If Exists Temp_Hotels_City_Sup; 
	Create Temporary Table Temp_Hotels_City_Sup
	As
	Select * From Hotels Where CityId in (@CityId) and CompetitorId in (@intSupplierId);


	insert into Hotels 
		(WebSiteHotelId, HotelName, HotelAddress1, HotelAddress2, HotelPostCode, CityId, StarRatingId, CompetitorId, HotelMatchStatus, 
			HotelDescription, CreatedBy, LastRequestRunId)
                
	select CRAWL.nvcrHotelCode as nvcrWebSiteHotelId, 
			CRAWL.nvcrHotelName as nvcrHotelName, 
			CRAWL.nvcrHotelLocation as nvcrHotelAddress1,				 
			null as nvcrHotelAddress2, null as nvcrHotelPostCode, 
			CRAWL.CityId as intCityId,  null as nvcrHotelStar, 
			CRAWL.intSupplierId as intSupplierId, 
			0 as tintHotelMatchStatus , 
			Hotel.HotelName as nvcrHotelDescription
			, 85 as intUsrId, p_intDiPBagDynamicId as intDiPBagDynamicId
	from Temp_BatchCrawlData as CRAWL 
	left outer Join Temp_Hotels_City_Sup as Hotel  
		on  Hotel.CityId = CRAWL.CityId 
		and CRAWL.nvcrHotelName = Hotel.HotelName 
		and CRAWL.intSupplierId = Hotel.CompetitorId 
	Where	CRAWL.intDiPBagDynamicId = p_intDiPBagDynamicId 
		and		CRAWL.nvcrHotelName is not Null 
		and		CRAWL.nvcrHotelCode is null
	group by CRAWL.intDiPBagDynamicId, CRAWL.nvcrHotelCode, CRAWL.nvcrHotelName, 
	CRAWL.nvcrCity, CRAWL.CityId, CRAWL.intSupplierId, Hotel.HotelName ,
	CRAWL.nvcrHotelLocation 
	having Hotel.HotelName is null;  

		
	Drop Temporary Table If Exists Temp_Hotels_City_Sup; 
	Create Temporary Table Temp_Hotels_City_Sup
	As
	Select * From Hotels Where CityId in (@CityId) and CompetitorId in (@intSupplierId);
    
    
       
	UPDATE Hotels HOTEL  
	INNER JOIN Temp_BatchCrawlData CRAWL 	
		ON HOTEL.CityId = CRAWL.CityId	
		AND CRAWL.intSupplierId = HOTEL.CompetitorId			
		AND HOTEL.HotelName = CRAWL.nvcrHotelName				
	SET	
	nvcrHotelStar = CASE WHEN CRAWL.nvcrHotelStar IS NULL THEN null
					   WHEN INSTR(CRAWL.nvcrHotelStar, '/') > 0 THEN Substring(CRAWL.nvcrHotelStar, INSTR(CRAWL.nvcrHotelStar, '/')+1,1) 
					ELSE null END
	Where	CRAWL.intDiPBagDynamicId = p_intDiPBagDynamicId 
	and cast(HOTEL.CreatedDate as date)=cast(NOW() as date);
			
		 
         
	Drop Temporary Table If exists Temp_NewHotel;
	Create Temporary Table Temp_NewHotel
	As
	SELECT DISTINCT CRAWL.nvcrHotelName, CRAWL.CityId , CRAWL.intSupplierId, CRAWL.intDiPBagDynamicId , 
	CRAWL.nvcrCompetitorHotelID, CRAWL.nvcrHotelLocation 
	FROM Temp_BatchCrawlData CRAWL 			 
	WHERE CRAWL.intDiPBagDynamicId = p_intDiPBagDynamicId; 
	
   
	
	UPDATE Hotels HOTEL INNER JOIN Temp_NewHotel BCD
		ON HOTEL.CityId = BCD.CityId					
		AND HOTEL.CompetitorId = BCD.intSupplierId
		AND LTRIM(RTRIM(HOTEL.HotelName)) = LTRIM(RTRIM(BCD.nvcrHotelName))			
		AND HOTEL.LastRequestRunId = p_intDiPBagDynamicId	
	SET HOTEL.WebSiteHotelId = BCD.nvcrCompetitorHotelID
	WHERE BCD.intDiPBagDynamicId = p_intDiPBagDynamicId
		AND HOTEL.CompetitorId NOT IN(1,6,25,37,46,70,71,72,73,74,75,76)  
		AND	HOTEL.HotelName IS NOT NULL 						
		AND	IFNULL(HOTEL.WebSiteHotelId, '') = ''						
		AND	IFNULL(BCD.nvcrCompetitorHotelID, '') <> ''							
		AND	LTRIM(RTRIM(BCD.nvcrCompetitorHotelID)) REGEXP '^[a-zA-Z0-9]+$'; -- NOT LIKE '%[^a-zA-Z0-9]%';
	
	 
		
	Drop Temporary Table If exists Temp_NewHotel;
	Create Temporary Table Temp_NewHotel
	As
	SELECT DISTINCT CRAWL.nvcrHotelName, CRAWL.CityId , CRAWL.intSupplierId, CRAWL.intDiPBagDynamicId , 
	CRAWL.nvcrCompetitorHotelID, CRAWL.nvcrHotelLocation 
	FROM Temp_BatchCrawlData CRAWL 			  
	WHERE CRAWL.intDiPBagDynamicId = p_intDiPBagDynamicId;
        
					 
		
	UPDATE Hotels HOTEL INNER JOIN Temp_NewHotel BCD
		ON HOTEL.CityId = BCD.CityId					
		AND HOTEL.CompetitorId = BCD.intSupplierId
		AND LTRIM(RTRIM(HOTEL.HotelName)) = LTRIM(RTRIM(BCD.nvcrHotelName))								
		AND HOTEL.LastRequestRunId = p_intDiPBagDynamicId	
        SET HOTEL.WebSiteHotelId = BCD.nvcrCompetitorHotelID
	WHERE BCD.intDiPBagDynamicId = p_intDiPBagDynamicId
		AND HOTEL.CompetitorId IN(10)  
		AND	HOTEL.HotelName IS NOT NULL 						
		AND	IFNULL(HOTEL.WebSiteHotelId, '') = ''						
		AND	IFNULL(BCD.nvcrCompetitorHotelID, '') <> '';	
			 
	
	Drop Temporary Table If exists Temp_NewHotel;
	Create Temporary Table Temp_NewHotel
	As
	SELECT DISTINCT LTRIM(RTRIM(CRAWL.nvcrHotelName)) nvcrHotelName, CRAWL.CityId , CRAWL.intSupplierId, CRAWL.intDiPBagDynamicId , CRAWL.nvcrLongitude, 
		CRAWL.nvcrLatitude, CRAWL.nvcrHotelLocation   
		,nvcrCompetitorHotelID
	FROM Temp_BatchCrawlData CRAWL 	 
	WHERE	CRAWL.intDiPBagDynamicId = p_intDiPBagDynamicId;	


	Drop Temporary Table If exists Temp_Hotels;
    Create Temporary Table Temp_Hotels
    As
    Select HOTEL.HotelId,  HOTEL.Longitude, 
		(CASE WHEN IFNULL(HOTEL.Longitude, '') = '' And fn_IsNumeric(BCD.nvcrLongitude) = 1 THEN BCD.nvcrLongitude      
				ELSE HOTEL.Longitude
		END ) BCD_Longitude, HOTEL.Latitude,
        (CASE WHEN IFNULL(HOTEL.Latitude, '') = '' And fn_IsNumeric(BCD.nvcrLatitude) = 1 THEN BCD.nvcrLatitude      
				ELSE HOTEL.Latitude
		END ) BCD_Latitude        
    From Temp_Hotels_City_Sup HOTEL INNER JOIN  Temp_NewHotel BCD
		ON HOTEL.CityId = BCD.CityId		 						
		AND HOTEL.CompetitorId = BCD.intSupplierId
		AND HOTEL.HotelName = BCD.nvcrHotelName	
		And  Case WHen BCD.intSupplierId not in (1,6,25) 
				  Then Ifnull(HOTEL.WebSiteHotelId,'') 
			 Else '1' 
			 End = Case when BCD.intSupplierId not in (1,6,25)
						Then Ifnull(BCD.nvcrCompetitorHotelID,'')  
				   Else '1' End 	
	WHERE BCD.intDiPBagDynamicId = p_intDiPBagDynamicId 
	AND HOTEL.CompetitorId NOT IN(1,6,25,37,46,70,71,72,73,74,75,76)  
	AND	(IFNULL(HOTEL.Longitude, '') = '' OR IFNULL(HOTEL.Latitude, '') = '')
	AND HOTEL.HotelName IS NOT NULL;
    
    
	Update Hotels H inner Join Temp_Hotels T  
		On H.HotelId = T.HotelId 	 
	SET H.Longitude = BCD_Longitude,
		H.Latitude = BCD_Latitude;		
  
  
    Drop Temporary Table If exists Temp_Hotels;
    Create Temporary Table Temp_Hotels
    As
    Select Distinct HOTEL.HotelId 
    From Temp_Hotels_City_Sup HOTEL INNER JOIN Temp_BatchCrawlData CRAWL 	
		ON HOTEL.CityId = CRAWL.CityId
        and HOTEL.CompetitorId in (1,6,25)
		AND HOTEL.HotelName = CRAWL.nvcrHotelName;	
    
    
    Update Hotels H inner Join Temp_Hotels T  
		On H.HotelId = T.HotelId	
	SET	
	LastAppearnceDate = NOW(),
	LastRequestRunId = p_intDiPBagDynamicId;
    
    
    Drop Temporary Table If exists Temp_Hotels;
    Create Temporary Table Temp_Hotels
    As
    Select Distinct HOTEL.HotelId 
    From Temp_Hotels_City_Sup HOTEL INNER JOIN Temp_BatchCrawlData CRAWL
		ON HOTEL.CityId = CRAWL.CityId
        AND CRAWL.intSupplierId = HOTEL.CompetitorId
        and HOTEL.CompetitorId not in (1,6,25)					
		AND HOTEL.HotelName = CRAWL.nvcrHotelName
		and Ifnull(HOTEL.WebSiteHotelId,'')=Ifnull(CRAWL.nvcrCompetitorHotelID,'');
		   
    
    
	Update Hotels H inner Join Temp_Hotels T  
		On H.HotelId = T.HotelId	
	SET	
	LastAppearnceDate = NOW(),
	LastRequestRunId = p_intDiPBagDynamicId; 
    
    
    
    Drop Temporary Table If exists Temp_Hotels;
    Create Temporary Table Temp_Hotels
    As
    Select Distinct HOTEL.HotelId , HOTEL.CRAWLedHotelAddress, CRAWL.nvcrHotelLocation
    From Temp_Hotels_City_Sup HOTEL INNER JOIN Temp_BatchCrawlData CRAWL
		ON HOTEL.CityId = CRAWL.CityId			
		AND CRAWL.intSupplierId = HOTEL.CompetitorId			
		AND HOTEL.HotelName = CRAWL.nvcrHotelName			  
		And  Case WHen CRAWL.intSupplierId not in (1,6,25) 
				  Then Ifnull(HOTEL.WebSiteHotelId,'') 		   
			 Else '1' End = Case when  CRAWL.intSupplierId not in (1,6,25)
								 Then Ifnull(CRAWL.nvcrCompetitorHotelID,'')
							Else '1' End; 
    
	Update Hotels H inner Join Temp_Hotels T  
		On H.HotelId = T.HotelId	
	SET	H.CRAWLedHotelAddress = T.nvcrHotelLocation;

	
	Drop Temporary Table If exists Temp_Hotels;
    Create Temporary Table Temp_Hotels
    As
    Select Distinct HOTEL.HotelId, 
		(CASE WHEN CRAWL.nvcrHotelStar IS NULL THEN null
							WHEN position( '/' in CRAWL.nvcrHotelStar) > 0 THEN SUBSTRING(CRAWL.nvcrHotelStar, position( '/' in CRAWL.nvcrHotelStar)+1,1) 
							ELSE null 
							END) CRAWLedHotelStar_BCD, HOTEL.CRAWLedHotelStar
    
    From
     Temp_Hotels_City_Sup HOTEL INNER JOIN  Temp_BatchCrawlData CRAWL
		ON HOTEL.CityId = CRAWL.CityId
		AND CRAWL.intSupplierId = HOTEL.CompetitorId			
		AND HOTEL.HotelName = CRAWL.nvcrHotelName;
    
    
    Update Hotels H inner Join Temp_Hotels T  
		On H.HotelId = T.HotelId	
	SET	H.CRAWLedHotelStar = T.CRAWLedHotelStar_BCD;
    
    
    Drop Temporary Table If exists Temp_Hotels;
    Create Temporary Table Temp_Hotels
    As
    Select Distinct HOTEL.HotelId, CRAWLedZoneName, CRAWL.nvcrMultipleZoneCheck    
    From Temp_Hotels_City_Sup HOTEL INNER JOIN Temp_BatchCrawlData CRAWL
		ON HOTEL.CityId = CRAWL.CityId
		AND CRAWL.intSupplierId = HOTEL.CompetitorId			
		AND HOTEL.HotelName = CRAWL.nvcrHotelName
		And  Case WHen CRAWL.intSupplierId not in (1,6,25) Then Ifnull(HOTEL.WebSiteHotelId,'') 
			Else '1' End = Case when  CRAWL.intSupplierId not in (1,6,25) Then Ifnull(CRAWL.nvcrCompetitorHotelID,'')
							Else '1' End; 
    
    
    Update Hotels H inner Join Temp_Hotels T  
		On H.HotelId = T.HotelId
	Set H.CRAWLedZoneName = T.nvcrMultipleZoneCheck;  
    
    
  
	-- start change PMS # 25830
	-- To clear duplicate hotel entries after adding new one
	call  sp_ClearDuplicate_Hotel();
	-- end of change PMS # 25830

	-- start change PMS R3# 26071;Bhavin.Dhimmar
	call  usp_DipBagHM_CrawlManager_AddNewlyHotel_DummyForhotelopia_Upload (p_intDiPBagDynamicId);
    
	-- end of change PMS R3# 26071;Bhavin.Dhimmar
	
	-- for HotelCode wise Matching, vijay S K, 29-Jul-2010
	call sp_MatchUserHotel_HotelCode_Batch (0,p_intDiPBagDynamicId);
	-- End hotelcode matching

	-- start change PMS # 25830	
	-- Commented; because Newly hotels are added before DiPBagDynamic.tintDiPBagDynamicStatus=3
	 
	-- end of change PMS # 25830

 
	 
			
		Update Hotels 
			Set HotelMatchStatus = 1 
		Where LastRequestRunId = p_intDiPBagDynamicId And 
		CompetitorId in (1, 6, 25);
	

	
 
 
 

end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_Add_ProxyMaster` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
