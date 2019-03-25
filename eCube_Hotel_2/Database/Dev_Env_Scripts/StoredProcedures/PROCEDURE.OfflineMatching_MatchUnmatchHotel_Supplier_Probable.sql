DELIMITER ;;

CREATE PROCEDURE `OfflineMatching_MatchUnmatchHotel_Supplier_Probable`(
       p_intCityId LONGTEXT,  
       p_nvcrSupplierId LONGTEXT  
)
BEGIN  

		
		     
        
				
 
				
                
				Call sp_split(p_intCityId,',');
				
                Drop Temporary Table If exists Temp_intCityId;        
				CREATE TEMPORARY TABLE Temp_intCityId     
				(intCityId int NOT NULL);

				Insert into Temp_intCityId
				Select items from SplitValue; 
                
                
                
				Call sp_split(p_nvcrSupplierID,',');
				
				Drop Temporary Table If exists Temp_SupplierID;        
				CREATE TEMPORARY TABLE Temp_SupplierID        
				(intSupplierId int NOT NULL);

				Insert into Temp_SupplierID
				Select items from SplitValue; 

			
				drop temporary table if exists Temp_MatchUnmatchHotel_Supplier_Probable;
				 Create temporary table Temp_MatchUnmatchHotel_Supplier_Probable
				 AS
        
				SELECT   distinct
				ifnull(s.name,'') AS 'Secondary Supplier Company', 
                m.HotelId  as     'Primary Supplier Hotel ID', 
                ifnull(m.WebSiteHotelId,'') AS 'Primary Supplier Hotel Code',  
				ifnull(m.HotelName,'')  AS 'Primary Supplier Hotel Name', 
                ifnull(hs.HotelStatus,'')  AS 'Primary supplier Hotel Status', -- Added By Sumeet Helchal on 13thNov2017
                ifnull(m.HotelAddress1,'') As 'Primary Supplier Hotel Address',  
                ifnull(m.StarRatingId,'') As 'Primary supplier Hotel Star',-- Added By Sumeet Helchal on 13thNov2017
                ifnull(m.Longitude,'') as 'Primary Supplier Longitude',   --  Added by Shree.Maskar on 26-May-2016
                ifnull(m.Latitude,'') as 'Primary Supplier Latitude',   --  Added by Shree.Maskar on 26-May-2016  
                ifnull(h.HotelId ,'') as 'Secondary Supplier Hotel ID',
                ifnull(h.WebSiteHotelId,'') as 'Secondary Website Hotel ID',--  Added by Shree.Maskar on 26-May-2016
                ifnull(h.HotelName,'') AS 'Secondary Supplier Hotel Name',
                ifnull(h.HotelAddress1,'') As 'Secondary Supplier Hotel Address', 
                ifnull(h.StarRatingId,'') As 'Secondary supplier Hotel Star',-- Added By Sumeet Helchal on 13thNov2017
                ifnull(h.Longitude,'') as 'Secondary Supplier Longitude',        --  Added by Shree.Maskar on 26-May-2016
                ifnull(h.Latitude,'') as 'Secondary Supplier Latitude',   --  Added by Shree.Maskar on 26-May-2016
                ifnull(CONCITY.CityCode,'') AS 'Destination Code',              
                ifnull(CONCITY.CityName,'') AS 'City',            
                ifnull(CONCITY.CountryName,'') AS 'Country' ,
                mt.MatchType AS 'Matching Type', 
                ifnull(DATE_FORMAT(h.CreatedDate,'%d/%m/%Y'),'') AS 'Added on (Secondary Supplier)',-- Modified By Sumeet Helchal on 29thdec2017
                ifnull(DATE_FORMAT(r.MatchDate,'%d/%m/%Y'),'') AS 'Matched on', --  Added by Nilam.Pawashe on 26-May-2016
                ifnull(DATE_FORMAT(h.LastAppearnceDate,'%d/%m/%Y'),'')  AS  'Secondary Hotel Last Appearance',-- Modified By Sumeet Helchal on 29thdec2017 
                ifnull(DATE_FORMAT(m.LastAppearnceDate,'%d/%m/%Y'),'')  AS  'Primary Hotel Last Appearance',-- Added By Sumeet Helchal on 29thdec2017 
                ifnull(r.MatchingScore,'') AS 'Matching Score (%)' -- Modified By Sumeet Helchal on 29thdec2017
                ,(Select fn_GetExcatMatchStatus(m.HotelId,h.CompetitorId,1)) 'Primary Matched Exist'
                ,(Select fn_GetExcatMatchStatus(h.HotelId,h.CompetitorId,2)) 'Secondary Match Exist'
                ,ifnull(h.ZoneName ,'') as 'Secondary Supplier Zone Name'-- Added By Sumeet Helchal on 29thdec2017 
				FROM  Hotels h
				Inner Join (SELECT intCityId from Temp_intCityId) MC  -- change for split  
				On h.CityId = MC.intCityId 
				Inner Join (SELECT intSupplierId from Temp_SupplierID) MS -- change for split
				On h.CompetitorId = MS.intSupplierId
				LEFT OUTER JOIN ProbableMatchedHotels r 
				ON h.HotelId = r.ProbableMatchedHotelComHotelId   
				LEFT OUTER JOIN Hotels m 
				ON r.HotelId = m.HotelId  
				INNER JOIN tbl_Competitor s
				ON h.CompetitorId = s.Id  
				INNER JOIN `vw_dipbaghm_getcitycountry` CONCITY 
				ON h.CityId = CONCITY.CityId 
				Inner Join MSTMatchType mt 
				on mt.MatchType = r.MatchType 
				LEFT JOIN HotelStatus hs 
				ON IFNULL(m.HotelStatusId,'') = IFNULL(hs.HotelStatusId,'')
              
-- WHERE 
       --     h.intCityId IN (SELECT Items FROM [dbo].[Split](@intCityId,','))
       --     AND h.intSupplierId IN (SELECT Items FROM [dbo].[Split](@nvcrSupplierId,',')) 
			ORDER BY ifnull(s.name,''),ifnull(h.Hotelname,''),ifnull(m.Hotelname,'');
  
  


			 SELECT DISTINCT `Secondary Supplier Company`,
             ifnull(cast(`Primary Supplier Hotel ID` as char(50)),'') as `Primary Supplier Hotel ID`,
              -- case 
              -- when isnull([Primary Supplier Hotel ID],0) = 0 then ''
              -- else isnull([Primary Supplier Hotel ID],'') end as [Primary Supplier Hotel ID],
             `Primary Supplier Hotel Code`,
             replace(`Primary Supplier Hotel Name`,',','') as `Primary Supplier Hotel Name`,
             replace(`Primary supplier Hotel Status`,',','')  as `Primary supplier Hotel Status`,-- Added By Sumeet Helchal on 13thNov2017
             replace(`Primary Supplier Hotel Address`,',','') as `Primary Supplier Hotel Address`,
             replace(`Primary supplier Hotel Star`,',','') as `Primary supplier Hotel Star`,-- Added By Sumeet Helchal on 13thNov2017
             `Primary Supplier Longitude`,
             `Primary Supplier Latitude`,
             `Secondary Supplier Hotel ID`,
             `Secondary Website Hotel ID`,
             replace(`Secondary Supplier Hotel Name`,',','') as `Secondary Supplier Hotel Name`,
             replace(`Secondary Supplier Hotel Address`,',','') as `Secondary Supplier Hotel Address`,
             replace(`Secondary supplier Hotel Star`,',','') as `Secondary supplier Hotel Star`,-- Added By Sumeet Helchal on 13thNov2017
             `Secondary Supplier Longitude`,`Secondary Supplier Latitude`,        
             `Destination Code`,
             City,
             Country,
             `Matching Type` ,
             `Added on (Secondary Supplier)`,-- Modified By Sumeet Helchal on 29thdec2017
             `Matched on`,
             `Secondary Hotel Last Appearance`,-- Modified By Sumeet Helchal on 29thdec2017
             `Primary Hotel Last Appearance`,-- Added By Sumeet Helchal on 29thdec2017
             `Matching Score (%)`
			,`Primary Matched Exist`
			,`Secondary Match Exist`
             ,`Secondary Supplier Zone Name`-- Added By Sumeet Helchal on 29thdec2017 
              FROM Temp_MatchUnmatchHotel_Supplier_Probable;

      
			  drop temporary table Temp_MatchUnmatchHotel_Supplier_Probable;
 
END ;;
