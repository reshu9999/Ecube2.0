DELIMITER ;;

CREATE PROCEDURE `Delete_Primary_secondary_Hotel_Weekly`()
BEGIN


  
			Delete From HotelRelation WHere HotelRelationComHotelId in 
			(
			Select HotelId  From Hotels Where ifnull(cast(LastAppearnceDate as date),'1900-01-01') < ifnull(cast(CURRENT_TIMESTAMP()-42 as date),'1900-01-01')
			And CompetitorId Not in (1,6,25,89,90,91,94,95,88)
			-- Order by  sdtLastAppearnceDate desc
			);


			Delete From ProbableMatchedHotels WHere ProbableMatchedHotelComHotelId in 
			(
			Select HotelId  From Hotels Where ifnull(cast(LastAppearnceDate as date),'1900-01-01') < ifnull(cast(CURRENT_TIMESTAMP()-42 as date) ,'1900-01-01')
			And CompetitorId Not in (1,6,25,89,90,91,94,95,88)
			-- Order by  sdtLastAppearnceDate desc
			);
            
            
            
            -- new code added for handle can not delete paratent row a foregin key as discussed bhushan
            -- ProbableMatchedHotelComHotelId column use as disucced 
			   -- new query          
			Delete From ProbableMatchedHotels WHere ProbableMatchedHotelComHotelId in 
            (
             Select HotelId   From Hotels Where ifnull(cast(LastAppearnceDate as date),'1900-01-01') < ifnull(cast(CURRENT_TIMESTAMP()-42 as date),'1900-01-01')
			And CompetitorId Not in (1,6,25,89,90,91,94,95,88)
			);
            
				-- new query 
			Delete From hotelgroupdetails WHere HotelId in 
            (
             Select HotelId   From Hotels   Where ifnull(cast(LastAppearnceDate as date),'1900-01-01') < ifnull(cast(CURRENT_TIMESTAMP()-42 as date),'1900-01-01')
			And CompetitorId Not in (1,6,25,89,90,91,94,95,88)
			);
            
                 -- org query 
            Delete From Hotels Where ifnull(cast(LastAppearnceDate as date),'1900-01-01') < ifnull(cast(CURRENT_TIMESTAMP()-42 as date),'1900-01-01')
			And CompetitorId Not in (1,6,25,89,90,91,94,95,88);

	    
    
    
            Delete From HotelRelation WHere HotelId in 
			(
			Select HotelId From Hotels WHere HotelId Not in 
			(
			Select MH.HotelId
			From TempHotelMaster T  	Inner Join cities MC
			On T.Citycode = MC.CityCode
			Inner Join Hotels MH 
			On T.Websitehotelcode = MH.WebSiteHotelId
			And MC.CityId = MH.CityId
			And MH.CompetitorId in (1,6,25)
			)
			And CompetitorId  in (1,6,25) -- and intHotelId in (1526623,1526640,1526665)
			);
			
            
            
           -- error 19:11:50	call USP_SendMail_hoteldeletion_task()	Error Code: 1093. You can't specify target table 'hotels' for update in FROM clause	0.000 sec

			-- for above error temp table craeted 		
            
            drop temporary table if exists hotels_temp;
            create temporary table hotels_temp like Hotels; 
            
            -- code for hotel_groupdetails
			
            delete From hotelgroupdetails WHere HotelId Not in 
			(
			Select MH.HotelId
			From TempHotelMaster T  	Inner Join cities MC
			On T.Citycode = MC.CityCode
			Inner Join hotels_temp MH 
			On T.Websitehotelcode = MH.WebSiteHotelId
			And MC.CityId = MH.CityId
			And MH.CompetitorId in (1,6,25)
			);
			-- And CompetitorId  in (1,6,25);  -- change 
            
           	delete From ProbableMatchedHotels WHere ProbableMatchedHotelComHotelId Not in 
			(
			Select MH.HotelId
			From TempHotelMaster T  Inner Join cities MC
			On T.Citycode = MC.CityCode
			Inner Join hotels_temp MH 
			On T.Websitehotelcode = MH.WebSiteHotelId
			And MC.CityId = MH.CityId
			And MH.CompetitorId in (1,6,25)
			);
			-- And CompetitorId  in (1,6,25); --change column not present
            
			delete From Hotels WHere HotelId Not in 
			(
			Select MH.HotelId
			From TempHotelMaster T  Inner Join cities MC
			On T.Citycode = MC.CityCode
			Inner Join hotels_temp MH 
			On T.Websitehotelcode = MH.WebSiteHotelId
			And MC.CityId = MH.CityId
			And MH.CompetitorId in (1,6,25)
			)
			And CompetitorId  in (1,6,25);
			
            drop temporary table if exists hotels_temp;

END ;;
