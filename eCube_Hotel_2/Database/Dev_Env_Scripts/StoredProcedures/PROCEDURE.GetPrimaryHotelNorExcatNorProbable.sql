DELIMITER ;;

CREATE PROCEDURE `GetPrimaryHotelNorExcatNorProbable`(  
p_nvcrSupplierId NVARCHAR(500),
p_intCityId NVARCHAR(500))
BEGIN
  DECLARE v_intAdmin int;
			
     
            
					Call sp_split(p_nvcrSupplierId,',');
					Drop Temporary Table If exists Temp_Supplier_Nor_E_P;        
					CREATE TEMPORARY TABLE Temp_Supplier_Nor_E_P     
					(intSupplierId int  NULL);

					Insert into Temp_Supplier_Nor_E_P
					Select items from SplitValue; 


				
					Call sp_split(p_intCityId,',');
					Drop Temporary Table If exists Temp_CityId_Nor_E_P;        
					CREATE TEMPORARY TABLE Temp_CityId_Nor_E_P     
					(intCityId int NULL);

					Insert into Temp_CityId_Nor_E_P
					Select items from SplitValue; 

                
					drop temporary table if exists temp_MSTPrimaryHotel;
                    
					Create temporary table  temp_MSTPrimaryHotel
					AS 
					  SELECT
					MH.*,supp.secondaysupplierid 
					FROM Hotels MH
					Cross Join    (SELECT
					intSupplierId as secondaysupplierid
					FROM Temp_Supplier_Nor_E_P) supp
					WHERE CompetitorId = 1
					AND CityId IN (SELECT
					intCityId
					FROM Temp_CityId_Nor_E_P);


   -- drop table #temp_MSTPrimaryHotel

					ALTER TABLE temp_MSTPrimaryHotel ADD nvcrExcatMatchStatus nvarchar(5);
					ALTER TABLE temp_MSTPrimaryHotel ADD nvcrProbableMatchStatus nvarchar(5);
					ALTER TABLE temp_MSTPrimaryHotel ADD NvcrSecondarySupplier nvarchar(50);



					UPDATE temp_MSTPrimaryHotel
					SET nvcrExcatMatchStatus = 'N',
					 nvcrProbableMatchStatus = 'N';
							-- 694
				
                
                
					UPDATE temp_MSTPrimaryHotel PH INNER JOIN  HotelRelation HR
					ON HR.HotelId = PH.HotelId 
                    
				  	INNER JOIN Hotels SH
					ON HR.HotelRelationComHotelId = SH.HotelId
                    and SH.CompetitorId=PH.secondaysupplierid
					-- AND HR.bitIsManualUnmatch = 0
      				SET nvcrExcatMatchStatus = 'Y';


					DELETE FROM temp_MSTPrimaryHotel
					WHERE nvcrExcatMatchStatus = 'Y';

					UPDATE ProbableMatchedHotels PM
					INNER JOIN Hotels SH
					ON PM.ProbableMatchedHotelComHotelId = SH.HotelId
					INNER JOIN temp_MSTPrimaryHotel PH
					ON PM.HotelId = PH.HotelId
					and SH.CompetitorId=PH.secondaysupplierid
					SET nvcrProbableMatchStatus = 'Y';
      
				    DELETE FROM temp_MSTPrimaryHotel
					WHERE nvcrProbableMatchStatus = 'Y';
      
				   update temp_MSTPrimaryHotel temp
				   inner join tbl_Competitor supp
				   on temp.secondaysupplierid=supp.Id set NvcrSecondarySupplier=supp.name; 
  

  

					  SELECT DISTINCT
					  
					   REPLACE(MH.NvcrSecondarySupplier, ',', '') AS 'SecondarySupplierName',
						REPLACE(MS.name, ',', '') AS 'PrimarySupplierName',
						MH.HotelId 'PrimaryHotelId',
						REPLACE(MH.HotelName, ',', '') AS 'PrimaryHotelName',
						hs.HotelStatus AS 'HotelStatus',
						MH.WebSiteHotelId AS 'PrimaryHotelCode',
						MH.Longitude AS 'Longitude',
						MH.Latitude AS 'Latitude',
						CONCITY.CityName AS 'City',
						CONCITY.CityCode AS 'DestinationCode',
						CONCITY.CountryName AS 'Country',
						REPLACE(MH.HotelAddress1, ',', '') AS 'PrimaryHotelAddress',
						DATE_FORMAT (MH.LastAppearnceDate, '%d/%m/%Y') AS LastAppearance
						FROM temp_MSTPrimaryHotel MH
						INNER JOIN tbl_Competitor MS
						ON MH.CompetitorId = MS.Id
					  INNER JOIN `vw_dipbaghm_getcitycountry` CONCITY 
						ON MH.CityId = CONCITY.CityId
					  LEFT JOIN HotelStatus hs
						ON MH.HotelStatusId = hs.HotelStatusId;

      drop temporary table temp_MSTPrimaryHotel;
END ;;
