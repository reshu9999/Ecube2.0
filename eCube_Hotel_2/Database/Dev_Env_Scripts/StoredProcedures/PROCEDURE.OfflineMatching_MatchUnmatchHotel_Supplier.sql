DELIMITER ;;

CREATE PROCEDURE `OfflineMatching_MatchUnmatchHotel_Supplier`(
       p_intCityId LONGTEXT,  
       p_nvcrSupplierId LONGTEXT  
)
BEGIN    

							
					Call sp_split(p_intCityId,',');
					Drop Temporary Table If exists Temp_intCityId_Supplier;        
					CREATE TEMPORARY TABLE Temp_intCityId_Supplier     
					(intCityId int NOT NULL);

					Insert into Temp_intCityId_Supplier
					Select items from SplitValue; 
 
					
					Call sp_split(p_nvcrSupplierID,',');
					
					Drop Temporary Table If exists Temp_intSupplierId_Supplier;        
					CREATE TEMPORARY TABLE Temp_intSupplierId_Supplier        
					(intSupplierId int NOT NULL);

					Insert into Temp_intSupplierId_Supplier
					Select items from SplitValue; 


                    drop temporary table if exists Temp_MatchUnmatchHotel_Supplier;

					create temporary table Temp_MatchUnmatchHotel_Supplier
					 As 
					 SELECT DISTINCT  
                     s.name AS 'SupplierName',  
                     r.HotelId  'PrimarySupplierHotelId', 
                     m.WebSiteHotelId AS 'PrimarySupplierHotelCode',  
					 m.HotelName  AS 'PrimarySupplierHotelName', 
                     hs.HotelStatus AS 'HotelStatus',
                     m.HotelAddress1 as 'PrimarySupplierHotelAddress',
                     m.StarRatingId AS 'PrimarySupplierHotelStar',-- Added By Sumeet Helchal on 29th Dec 2017
                     m.Longitude as'PrimarySupplierLongitude',-- Added By Sumeet Helchal on 29th Dec 2017
                     m.Latitude as'PrimarySupplierLatitude',-- Added By Sumeet Helchal on 29th Dec 2017
                     h.HotelId  'SecondarySupplierHotelID',
                     h.WebSiteHotelId as 'SecondaryWebsiteHotelID',--  Added by Shree.Maskar on 26-May-2016
                     h.HotelName AS 'SecondarySupplierHotelName',
                     h.HotelAddress1 As 'SecondarySupplierHotelAddress', 
                     h.StarRatingId as 'SeconarySupplierHotelStar',-- Added By Sumeet Helchal on 29th Dec 2017
                     h.Longitude as 'Longitude',   --  Added by Shree.Maskar on 26-May-2016
                     h.Latitude as 'Latitude',   --  Added by Shree.Maskar on 26-May-2016
                     CONCITY.CityCode AS 'DestinationCode',
                     CONCITY.CityName AS 'City',  
					 CONCITY.CountryName AS 'Country' ,
					 CASE       
					 WHEN r.isHotelRelationManualMatch = 0 THEN 'A'
                     WHEN r.isHotelRelationManualMatch = 1 THEN 'M'
                     ELSE ''
                     END  AS 'MatchingType',                         
					  Case WHen Ifnull(DATE_FORMAT(h.CreatedDate,111),'') = '' Then '1900-01-01T00:00:00.000' Else Concat(Replace(DATE_FORMAT(h.CreatedDate,111),'/','-') , 'T00:00:00.000') End  AS 'Addedon',
					  Case WHen Ifnull(DATE_FORMAT(r.MatchDate,111),'') = '' Then '1900-01-01T00:00:00.000' Else Concat(Replace(DATE_FORMAT(r.MatchDate,111),'/','-') , 'T00:00:00.000') End  AS 'Matchedon',
					 Case WHen Ifnull(DATE_FORMAT(h.LastAppearnceDate,111),'') = '' Then '1900-01-01T00:00:00.000' Else Concat(Replace(DATE_FORMAT(h.LastAppearnceDate,111),'/','-') , 'T00:00:00.000') End  AS 'LastAppearance',
					 Case WHen Ifnull(DATE_FORMAT(m.LastAppearnceDate,111),'') = '' Then '1900-01-01T00:00:00.000' Else Concat(Replace(DATE_FORMAT(m.LastAppearnceDate,111),'/','-') , 'T00:00:00.000') End  AS 'PrimarySupplierLastAppearance',-- Added By Sumeet Helchal on 29th Dec 2017
					 IFNULL(h.ZoneName,'') AS 'SecondarySupplierZoneName'-- Added By Sumeet Helchal on 29th Dec 2017
					 FROM  Hotels h
                     LEFT OUTER JOIN HotelRelation r 
                     ON h.HotelId = r.HotelRelationComHotelId   
                    /* Chnage as unmatch table is diff
                    AND r.bitisManualUnmatch = 0  */
					LEFT OUTER JOIN Hotels m 
                    ON r.HotelId = m.HotelId       
					INNER JOIN tbl_Competitor s  
                    ON h.CompetitorId = s.Id   
                    INNER JOIN `vw_dipbaghm_getcitycountry` CONCITY 
                    ON h.CityId = CONCITY.CityId
					LEFT JOIN `HotelStatus` hs 
                    ON m.HotelStatusId =hs.HotelStatusId  
					WHERE h.CityId IN (SELECT intCityId FROM Temp_intCityId_Supplier)
					AND h.CompetitorId IN (SELECT intSupplierId FROM Temp_intSupplierId_Supplier) 
					ORDER BY s.name,h.HotelName,m.HotelName ;
                             -- change abbove line h. and m. same.
                          
                            
                    drop temporary table if exists Temp_MatchUnmatchHotel_Supplier_TEMP;
                    Create temporary table  Temp_MatchUnmatchHotel_Supplier_TEMP like Temp_MatchUnmatchHotel_Supplier;
                    insert into Temp_MatchUnmatchHotel_Supplier_TEMP select * from Temp_MatchUnmatchHotel_Supplier;
	  
					UPDATE Temp_MatchUnmatchHotel_Supplier T1 
					INNER JOIN Temp_MatchUnmatchHotel_Supplier_TEMP T2
					ON T1.SecondarySupplierHotelID = T2.SecondarySupplierHotelID
					AND T1.PrimarySupplierHotelId = T2.PrimarySupplierHotelId 
					AND T1.MatchingType = 'A' 
					AND T2.MatchingType = 'M' 
					SET T1.MatchingType = T2.MatchingType;    
					
							
                    drop temporary table if exists temp2;     
					create temporary table temp2
					select distinct  
					s.name AS 'SupplierName', 
					H.HotelId 'PrimarySupplierHotelId',
					websitehotelid as 'PrimarySupplierHotelCode', 
					hotelname as 'PrimarySupplierHotelName',  
					hs.HotelStatus AS 'HotelStatus', 
					HotelAddress1 as 'PrimarySupplierHotelAddress', 
					H.StarRatingId AS 'PrimarySupplierHotelStar',  
					H.Longitude as 'PrimarySupplierLongitude',
					H.Latitude as 'PrimarySupplierLatitude', 
					'' as 'SecondarySupplierHotelID',
					'' as  'SecondaryWebsiteHotelID',--  Added by Shree.Maskar on 26-May-2016
					'' as 'SecondarySupplierHotelName',
					'' As 'SecondarySupplierHotelAddress', 
					'' as 'SeconarySupplierHotelStar',-- Added By Sumeet Helchal on 29th Dec 2017
					'' as 'Longitude',   --  Added by Shree.Maskar on 26-May-2016
					'' as 'Latitude',   
					CONCITY.CityCode AS 'DestinationCode', 
					CONCITY.CityName AS 'City', 
					CONCITY.CountryName AS 'Country',
					'' as 'MatchingType',
					 Case WHen Ifnull(DATE_FORMAT(H.CreatedDate,111),'') = '' Then '1900-01-01T00:00:00.000' Else Concat(Replace(DATE_FORMAT(H.CreatedDate,111),'/','-') , 'T00:00:00.000') End  AS 'Addedon',
					 '1900-01-01T00:00:00.000' AS 'Matchedon',
					 '1900-01-01T00:00:00.000' AS 'LastAppearance',
					 Case WHen Ifnull(DATE_FORMAT(H.LastAppearnceDate,111),'') = '' Then '1900-01-01T00:00:00.000' Else Concat(Replace(DATE_FORMAT(H.LastAppearnceDate,111),'/','-') , 'T00:00:00.000') End  AS 'PrimarySupplierLastAppearance',   
					'' AS 'SecondarySupplierZoneName'  
					From Hotels H 
					INNER JOIN tbl_Competitor s 
					ON H.CompetitorId = s.Id   -- ID as discussed 
					INNER JOIN `vw_dipbaghm_getcitycountry` CONCITY
					ON H.CityId = CONCITY.CityId  
					LEFT JOIN `HotelStatus` hs 
					ON H.HotelStatusId =hs.HotelStatusId   
					LEFT JOIN Temp_MatchUnmatchHotel_Supplier as sec_primary_hotel
					ON H.HotelId = sec_primary_hotel.PrimarySupplierHotelId
					WHERE sec_primary_hotel.PrimarySupplierHotelId IS NULL 
						/* change  below code comeent as usermamangment not part
                        AND
						H.intsupplierid = (  
						SELECT intSupplierId   
						from Usermanagement.MstUser 
						where intUsrId = v_intAdmin)  */
					and H.CityId  IN (SELECT intCityId FROM Temp_intCityId_Supplier)
					order by CityName;  
                      
					 SELECT DISTINCT * FROM Temp_MatchUnmatchHotel_Supplier
					 union
					 select distinct * from temp2;

					 DROP temporary TABLE Temp_MatchUnmatchHotel_Supplier;
       
    
END ;;
