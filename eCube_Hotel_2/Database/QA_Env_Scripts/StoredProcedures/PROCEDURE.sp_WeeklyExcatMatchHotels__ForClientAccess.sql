DELIMITER ;;

CREATE PROCEDURE `sp_WeeklyExcatMatchHotels__ForClientAccess`(
	p_intHotelRelationId Longtext
)
BEGIN  
			Drop temporary table if exists Temp_W;
            
            Create temporary table Temp_W 
            as
			SELECT  DISTINCT -- r.intHotelRelationId 
			-- Top 500
			r.HotelRelationId, 
			IFNULL(s.name,'') AS 'Secondary Supplier Company',  			
			IFNULL(h.Hotelid ,'') AS 'Secondary Supplier Hotel ID',
			IFNULL(h.WebSiteHotelId,'') AS 'Secondary Website Hotel ID',
			IFNULL(h.HotelName,'') AS 'Secondary Supplier Hotel Name',
			IFNULL(h.HotelAddress1,'') AS 'Secondary Supplier Hotel Address', 
			IFNULL(h.StarRatingId,'') AS 'Secondary Supplier Hotel Star',-- Added By Sumeet Helchal on 14th Dec 2017 
			IFNULL(h.Longitude,'') AS 'Longitude', 	
			IFNULL(h.Latitude,'') AS 'Latitude',   
			r.HotelId  AS 'Primary Supplier Hotel ID', 
			IFNULL(m.WebSiteHotelId,'') AS 'Primary Supplier Hotel Code',  
			IFNULL(m.HotelName,'')  AS 'Primary Supplier Hotel Name',  
			IFNULL(HS.HotelStatus,'')  AS 'Hotel Status',  
			IFNULL(m.HotelAddress1,'') AS 'Primary Hotel Address',-- Added By Sumeet Helchal on 16th Oct 2017 
			IFNULL(m.StarRatingId,'') AS 'Primary Supplier Hotel Star',-- Added By Sumeet Helchal on 14th Dec 2017 
			IFNULL(m.Longitude,'') AS 'Primary Hotel Longitude',-- Added By Sumeet Helchal on 16th Oct 2017
			IFNULL(m.Latitude,'') AS 'Primary Hotel Latitude',-- Added By Sumeet Helchal on 16th Oct 2017			
			IFNULL(CONCITY.CityName,'') AS 'City', 
			IFNULL(CONCITY.CityCode,'') AS 'Destination Code',
			IFNULL(CONCITY.CountryName,'') AS 'Country' ,
			CASE	
				WHEN r.isHotelRelationManualMatch = 0 THEN 'A'
				WHEN r.isHotelRelationManualMatch = 1 THEN 'M'
				ELSE ''
			END  AS 'Matching Type', 
			IFNULL(DATE_FORMAT(h.CreatedDate,'%d/%m/%Y'),'') AS 'Added on',
			IFNULL(DATE_FORMAT(r.MatchDate,'%d/%m/%Y'),'') AS 'Matched on', 
			IFNULL(DATE_FORMAT(h.LastAppearnceDate,'%d/%m/%Y'),'')  AS  'Last Appearance',
			IFNULL(DATE_FORMAT(m.LastAppearnceDate,'%d/%m/%Y'),'')  AS  'Primary Hotel Last Appearance'  -- Added By Sumeet Helchal on 16th Oct 2017 		  
			,IFNULL(h.ZoneName,'') AS 'Secondary Supplier Zone Name'-- Added By Sumeet Helchal on 14th Dec 2017   
			FROM 	HotelRelation r   
			Inner JOIN Hotels h 
			ON   h.HotelId = r.HotelRelationComHotelId   
			AND r.isHotelRelationManualMatch = 0  
			Inner JOIN Hotels m 
			ON r.HotelId = m.HotelId  	
			INNER JOIN tbl_Competitor s 
			ON h.CompetitorId = s.Id  
			INNER JOIN `vw_dipbaghm_getcitycountry` CONCITY  
			ON h.CityId = CONCITY.CityId  
			LEFT JOIN HotelStatus HS 
			ON IFNULL(m.CompetitorId,'') = IFNULL(HS.HotelStatusId,'')
			-- Added by Bhushan Gaud Start
			Where r.HotelRelationId > p_intHotelRelationId;	    

			
            drop temporary table if exists Temp_Wek_temp;
			create temporary  table Temp_Wek_temp like Temp_W;
            insert into Temp_Wek_temp select * from Temp_W;

			UPDATE Temp_W T1 
			INNER JOIN Temp_Wek_temp T2
			ON T1.`Secondary Supplier Hotel ID` = T2.`Secondary Supplier Hotel ID` 
			AND T1.`Primary Supplier Hotel ID`  = T2.`Primary Supplier Hotel ID`
			AND T1.`Matching Type` = 'A' 
			AND T2.`Matching Type` = 'M' 
			SET T1.`Matching Type` = T2.`Matching Type`;

	
            
            SELECT DISTINCT 
			HotelRelationId,
			`Secondary Supplier Company`,
			`Secondary Supplier Hotel ID`,
			`Secondary Website Hotel ID`,
			REPLACE(`Secondary Supplier Hotel Name`,',','')
			`Secondary Supplier Hotel Name `,
			REPLACE(`Secondary Supplier Hotel Address`,',','') `Secondary Supplier Hotel Address`,
			REPLACE(`Secondary Supplier Hotel Star`,',','') `Secondary Supplier Hotel Star`,-- Added By Sumeet Helchal on 14th Dec 2017 
			ifnull(Longitude,'') `Longitude`,
			ifnull(Latitude,'') `Latitude`,
			IFNULL(`Primary Supplier Hotel ID`,'') `Primary Supplier Hotel ID`,
			ifnull(`Primary Supplier Hotel Code`,'') `Primary Supplier Hotel Code`,
			REPLACE(`Primary Supplier Hotel Name`,',','')`Primary Supplier Hotel Name`,
			ifnull(`Hotel Status`,'') `Hotel Status`, 
			ifnull(`Primary Hotel Address`,'') `Primary Hotel Address`,-- Added By Sumeet Helchal on 16th Oct 2017
			REPLACE(`Primary Supplier Hotel Star`,',','') `Primary Supplier Hotel Star`,-- Added By Sumeet Helchal on 14th Dec 2017 
			ifnull(`Primary Hotel Longitude`,'') `Primary Hotel Longitude`, -- Added By Sumeet Helchal on 16th Oct 2017
			ifnull(`Primary Hotel Latitude`,'') `Primary Hotel Latitude`, -- Added By Sumeet Helchal on 16th Oct 2017
			ifnull(`Destination Code`,'') `Destination Code`,
			ifnull(City,'') `City`,
			ifnull(Country,'')  `Country`,
			`Matching Type`,
			`Added on`,
			`Matched on`,
			`Last Appearance`,
			`Primary Hotel Last Appearance` -- Added By Sumeet Helchal on 16th Oct 2017 
			,`Secondary Supplier Zone Name`-- Added By Sumeet Helchal on 14th Dec 2017  
		FROM Temp_W;

					INSERT INTO  Temp_ExcatMatch
					   (`intHotelRelationId`
					   ,`Secondary Supplier Company`
					   ,`Secondary Supplier Hotel ID`
					   ,`Secondary Website Hotel ID`
					   ,`Secondary Supplier Hotel Name`
					   ,`Secondary Supplier Hotel Address`
					   ,`Secondary Supplier Hotel Star` -- Added By Sumeet Helchal on 14th Dec 2017 
					   ,`Longitude`
					   ,`Latitude`
					   ,`Primary Supplier Hotel ID`
					   ,`Primary Supplier Hotel Code`
					   ,`Primary Supplier Hotel Name`
					   ,`Hotel Status`
					   ,`Primary Supplier Hotel Address`-- Added By Sumeet Helchal on 16th Oct 2017 
					   ,`Primary Supplier Hotel Star`-- Added By Sumeet Helchal on 14th Dec 2017 	
					   ,`Primary Hotel Longitude`-- Added By Sumeet Helchal on 16th Oct 2017 	
					   ,`Primary Hotel Latitude`-- Added By Sumeet Helchal on 16th Oct 2017 
					   ,`Destination Code`
					   ,`City`
					   ,`Country`
					   ,`Matching Type`
					   ,`Added on`
					   ,`Matched on`
					   ,`Last Appearance`
					   ,`Primary Hotel Last Appearance`-- Added By Sumeet Helchal on 16th Oct 2017 
					   ,nvcrZoneName -- Added By Sumeet Helchal on 14th Dec 2017 	
					   )
					SELECT DISTINCT 
					HotelRelationId,
					`Secondary Supplier Company`,
					`Secondary Supplier Hotel ID`,
					`Secondary Website Hotel ID`,
					REPLACE(`Secondary Supplier Hotel Name`,',','')
					`Secondary Supplier Hotel Name `,
					REPLACE(`Secondary Supplier Hotel Address`,',','') `Secondary Supplier Hotel Address`,
					REPLACE(`Secondary Supplier Hotel Star`,',','') `Secondary Supplier Hotel Star`,-- Added By Sumeet Helchal on 14th Dec 2017 
					ifnull(Longitude,'') `Longitude`,
					ifnull(Latitude,'') `Latitude`,
					IFNULL(`Primary Supplier Hotel ID`,'') `Primary Supplier Hotel ID`,
					ifnull(`Primary Supplier Hotel Code`,'') `Primary Supplier Hotel Code`,
					REPLACE(`Primary Supplier Hotel Name`,',','')`Primary Supplier Hotel Name`,
					ifnull(`Hotel Status`,'') `Hotel Status`, 
					ifnull(`Primary Hotel Address`,'') `Primary Hotel Address`,-- Added By Sumeet Helchal on 16th Oct 2017
					REPLACE(`Primary Supplier Hotel Star`,',','') `Primary Supplier Hotel Star`,-- Added By Sumeet Helchal on 14th Dec 2017 
					ifnull(`Primary Hotel Longitude`,'') `Primary Hotel Longitude`, -- Added By Sumeet Helchal on 16th Oct 2017
					ifnull(`Primary Hotel Latitude`,'') `Primary Hotel Latitude`, -- Added By Sumeet Helchal on 16th Oct 2017
					ifnull(`Destination Code`,'') `Destination Code`,
					ifnull(City,'') `City`,
					ifnull(Country,'')  `Country`,
					`Matching Type`,
					`Added on`,
					`Matched on`,
					`Last Appearance`,
					`Primary Hotel Last Appearance` -- Added By Sumeet Helchal on 16th Oct 2017 
					,`Secondary Supplier Zone Name`-- Added By Sumeet Helchal on 14th Dec 2017  
				FROM Temp_W;


		DROP temporary TABLE Temp_W;
	
	/**** End: Added by Kiran.Kadam on 03-Aug-2015  */  
  
END ;;
