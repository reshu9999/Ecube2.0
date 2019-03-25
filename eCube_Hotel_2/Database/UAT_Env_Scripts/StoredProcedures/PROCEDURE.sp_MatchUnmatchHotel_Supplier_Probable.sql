DELIMITER ;;

CREATE PROCEDURE `sp_MatchUnmatchHotel_Supplier_Probable`(
	p_intCityId LONGTEXT,  
	p_nvcrSupplierId LONGTEXT  
)
BEGIN

	
    call sp_splt(p_intCityId,',');
    
    Drop Temporary Table If Exists Temp_City;
    create Temporary Table Temp_City
    As
    Select items As CityID From SplitValues;
    
    call sp_splt(p_nvcrSupplierId,',');
    
    Drop Temporary Table If Exists Temp_Supplier;
    create Temporary Table Temp_Supplier
    As
    Select items As SupplierID From SplitValues;
    

	Drop Temporary Table If Exists TempData;
	Create Temporary Table TempData
	As 
	SELECT   distinct
		ifnull(s.`name`,'') AS 'Secondary Supplier Company', 
		m.HotelId  as	'Primary Supplier Hotel ID', 
		ifnull(m.websitehotelid,'') AS 'Primary Supplier Hotel Code',  
		ifnull(m.hotelname,'')  AS 'Primary Supplier Hotel Name', 
		ifnull(hs.HotelStatus,'')  AS 'Primary supplier Hotel Status',  
		ifnull(m.HotelAddress1,'') As 'Primary Supplier Hotel Address',  
		ifnull(m.HotelStar,'') As 'Primary supplier Hotel Star', 
		ifnull(m.Longitude,'') as 'Primary Supplier Longitude', 
		ifnull(m.Latitude,'') as 'Primary Supplier Latitude',   
		ifnull(h.hotelid ,'') as 'Secondary Supplier Hotel ID',
		ifnull(h.websitehotelid,'') as 'Secondary Website Hotel ID', 
		ifnull(h.hotelname,'') AS 'Secondary Supplier Hotel Name',
		ifnull(h.HotelAddress1,'') As 'Secondary Supplier Hotel Address', 
		ifnull(h.HotelStar,'') As 'Secondary supplier Hotel Star', 
		ifnull(h.Longitude,'') as 'Secondary Supplier Longitude', 
		ifnull(h.Latitude,'') as 'Secondary Supplier Latitude',   
		ifnull(CONCITY.nvcrCityCode,'') AS 'Destination Code',		   
		ifnull(CONCITY.nvcrCityName,'') AS 'City',		   
		ifnull(CONCITY.nvcrCountryName,'') AS 'Country' ,		     
		mt.MatchType AS 'Matching Type', 
		ifnull(DATE_FORMAT(h.sdtAddedDateTime,'%d/%m/%Y'),'') AS 'Added on (Secondary Supplier)',
		ifnull(DATE_FORMAT(r.sdtmMatchedDate,'%d/%m/%Y'),'') AS 'Matched on', 
		ifnull(DATE_FORMAT(h.sdtLastAppearnceDate,'%d/%m/%Y'),'')  AS  'Secondary Hotel Last Appearance', 
		ifnull(DATE_FORMAT(m.sdtLastAppearnceDate,'%d/%m/%Y'),'')  AS  'Primary Hotel Last Appearance', 
		ifnull(r.MatchingScore,'') AS 'Matching Score (%)' 
		,(Select fn_GetExcatMatchStatus(m.intHotelId,h.intSupplierId,1)) 'Primary Matched Exist'
		,(Select fn_GetExcatMatchStatus(h.intHotelId,h.intSupplierId,2)) 'Secondary Match Exist'
		,ifnull(h.nvcrZoneName ,'') as 'Secondary Supplier Zone Name' 

	FROM	Hotels h   
	Inner Join 	Temp_City MC
	On h.intCityId = MC.CityID  
	Inner Join 	Temp_Supplier MS
	On h.CompetitorId = MS.SupplierID
	LEFT OUTER JOIN ProbableMatchedHotels r   ON h.HotelId = r.ProbableMatchedHotelComHotelId   
	LEFT OUTER JOIN Hotels m  ON r.HotelId = m.HotelId  
	INNER JOIN tbl_Competitor s  ON h.CompetitorId = s.Id  
    INNER JOIN vw_DipBagHM_GetCityCountry CONCITY ON H.CityId = CONCITY.CityId 
	Inner Join MSTMatchType mt on mt.MatchType = r.MatchType 
	LEFT JOIN HotelStatus hs  ON ifnull(m.HotelStatusId,'') = IFNULL(hs.HotelStatusId,'')
		ORDER BY ifnull(s.nvcrsuppliername,''),ifnull(h.nvcrHotelname,''),ifnull(m.nvcrHotelname,'');
 
/*
	SELECT DISTINCT `Secondary Supplier Company`,
		ifnull(cast(`Primary Supplier Hotel ID` as nvarchar(50)),'') as Primary Supplier Hotel ID,
		`Primary Supplier Hotel Code`,
		replace(`Primary Supplier Hotel Name`,',','')Primary Supplier Hotel Name,
		replace(`Primary supplier Hotel Status`,',','') Primary supplier Hotel Status, 
		replace(`Primary Supplier Hotel Address`,',','')Primary Supplier Hotel Address,
		replace(`Primary supplier Hotel Star`,',','')Primary supplier Hotel Star,
		`Primary Supplier Longitude`,
		`Primary Supplier Latitude`,
		`Secondary Supplier Hotel ID`,
		`Secondary Website Hotel ID`,
		replace(`Secondary Supplier Hotel Name`,',','')
		Secondary Supplier Hotel Name ,
		replace(`Secondary Supplier Hotel Address`,',','')Secondary Supplier Hotel Address,
		replace(`Secondary supplier Hotel Star`,',','')Secondary supplier Hotel Star,
		`Secondary Supplier Longitude`,`Secondary Supplier Latitude`,		
		`Destination Code`,
		City,
		Country,
		`Matching Type` ,
		`Added on (Secondary Supplier)`,
		`Matched on`,
		`Secondary Hotel Last Appearance`,
		`Primary Hotel Last Appearance`,
		 `Matching Score (%)`
		  , `Primary Matched Exist`
		  , `Secondary Match Exist`
		  ,`Secondary Supplier Zone Name` 
	FROM #Temp 
*/
	DROP TABLE TempData;
	
  
END ;;
