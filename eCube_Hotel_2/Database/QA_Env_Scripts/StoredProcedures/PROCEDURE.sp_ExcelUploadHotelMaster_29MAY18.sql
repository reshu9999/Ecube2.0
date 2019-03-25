DELIMITER ;;

CREATE PROCEDURE `sp_ExcelUploadHotelMaster_29MAY18`(
 p_intSupplierId int,  
 p_intUserId Int,  
 out p_nvcrErrorMsg  nvarchar(200)  
 
 )
BEGIN    


   Declare v_intVersion int;
     /*
   
	 IF ((select COUNT(Websitehotelcode) from temphotelmaster where CHAR_LENGTH(RTRIM( LTRIM(rtrim(Websitehotelcode))))>0) = 0)
             THEN
               UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Website Hotel Code column having blank value',ErrorFlag = 1;  
             END IF;  
              IF((select COUNT(Hotelname) from temphotelmaster where CHAR_LENGTH(RTRIM( LTRIM(rtrim(Hotelname))))>0) = 0)
             THEN
               UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Hotel Name column having blank value',ErrorFlag = 1;  
             END IF;  
              IF((select COUNT(Starrating) from temphotelmaster where CHAR_LENGTH(RTRIM( LTRIM(rtrim(Starrating))))>0)= 0)
             THEN
               UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Star Rating column having blank value',ErrorFlag = 1;  
             END IF;  
               IF((select COUNT(Address1) from temphotelmaster where CHAR_LENGTH(RTRIM( LTRIM(rtrim(Address1))))>0) = 0)
             THEN
               UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Address1 column having blank value',ErrorFlag = 1;  
             END IF;  
             IF((select COUNT(Countrycode) from temphotelmaster where CHAR_LENGTH(RTRIM( LTRIM(rtrim(Countrycode))))>0)= 0)
             THEN
               UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Country Code column having blank value',ErrorFlag = 1;  
             END IF;  
             IF((select COUNT(Countryname) from temphotelmaster where CHAR_LENGTH(RTRIM( LTRIM(rtrim(Countryname))))>0) = 0)
             THEN
               UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Country Name column having blank value',ErrorFlag = 1;  
             END IF;  
              IF((select COUNT(ZipCode) from temphotelmaster where CHAR_LENGTH(RTRIM( LTRIM(rtrim(ZipCode))))>0) = 0)
             THEN
               UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Zip Code having blank value',ErrorFlag = 1;  
             END IF;  
             
			 
			 
			 IF((select COUNT(Citycode) from temphotelmaster where CHAR_LENGTH(RTRIM( LTRIM(rtrim(Citycode))))>0) = 0)
             THEN
               UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - City Code having blank value',ErrorFlag = 1;  
             END IF; 
                IF((select COUNT(Cityname) from temphotelmaster where CHAR_LENGTH(RTRIM( LTRIM(rtrim(Cityname))))>0) = 0)
             THEN
               UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - City Name having blank value',ErrorFlag = 1;  
             END IF; 
             
             IF((select COUNT(nvcrHotelStatus) from temphotelmaster where CHAR_LENGTH(RTRIM( LTRIM(rtrim(nvcrHotelStatus))))>0) = 0)
             THEN
               UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Hotel status having blank value',ErrorFlag = 1;  
             END IF; 
         -- End by Mahesh 20160722    
			 
			            
  
   UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Website Hotel Code Should not have blank record ',ErrorFlag = 1    
     -- FROM temphotelmaster TD    
     WHERE IFNULL(WebSiteHotelCode,'')= '' AND ErrorFlag = 0;     
       
          
	UPDATE temphotelmaster TDO
      inner join
      (    
      SELECT  WebSiteHotelCode
      FROM temphotelmaster TDI 
         
      GROUP BY WebSiteHotelCode
      HAVING Count(WebSiteHotelCode) > 1
         
     ) TDI ON   TDO.Websitehotelcode = TDI.WebSiteHotelCode AND ErrorFlag = 0  
    
    SET ErrorStatus = 'Invalid Record - Website Hotel Code Should not have duplicate record',
    ErrorFlag =1 ;  
         
       
       
       
       
       

    
       
        UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Website Hotel Code Should have numeric value ',ErrorFlag = 1     
       	WHERE ISNUMERIC(WebSiteHotelCode)=0 AND ErrorFlag = 0;   
     
     -- --------Validation for Same Websitehotel duplicate in same city-----------------		 
	
    	UPDATE temphotelmaster 
        SET ErrorStatus = 'Invalid Record - Same Websitehotel duplicate in same city ',ErrorFlag = 1  
	     
	 WHERE Websitehotelcode IN
	(
	SELECT A.Websitehotelcode from   
		 ( 
	 SELECT t1.Websitehotelcode,t1.Citycode from temphotelmaster t1  
	 Where t1.errorflag = 0  
	 group by t1.Websitehotelcode,t1.Citycode  
	 having count(Websitehotelcode)> 1
	)A
	 )
	and errorflag = 0; 
    
      
       
    
    
    UPDATE temphotelmaster  SET ErrorStatus = 'Invalid Record - Same Websitehotel duplicate in same city ',ErrorFlag = 1  

	 WHERE Websitehotelcode IN
	(
	SELECT A.Websitehotelcode from   
		 ( 
	 SELECT t1.Websitehotelcode,t1.Citycode from temphotelmaster t1
	 Where t1.errorflag = 0  
	 group by t1.Websitehotelcode,t1.Citycode  
	 having count(Websitehotelcode)> 1
	)A
	 )
	and errorflag = 0 ;
      
      -- Remain funcition craetion 
     UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Invalid Hotel Name',ErrorFlag = 1    
     WHERE  ErrorFlag = 0    and  CHAR_LENGTH(RTRIM(Hotelname))<>CHAR_LENGTH(RTRIM(udf_StripHTML(Hotelname)));
     
		UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Hotel Name Should not have blank record ',ErrorFlag = 1    
         WHERE IFNULL(Hotelname,'') = '' AND  ErrorFlag = 0;      
    
  

	 -- ------------------Update for starrating ------------------------------------------------
	 UPDATE temphotelmaster set starrating=RemoveCharctersForHotelStar(starrating); 
     UPDATE temphotelmaster set starrating = replace(starrating,'_','.'); 
	 UPDATE temphotelmaster set starrating = 0 where starrating = '' or starrating is null;
	    
     UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Star rating must be numeric ',ErrorFlag = 1    
     WHERE ISNUMERIC(Starrating)=0 AND ErrorFlag = 0;  
    -- -End Check Numeric--------------------       
      
     
     
     
      
    
     UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Country Code Should  have only 2 digit',ErrorFlag = 1    
        WHERE char_length(rtrim(Countrycode)) > 2 AND ErrorFlag = 0;    
     
      UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Country Code Should not have blank',ErrorFlag = 1    
     -- FROM temphotelmaster TD    
        WHERE IFNULL(Countrycode,'') = '' AND ErrorFlag = 0;   
        
		-- Added Start by Mahesh 20160722
		       UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Longitude Should accept only numeric , dot(.) and dash(-).',ErrorFlag = 1    
     -- FROM temphotelmaster TD    
        -- WHERE ISNUMERIC(ISNULL(Longitude,'') = '') AND ErrorFlag = 0   
        WHERE ISNUMERIC(ifnull(Longitude,''))=0 AND ErrorFlag = 0 
		-- Added by Bhushan Gaud for master list update Start
			And ifnull(Longitude,'') != ''; 
        -- Added by Bhushan Gaud for master list update End
        
          UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Latitude Should accept only numeric , dot(.) and dash(-).',ErrorFlag = 1    
     -- FROM temphotelmaster TD    
        -- WHERE ISNULL(Latitude,'') = '' AND ErrorFlag = 0   
         WHERE ISNUMERIC(ifnull(Latitude,''))=0 AND ErrorFlag = 0 
        -- End by Mahesh 20160722
		-- Added by Bhushan Gaud for master list update Start
			And ifnull(Latitude,'') != ''; 
        -- Added by Bhushan Gaud for master list update End
		
  UPDATE temphotelmaster  SET ErrorStatus = 'Invalid Record - Same Country Code mapped with different countries name',ErrorFlag = 1  
     WHERE CountryCode IN(  
     SELECT A.CountryCode from   
     (  
      SELECT t1.CountryCode,t1.CountryName from temphotelmaster t1 
      Where t1.errorflag = 0  
      group by t1.CountryCode,t1.CountryName  
     ) A  
     Where errorflag = 0      
     Group By A.CountryCode  
     Having Count(A.CountryName) > 1);
     
      UPDATE temphotelmaster t 
   	INNER JOIN MSTCountry c 
	ON t.Countrycode = c.nvcrCountryShortCode  
    SET ErrorStatus = 'Invalid Record - Same Country Code mapped with different country in master table',ErrorFlag = 1  
     WHERE CountryName <> nvcrCountryName AND errorflag = 0;  

        
      
     UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Invalid Country Name missing',ErrorFlag = 1    
     WHERE IFNULL(Countryname,'') = '' AND ErrorFlag = 0;    
     
      UPDATE temphotelmaster  SET ErrorStatus = 'Invalid Record - Same Country Name mapped with different country code in master table',ErrorFlag = 1    
     WHERE CountryName IN(  
     SELECT A.CountryName from   
     (  
      SELECT t1.CountryCode,t1.CountryName from temphotelmaster t1 
      Where t1.errorflag = 0  
      group by t1.CountryCode,t1.CountryName  
     ) A  
     Where errorflag = 0   
     Group By A.CountryName  
     Having Count(A.CountryName) > 1);    
        
      UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Hotel Status Should not have blank',ErrorFlag = 1    
     WHERE IFNULL(NvcrHotelStatus,'') = '' AND ErrorFlag = 0;  
        
      
      
      
       UPDATE temphotelmaster Set NvcrHotelStatus='Inactive' where UPPER(ltrim(rtrim(NvcrHotelStatus)))='NOT ACTIVE'; -- NOT Active\92 
     
     
     
     
  
     UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Invalid City Code missing',ErrorFlag = 1    
     -- FROM temphotelmaster TD    
     WHERE IFNULL(Citycode,'') = '' AND ErrorFlag = 0;  
  
     UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Invalid City Name missing',ErrorFlag = 1    
     -- FROM temphotelmaster TD    
     WHERE IFNULL(Cityname,'') = '' AND ErrorFlag = 0;  
     
     UPDATE temphotelmaster SET ErrorStatus = 'Invalid Record - Same city Name mapped with different city code in master table',ErrorFlag = 1  
     WHERE CityName IN(  
     SELECT A.CityName from   
     (  
      SELECT t1.CityCode,t1.CityName,t1.countrycode from temphotelmaster t1 
      Where t1.errorflag = 0  
      group by t1.CityCode,t1.CityName,t1.countrycode  
     ) A  
     Where errorflag = 0   
     Group By A.CityName , A.countrycode   
     Having Count(A.CityName) > 1) ; 
  
  

    
     
     UPDATE temphotelmaster Set ErrorStatus = 'Invalid Record - Hotel Status does not exist in Master Database',ErrorFlag = 1    
     -- select * from temphotelmaster
     WHERE IFNULL(NvcrHotelStatus,'')  Not in (Select vcrStatus From MstHotelStatus) AND ErrorFlag = 0;  
   
      


                  -- Duplicate records with combination of all in uploaded file    
    
     UPDATE temphotelmaster TDO 
	INNER JOIN    
     (    
      SELECT  Websitehotelcode,Hotelname,Starrating,Address1,Countrycode,Countryname,ZipCode,Longitude,Latitude,Citycode,Cityname  
      FROM temphotelmaster TDI 
      WHERE TDI.ErrorFlag = 0    
      GROUP BY Websitehotelcode,Hotelname,Starrating,Address1,Countrycode,Countryname,ZipCode,Longitude,Latitude,Citycode,Cityname  
      HAVING Count(Websitehotelcode) > 1    
     ) TDI    
     ON TDO.Websitehotelcode = TDI.Websitehotelcode AND    
      TDO.Hotelname = TDI.Hotelname AND    
      TDO.Starrating = TDI.Starrating AND  
      TDO.Address1 = TDI.Address1 AND    
      TDO.Countrycode = TDI.Countrycode AND    
      TDO.Countryname = TDI.Countryname AND  
      TDO.ZipCode = TDI.ZipCode AND
      TDO.Longitude = TDI.Longitude AND
      TDO.Latitude = TDI.Latitude AND         
      TDO.Citycode = TDI.Citycode AND    
      TDO.Cityname = TDI.Cityname  
   SET ErrorStatus = 'Invalid Record -  Duplicate record',ErrorFlag = 1;    

	
	
	 Update TempHotelMaster set OrignalCityName=Cityname; 		
	 Update TempHotelMaster set OrignalCountryName=Countryname; 		
	
		update temphotelmaster inner join		 
		(
		select c.nvcrcountryshortcode , t.countryname  ,c.nvcrcountryname   
		from temphotelmaster t  
			inner join Mstcountry c 
				on countrycode=c.nvcrcountryshortcode
		where c.nvcrcountryname <> t.countryname
		group by  c.nvcrcountryshortcode ,t.countryname ,c.nvcrcountryname
		)a
        on temphotelmaster.countrycode=a.nvcrcountryshortcode
        set countryname = a.nvcrcountryname;
		
		
        Create temporary table Temp_Cities
        (nvcrcitycode nvarchar (50),
         nvcrcityname nvarchar(100),
         nvcrCountryShortCode nvarchar(1000)
         );
         
         insert into Temp_Cities
        select a.nvcrcitycode,a.nvcrcityname,b.nvcrCountryShortCode 
		from Cities a 
			inner join Mstcountry b
				on a.intcountryid=b.intcountryid;

		Update temphotelmaster 
		inner join 
		(
			select c.nvcrcitycode,c.nvcrcityname  ,c.nvcrCountryShortCode 
			from temphotelmaster t 
				inner join Temp_Cities c 
					on t.countrycode=c.nvcrCountryShortCode
						and t.citycode=c.nvcrcitycode
			where t.cityname <> c.nvcrcityname
			group by  c.nvcrcitycode,c.nvcrcityname  ,c.nvcrCountryShortCode
		)a
        set cityname = a.nvcrcityname
		where temphotelmaster.citycode=a.nvcrcitycode
		and temphotelmaster.countrycode=a.nvcrCountryShortCode;  
	
    
      -- Remain Function applied 
    -- ---------------------------- Replace Spanish char-----------------  
    
	   update temphotelmaster set Hotelname = ReplaceSpanishChars(Hotelname);  -- from temphotelmaster   
	   update temphotelmaster set Countryname = ReplaceSpanishChars(Countryname);  -- from temphotelmaster   
       update temphotelmaster set Cityname = ReplaceSpanishChars(Cityname);  -- from temphotelmaster   
	   update temphotelmaster set Hotelname = replace(Hotelname,'(!)',''); 
	   update temphotelmaster set Hotelname = replace(Hotelname,'(.)',''); 
	   update temphotelmaster set Countryname = replace(Countryname,'(!)',''); 
	   update temphotelmaster set Countryname = replace(Countryname,'(.)',''); 
	   update temphotelmaster set Cityname = replace(Cityname,'(!)',''); 
	   update temphotelmaster set Cityname = replace(Cityname,'(.)',''); 		
     
	  

	if NOT EXISTS( select * from temphotelmaster 
            where errorflag = 1  limit 1) Then 
		 
	
			
			truncate table  bkpMSTHotel; 
			truncate table  bkpMSTCity ;
			truncate table  bkpMSTCountry;
		 
			
			
			set v_intVersion =1;	

			
			 INSERT INTO bkpMSTCountry(  
			   intCountryId, nvcrCountryShortCode, nvcrCountryName,  
			   nvcrcitycode,bitCountryActive, intVersion)  
			 SELECT intCountryId, nvcrCountryShortCode, nvcrCountryName,  
			   nvcrcitycode, bitCountryActive, v_intVersion 
			FROM MSTCountry; 

			 INSERT INTO bkpMSTCity(  
			   intCityId, nvcrCityName, intCountryId,  
			   nvcrcitycode, intDipBagSyncId, bitCityActive, intVersion
			   )  
			 SELECT intCityId, nvcrCityName,  intCountryId,  
			   nvcrcitycode, intDipBagSyncId, bitCityActive, v_intVersion  
			FROM MSTCity;

			 INSERT INTO bkpMSTHotel(  
			   `intHotelId`,`nvcrWebSiteHotelId`,`nvcrHotelName`,`nvcrHotelAddress1`,`nvcrHotelAddress2`
				,`intCityId`,`nvcrHotelBrandName`,`nvcrHotelStar`,`nvcrHotelPostCode`,`intSupplierId`
				,`tintHotelMatchStatus`,`nvcrHotelDescription`,`intUsrId`,`bitisProceesed`
				,`sdtAddedDateTime`,`nvcrMatchHotelName`,`intDipBagSyncId`,`bitIsMailed`
				,`intDiPBagDynamicId`,`intVersion`,nvcrYieldManager,nvcrContractManager,nvcrDemandGroup)  
			 SELECT intHotelId, nvcrWebSiteHotelId, nvcrHotelName, nvcrHotelAddress1, nvcrHotelAddress2,  
			   intCityId, nvcrHotelBrandName, nvcrHotelStar, nvcrHotelPostCode, intSupplierId,  
			   tintHotelMatchStatus, nvcrHotelDescription, intUsrId, bitisProceesed,  
			   sdtAddedDateTime, nvcrMatchHotelName, intDipBagSyncId, bitIsMailed, 
				intDiPBagDynamicId, v_intVersion,nvcrYieldManager,nvcrContractManager,nvcrDemandGroup
			FROM MSTHotel;  

		   -- -------------------------Insert New country in HotelMonitor.MSTCountry table------------------  
			INSERT INTO MSTCountry(  
			   nvcrCountryShortCode, nvcrCountryName)  
			 select distinct tm.Countrycode,tm.CountryName  
			 from temphotelmaster tm
				left join MSTCountry hc 
					 on tm.Countrycode = hc.nvcrCountryShortCode  
						and tm.CountryName = hc.nvcrcountryName  
			 where hc.nvcrCountryShortCode is null  
			 and hc.nvcrcountryName is null  
			 and   tm.ErrorFlag = 0  ; 
		   -- --------------------End Insert New country in HotelMonitor.MSTCountry table----------------------  
		  
		   -- -----------------------start Update countryid of temphotelmaster table ------------------------------  
			 UPDATE temphotelmaster TD  
				INNER JOIN MSTCountry C 
					ON TD.Countrycode = C.nvcrCountryShortCode
						and TD.CountryName = c.nvcrCountryName
			SET Countryid = intCountryid 
            WHERE ErrorFlag = 0 ; 
		   -- -----------------------end Update countryid of temphotelmaster table ------------------------------   

			 
			
				Create Temporary table NewCity
				(
				`RecRowId` numeric(18, 0),
				`Citycode` nvarchar(100) NULL,
				`Cityname` nvarchar(100) NULL,
				`Countrycode` nvarchar(100) NULL
				); 
				insert into NewCity (RECRowID,cityname)
				select min(RECRowID) as RECRowID ,cityname  
				from temphotelmaster -- where citycode not in(select nvcrcitycode from hotelmonitor.Mstcity with(nolock) )
				group by  cityname;



	update NewCity 
				inner join
				(
				select t.RecRowId, t.Citycode,t.Countrycode
				from temphotelmaster t , NewCity n
				where t.RecRowId=n.RecRowId
				) a
                set Citycode = a.citycode , Countrycode=a.Countrycode
				where NewCity.RecRowId=a.RecRowId;




				update temphotelmaster 
				inner join 
				(
				select t.RecRowId from temphotelmaster t , NewCity n where
				t.cityname=n.cityname 
				and t.citycode<>n.citycode
				and t.countrycode<>n.countrycode
				) b
                set cityname = cityname + '_' + countrycode 
				where temphotelmaster.RecRowId=b.RecRowId;

				drop table NewCity;







    -- ----------------------------------End Code for new city change city name-----------------------------------------
		 -- --------------------------------------------------------------------------------------------------
			
             Create temporary table temp
             (citycode nvarchar(100),
             countryid nvarchar (100)
            );
             insert into temp
				select  citycode,countryid 
				from  TempHotelMaster 
				where citycode in( select distinct nvcrcitycode from Mstcity )
				group by citycode,countryid;
					
				-- drop table #temp2
                  Create temporary table temp2
             (citycode nvarchar(100),
             countryid nvarchar (100)
            );
                
                insert into temp2
				select t.*
				from temp t  ,Cities c 
				where t.citycode = c.nvcrcitycode
				and t.countryid = c.intcountryid;

			
				Update TempHotelMaster t 
				left join temp2 
						on t.citycode=temp2.citycode
							and t.countryid=temp2.countryid
				set cityname =  concat(cityname , '_' , countrycode)  
                where temp2.citycode is null
				and temp2.countryid is null
				and ErrorFlag = 0  
				and t.citycode in( select distinct nvcrcitycode from Mstcity );	
		 -- ---------------------------------Code for new city change city name--------------------------------------------

		   -- ---------------------Start insert new city in HotelMonitor.MSTCity table----------------------     
			INSERT INTO MSTCity(  
			   nvcrCityName, intCountryId,  nvcrcitycode)  
			select distinct tm.Cityname,tm.Countryid,tm.Citycode 
			from  temphotelmaster tm 
				left join Mstcity hc 
					on Countryid = hc.intCountryId   
						and tm.Citycode = hc.nvcrcitycode    
			 where 
			  hc.intCountryId is null  
			 and hc.nvcrcitycode is null  
			 and tm.ErrorFlag = 0 ;  	

  
		   -- ---------------------End insert new city in HotelMonitor.MSTCity table----------------------     
		     
		  -- -----------------------start Update cityid of temphotelmaster table -----------------------   
			 UPDATE temphotelmaster TD 
					INNER JOIN MSTCity C 
					ON TD.Citycode = C.nvcrcitycode  
						and TD.Countryid=c.intCountryId	
                        SET Cityid = intCityId  
			 WHERE ErrorFlag = 0;   
		  -- -----------------------end Update cityid of temphotelmaster table ------------------------------  
		    

			  -- -----------------------Added by Bhushan Gaud start Update Hotel Status temphotelmaster table ------------------------------  
			 UPDATE temphotelmaster TD 
			 INNER JOIN MstHotelStatus MHS 
					ON TD.NvcrHotelStatus = MHS.vcrStatus
                    SET IntHotelStatusID = MHS.intStatusID
			 WHERE ErrorFlag = 0;  
		   -- -----------------------Added by Bhushan Gaud end Update Hotel Status temphotelmaster table ------------------------------  




		  -- ---------------------Start insert new Hotel in HotelMonitor.MSTHotel table----------------------     
		  INSERT INTO MSTHotel(  
			   nvcrWebSiteHotelId,  
			   nvcrHotelName,  
			   nvcrHotelAddress1,  
			   intCityId,  
			   nvcrHotelStar,  
			   nvcrHotelPostCode, 
			   nvcrLongitude,
			   nvcrLatitude, 
			   intSupplierId,  
			   tintHotelMatchStatus,  
			   intUsrId,  
			   bitisProceesed,  
			   sdtAddedDateTime,  
			   bitIsMailed,
			   intStatusID,
			   nvcrYieldManager, -- Added by sandeep sharma
			   nvcrContractManager, -- Added by sandeep sharma
			   nvcrDemandGroup
			  )    -- Added by sandeep sharma
			 SELECT t.Websitehotelcode,  
			  fn_HotelNameReplaceSpecialChars(t.Hotelname),  
			   t.Address1,  
			   t.Cityid,  
			   t.Starrating,  
			   t.ZipCode, 
			   t.Longitude,
			   t.Latitude, 
			   p_intSupplierId as intSupplierId ,  
			   0 as tintHotelMatchStatus ,  
			   p_intUserId as intUsrId,  
			   0 as bitisProceesed ,  
			   now() as sdtAddedDateTime ,  
			   0 as bitIsMailed,
			   T.IntHotelStatusID,
			   t.nvcrYieldManager,
			   t.nvcrContractManager,
			   t.nvcrDemandGroup -- Added by Bhushan Gaud   
			 FROM temphotelmaster t
				left join msthotel h 
			 on  t.Websitehotelcode = h.nvcrWebSiteHotelId   
			 and t.Cityid = h.intCityId  
			 and intSupplierId=p_intSupplierId   
			 where h.nvcrWebSiteHotelId is null  
			 and h.intCityId is null  
			 and errorflag = 0 ;  
		       
		  -- ---   ------------------End insert new Hotel in HotelMonitor.MSTHotel table----------------------       
		  
		  -- ----------Start Update ids for Hotel-----------------------  
			 UPDATE temphotelmaster TD 
					INNER JOIN MSTHotel h 
					ON TD.Websitehotelcode = h.nvcrWebSiteHotelId  
						and td.cityid=h.intcityid	
						and h.intSupplierid=p_intSupplierId		
                        SET HotelID = intHotelId  
			 WHERE ErrorFlag = 0 ;  
		  -- ----------End Update ids for Hotel-----------------------  
		  
		  -- ---------------Start update HotelMonitor.msthotel all details--------   
			  UPDATE  msthotel H   
			INNER JOIN  temphotelmaster T 
					ON 
					t.Websitehotelcode = h.nvcrWebSiteHotelId   
					 and h.intSupplierId in(1,6,25)  
                     
                     SET nvcrHotelName = fn_HotelNameReplaceSpecialChars(Hotelname),  
			   nvcrHotelAddress1 =Address1 ,  
			   intCityId =Cityid,  
			   nvcrHotelStar = Starrating,  
			   nvcrHotelPostCode =ZipCode ,			           
			   intUsrId = p_intUserId ,
			   intStatusID = T.IntHotelStatusID, -- Added by Kiran.Kadam on 06-Feb-2016 - For HotelStatus Update.  
		        nvcrLongitude = case when ifnull(T.Longitude,'')='' then h.nvcrLongitude else T.Longitude end,-- T.Longitude,
			   nvcrLatitude = case when ifnull(T.Latitude,'')='' then h.nvcrLatitude else T.Latitude end,-- T.Latitude,
			   nvcrYieldManager=  case when ifnull(T.nvcrYieldManager,'')='' then h.nvcrYieldManager else T.nvcrYieldManager end,-- T.nvcrYieldManager,
			   nvcrContractManager=case when ifnull(T.nvcrContractManager,'')='' then h.nvcrContractManager else T.nvcrContractManager end,-- T.nvcrContractManager,
			   nvcrDemandGroup=case when ifnull(T.nvcrDemandGroup,'')='' then h.nvcrDemandGroup else T.nvcrDemandGroup end -- T.nvcrDemandGroup
			  WHERE errorflag = 0;  
		 
		 call usp_DipBagHM_CrawlManager_AddNewlyHotel_DummyForhotelopia_Upload (0);
		          
		  END if;                
    
    
    
    
     SELECT     
     Concat('"', replace(replace(Websitehotelcode,',',''),'"',''),'"') as Websitehotelcode,  
     Concat('"', replace(replace( Hotelname,',',''),'"',''),'"') as Hotelname,  
      Concat('"',replace(replace( Starrating,',',''),'"',''),'"') as Starrating,  
      Concat('"', replace(replace(Address1,',',''),'"',''),'"') as Address1,  
      Concat('"',replace(replace( Countrycode,',',''),'"',''),'"') as Countrycode,  
      Concat('"', replace(replace(OrignalCountryname,',',''),'"',''),'"') as Countryname,  
	  Concat('"',replace(replace( Countryname,',',''),'"',''),'"') as UpdatedCountryname, 		
      Concat('"',replace(replace( ZipCode,',',''),'"',''),'"') as ZipCode, 
      Concat('"',replace(replace( Longitude,',',''),'"',''),'"') as Longitude,
      Concat('"', replace(replace(Latitude,',',''),'"',''),'"') as Latitude, 
      Concat('"', replace(replace(Citycode,',',''),'"',''),'"') as Citycode,  
      Concat('"',replace(replace( OrignalCityName,',',''),'"','') ,'"') as CityName,
	  Concat('"', replace(replace(CityName,',',''),'"',''),'"') as UpdatedCityname,
	  Concat('"',replace(replace( nvcrHotelStatus,',',''),'"',''),'"') as HotelStatus,	
      Concat('"',replace(replace( ErrorStatus,',',''),'"',''),'"') as ErrorStatus  
   FROM temphotelmaster  WHERE ErrorFlag = 1   ; 
 
      Leave sp_lbl;    
     

        Set p_nvcrErrorMsg = ERROR_MESSAGE() ;   
	
         
       END;  
       */
  -- print @nvcrErrorMsg
  End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_ExcelUploadHotelMaster_TEST` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
