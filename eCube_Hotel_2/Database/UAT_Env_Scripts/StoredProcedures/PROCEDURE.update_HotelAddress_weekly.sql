DELIMITER ;;

CREATE PROCEDURE `update_HotelAddress_weekly`()
BEGIN



			DECLARE v_bitKeywordReplaceActive TINYINT DEFAULT 0;
			SELECT bitupdatehoteladdress INTO v_bitKeywordReplaceActive FROM ProcessInfo;
			
			IF(v_bitKeywordReplaceActive = 1)
			THEN
				
			UPDATE Hotels  MST
			inner join
			Hotels  MST1  
			on MST.HotelId=MST1.HotelId
			SET HotelAddress1=MST1.CrawledHotelAddress
			where
			ifnull(MST.CrawledHotelAddress,'')!='';	
			
			UPDATE Hotels  MST
			inner join
			Hotels  MST1  
			on MST.HotelId=MST1.HotelId
			SET StarRatingId=MST1.StarRatingId
			where ifnull(MST.CrawledHotelStar,'')!='';	
	
			UPDATE Hotels  MST
			inner join
			Hotels MST1  
			on MST.intHotelId=MST1.intHotelId
			SET ZoneName=MST1.ZoneName
			WHERE ifnull(MST.ZoneName,'')!='';

			end if;


/*			 -- below is the code change  and craete the #temp table
			select Intcityid,nvcrWebSiteHotelId,nvcrCrawledHotelStar,
			ROW_NUMBER() OVER (PARTITION BY Intcityid,nvcrWebSiteHotelId ORDER BY Intcityid DESC) AS rank into #temp

			from HotelMonitor.MSTHotel 
			where intSupplierId in(1,6,25) and ifnull(nvcrCrawledHotelStar,'')!='';	 

			-- select * from #temp where nvcrWebSiteHotelId='104713'
			delete from  #temp where rank>1;
		 	UPDATE hotels MST 
			SET 
		    nvcrHotelStar=Hotel.nvcrCrawledHotelStar
			inner join #temp Hotel			
			ON HOTEL.nvcrWebSiteHotelId = MST.nvcrWebSiteHotelId
			AND HOTEL.intCityID = MST.intCityID				
		   	
            drop table #temp;	
			END IF;
*/


END ;;
