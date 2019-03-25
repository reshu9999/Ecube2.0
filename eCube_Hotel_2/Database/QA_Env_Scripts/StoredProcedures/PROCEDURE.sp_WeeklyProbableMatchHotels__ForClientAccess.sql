DELIMITER ;;

CREATE PROCEDURE `sp_WeeklyProbableMatchHotels__ForClientAccess`(
	p_intProbableMatchedHotelId Longtext
)
BEGIN  

		
        
			/*
			SELECT  DISTINCT 
			r.ProbableMatchedHotelId, 
			IFNULL(s.name,'') AS 'Secondary Supplier Company',  			
			IFNULL(h.HotelId ,'') AS 'Secondary Supplier Hotel ID',
			IFNULL(h.WebSiteHotelId,'') AS 'Secondary Website Hotel ID',
			IFNULL(h.HotelName,'') AS 'Secondary Supplier Hotel Name',
			IFNULL(h.HotelAddress1,'') AS 'Secondary Supplier Hotel Address', 
			IFNULL(h.StarRatingId,'') AS 'Secondary supplier Hotel Star', -- Added By Sumeet helchal on 14th Nov 2017
			IFNULL(h.Longitude,'') AS 'Longitude', 	
			IFNULL(h.Latitude,'') AS 'Latitude',   
			ifnull(r.HotelId,'') AS 'Primary Supplier Hotel ID', 
			IFNULL(m.WebSiteHotelId,'') AS 'Primary Supplier Hotel Code',  
			IFNULL(m.HotelName,'')  AS 'Primary Supplier Hotel Name', 
			IFNULL(m.Hoteladdress1,'') AS 'Primary Supplier Hotel Address',  
			IFNULL(m.StarRatingId,'') AS 'Primary supplier Hotel Star',-- Added By Sumeet helchal on 14th Nov 2017
			IFNULL(m.Longitude,'') AS 'Primary Supplier Longitude',  
			IFNULL(m.Latitude,'') AS 'Primary Supplier Latitude', 
			IFNULL(DATE_FORMAT(m.LastAppearnceDate,'%d/%m/%Y'),'')  AS  'Primary Hotel Last Appearance', -- Added By Sumeet Helchal on 14th Dec 2017 	 
			IFNULL(HS.HotelStatus,'')  AS 'Hotel Status',  			
			IFNULL(CONCITY.CityName,'') AS 'City', 
			IFNULL(CONCITY.CityCode,'') AS 'Destination Code',
			IFNULL(CONCITY.CountryName,'') AS 'Country' ,
			-- CASE	
			--	WHEN r.isHotelRelationManualMatch = 0 THEN 'A'
			--	WHEN r.isHotelRelationManualMatch = 1 THEN 'M'
			--	ELSE ''
			-- END  AS 'Matching Type', 
			IFNULL(mt.MatchType,'')  AS 'Matching Type', 
			IFNULL(DATE_FORMAT(h.CreatedDate,'%d/%m/%Y'),'') AS 'Added on',
			IFNULL(DATE_FORMAT(r.MatchDate,'%d/%m/%Y'),'') AS 'Matched on', 
			IFNULL(DATE_FORMAT(h.LastAppearnceDate,'%d/%m/%Y'),'')  AS  'Last Appearance', 		  
			 r.MatchingScore AS 'Matching Score (%)'  
	 	   -- Started:Added by Sumeet Helchal for displaying flag Y or N 
		  -- , (Select [HotelMonitor].[fn_GetExcatMatchStatus](m.intHotelId,m.intSupplierId,1)) 'Primary Matched Exist'
		  -- , (Select [HotelMonitor].[fn_GetExcatMatchStatus](h.intHotelId,h.intSupplierId,2)) 'Secondary Match Exist'
		  , '' `Primary Matched Exist`
		  , '' `Secondary Match Exist`
		  -- Ended: Added by Sumeet Helchal for displaying flag Y or N 
		  ,IFNULL(h.ZoneName,'') AS 'Secondary Supplier Zone Name'-- Added By Sumeet Helchal on 14th Dec 2017 
		FROM ProbableMatchedHotels r
		Inner  JOIN  Hotels h  
		ON h.HotelId = r.ProbableMatchedHotelComHotelId   
		-- AND r.bitisManualUnmatch = 0  
		Inner join Hotels m 
		ON r.HotelId = m.HotelId  	
		INNER JOIN tbl_Competitor s 
		ON h.CompetitorId = s.Id  
		INNER JOIN `vw_dipbaghm_getcitycountry` CONCITY  
		ON h.CityId = CONCITY.CityId  
		LEFT JOIN HotelStatus HS 
		ON IFNULL(m.HotelStatusId,'') = IFNULL(HS.HotelStatusId,'')
		LEFT JOIN `MSTMatchType` mt 
		ON r.MatchType = mt.MatchType		
	    Where r.ProbableMatchedHotelId > p_intProbableMatchedHotelId
		 
	ORDER BY IFNULL(s.name,''),IFNULL(h.Hotelname,''),IFNULL(m.Hotelname,'');
		
        */
        
					truncate table  Temp_ProbableMatch;
                        
						INSERT INTO  Temp_ProbableMatch
					   (`intProbableMatchedHotelId`
						  ,`Secondary Supplier Company`
						  ,`Secondary Supplier Hotel ID`
						  ,`Secondary Website Hotel ID`
						  ,`Secondary Supplier Hotel Name`
						  ,`Secondary Supplier Hotel Address`
						  ,`Secondary supplier Hotel Star`-- Added By Sumeet helchal on 14th Nov 2017
						  ,`Longitude`
						  ,`Latitude`
						  ,`Primary Supplier Hotel ID`
						  ,`Primary Supplier Hotel Code`
						  ,`Primary Supplier Hotel Name`
						  ,`Primary Supplier Hotel Address`
						  ,`Primary supplier Hotel Star`-- Added By Sumeet helchal on 14th Nov 2017
						  ,`Primary Supplier Longitude`
						  ,`Primary Supplier Latitude`
						  ,`Primary Hotel Last Appearance`-- Added By Sumeet Helchal on 14th Dec 2017 
						  ,`Hotel Status`
						  ,`City`
						  ,`Destination Code`
						  ,`Country`
						  ,`Matching Type`
						  ,`Added on`
						  ,`Matched on`
						  ,`Last Appearance`
						  ,`Matching Score (%)`
						  ,`Primary Matched Exist`
						  ,`Secondary Match Exist`
						  ,nvcrZoneName -- Added By Sumeet Helchal on 14th Dec 2017
						  )
						SELECT  DISTINCT 
						r.ProbableMatchedHotelId, 
						IFNULL(s.name,'') AS 'Secondary Supplier Company',  			
						IFNULL(h.HotelId ,'') AS 'Secondary Supplier Hotel ID',
						IFNULL(h.WebSiteHotelId,'') AS 'Secondary Website Hotel ID',
						IFNULL(h.HotelName,'') AS 'Secondary Supplier Hotel Name',
						IFNULL(h.HotelAddress1,'') AS 'Secondary Supplier Hotel Address', 
						IFNULL(h.StarRatingId,'') AS 'Secondary supplier Hotel Star', -- Added By Sumeet helchal on 14th Nov 2017
						IFNULL(h.Longitude,'') AS 'Longitude', 	
						IFNULL(h.Latitude,'') AS 'Latitude',   
						ifnull(r.HotelId,'') AS 'Primary Supplier Hotel ID', 
						IFNULL(m.WebSiteHotelId,'') AS 'Primary Supplier Hotel Code',  
						IFNULL(m.HotelName,'')  AS 'Primary Supplier Hotel Name', 
						IFNULL(m.Hoteladdress1,'') AS 'Primary Supplier Hotel Address',  
						IFNULL(m.StarRatingId,'') AS 'Primary supplier Hotel Star',-- Added By Sumeet helchal on 14th Nov 2017
						IFNULL(m.Longitude,'') AS 'Primary Supplier Longitude',  
						IFNULL(m.Latitude,'') AS 'Primary Supplier Latitude', 
						IFNULL(DATE_FORMAT(m.LastAppearnceDate,'%d/%m/%Y'),'')  AS  'Primary Hotel Last Appearance', -- Added By Sumeet Helchal on 14th Dec 2017 	 
						IFNULL(HS.HotelStatus,'')  AS 'Hotel Status',  			
						IFNULL(CONCITY.CityName,'') AS 'City', 
						IFNULL(CONCITY.CityCode,'') AS 'Destination Code',
						IFNULL(CONCITY.CountryName,'') AS 'Country' ,
						-- CASE	
						--	WHEN r.isHotelRelationManualMatch = 0 THEN 'A'
						--	WHEN r.isHotelRelationManualMatch = 1 THEN 'M'
						--	ELSE ''
						-- END  AS 'Matching Type', 
						IFNULL(mt.MatchType,'')  AS 'Matching Type', 
						IFNULL(DATE_FORMAT(h.CreatedDate,'%d/%m/%Y'),'') AS 'Added on',
						IFNULL(DATE_FORMAT(r.MatchDate,'%d/%m/%Y'),'') AS 'Matched on', 
						IFNULL(DATE_FORMAT(h.LastAppearnceDate,'%d/%m/%Y'),'')  AS  'Last Appearance', 		  
						 r.MatchingScore AS 'Matching Score (%)'  
					   -- Started:Added by Sumeet Helchal for displaying flag Y or N 
					  -- , (Select [HotelMonitor].[fn_GetExcatMatchStatus](m.intHotelId,m.intSupplierId,1)) 'Primary Matched Exist'
					  -- , (Select [HotelMonitor].[fn_GetExcatMatchStatus](h.intHotelId,h.intSupplierId,2)) 'Secondary Match Exist'
					  , '' `Primary Matched Exist`
					  , '' `Secondary Match Exist`
					  -- Ended: Added by Sumeet Helchal for displaying flag Y or N 
					  ,IFNULL(h.ZoneName,'') AS 'Secondary Supplier Zone Name'-- Added By Sumeet Helchal on 14th Dec 2017 
					FROM ProbableMatchedHotels r
					Inner  JOIN  Hotels h  
					ON h.HotelId = r.ProbableMatchedHotelComHotelId   
					-- AND r.bitisManualUnmatch = 0  
					Inner join Hotels m 
					ON r.HotelId = m.HotelId  	
					INNER JOIN tbl_Competitor s 
					ON h.CompetitorId = s.Id  
					INNER JOIN `vw_dipbaghm_getcitycountry` CONCITY  
					ON h.CityId = CONCITY.CityId  
					LEFT JOIN HotelStatus HS 
					ON IFNULL(m.HotelStatusId,'') = IFNULL(HS.HotelStatusId,'')
					LEFT JOIN MSTMatchType mt 
					ON r.MatchType = mt.MatchType		
					Where r.ProbableMatchedHotelId > p_intProbableMatchedHotelId
					 
				ORDER BY IFNULL(s.name,''),IFNULL(h.Hotelname,''),IFNULL(m.Hotelname,'');

			  
END ;;
