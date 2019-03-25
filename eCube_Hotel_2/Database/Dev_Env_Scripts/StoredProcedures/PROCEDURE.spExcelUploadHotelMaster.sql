DELIMITER ;;

CREATE PROCEDURE `spExcelUploadHotelMaster`(
 p_intSupplierId int,  
  p_intUserId Int  --   ,out p_nvcrErrorMsg  nvarchar(200)  
 
 )
BEGIN        
   declare v_intVersion int;
   -- declare p_intSupplierId  int;
   -- declare  p_intUserId Int ;
   
   -- declare p_nvcrErrorMsg nvarchar(200)  ;
	Declare minCompetitorId, maxCompetitorId int default 0;
    
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
	BEGIN
		-- set p_nvcrErrorMsg = 'Error in procedure spExcelUploadHotelMaster5';
        GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE,@errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
		-- SET p_nvcrErrorMsg = CONCAT("ERROR :", @errno, " (", @sqlstate, "): ", @text);
	End;

-- set p_intSupplierId=1;
   -- set p_intUserId=1 ;
   
      Truncate table TempHotelMaster;
       
      INSERT INTO `eCube_Centralized_DB`.`TempHotelMaster`
		(
		`Websitehotelcode`,
		`Hotelname`,
		`Starrating`,
		`Address1`,
		`Countrycode`,
		`Countryname`,
		`ZipCode`,
		`Longitude`,
		`Latitude`,
		`Citycode`,
		`Cityname`,
		`nvcrHotelStatus`,
		`nvcrYieldManager`,
		`nvcrContractManager`,
		`nvcrDemandGroup` 
		)
	SELECT 
		`temphotelmaster_excel`.`Website hotel code`,
		`temphotelmaster_excel`.`Hotelname`,
		`temphotelmaster_excel`.`Star rating`,
		`temphotelmaster_excel`.`Address1`,
		`temphotelmaster_excel`.`Country code`,
		`temphotelmaster_excel`.`Country name`,
		`temphotelmaster_excel`.`Zip Code`,
		`temphotelmaster_excel`.`Longitude`,
		`temphotelmaster_excel`.`Latitude`,
		`temphotelmaster_excel`.`City code`,
		`temphotelmaster_excel`.`City name`,
		`temphotelmaster_excel`.`Hotel Status`,
		`temphotelmaster_excel`.`Yield Manager`,
		`temphotelmaster_excel`.`Contract Manager`,
		`temphotelmaster_excel`.`Demand Group`
	FROM `eCube_Centralized_DB`.`temphotelmaster_excel`;
      
	SET SQL_SAFE_UPDATES = 0;
	UPDATE TempHotelMaster Set ErrorStatus = ifnull(ErrorStatus, ''), ErrorFlag = ifnull(ErrorFlag,0);
    
	IF exists(select Hotelname from TempHotelMaster 
	-- where CHAR_LENGTH(RTRIM( LTRIM(rtrim(Hotelname))))>0) = 0)
	where LENGTH(RTRIM( LTRIM(rtrim(ifnull(Hotelname,''))))) = 0 limit 1)
	THEN
		UPDATE TempHotelMaster 
        Set ErrorStatus = 'Invalid Record - Hotel Name column having blank value',ErrorFlag = 1
        where LENGTH(RTRIM( LTRIM(rtrim(ifnull(Hotelname,''))))) = 0;  
	END IF;  
	 
	
    
	IF exists(select Starrating from TempHotelMaster 
	-- where CHAR_LENGTH(RTRIM( LTRIM(rtrim(Starrating))))>0)= 0)
		where LENGTH(RTRIM( LTRIM(rtrim(ifnull(Starrating,''))))) = 0 limit 1)
	THEN
		   UPDATE TempHotelMaster 
           Set ErrorStatus = case when ErrorStatus != '' then concat( ErrorStatus,';Invalid Record - Star Rating column having blank value') 
								else 'Invalid Record - Star Rating column having blank value' end
							,ErrorFlag = 1
           where LENGTH(RTRIM( LTRIM(rtrim(ifnull(Starrating,''))))) = 0;    
	END IF;  
	  
	IF exists(select Address1 from TempHotelMaster 
		-- where CHAR_LENGTH(RTRIM( LTRIM(rtrim(Address1))))>0) = 0)
        where LENGTH(RTRIM( LTRIM(rtrim(ifnull(Address1,''))))) = 0 limit 1)
	THEN
	   UPDATE TempHotelMaster 
       Set ErrorStatus = case when ErrorStatus != '' then concat( ErrorStatus,';Invalid Record - Address1 column having blank value') 
								else 'Invalid Record - Address1 column having blank value' end
							,ErrorFlag = 1
	   where LENGTH(RTRIM( LTRIM(rtrim(ifnull(Address1,''))))) = 0;  
	END IF;  
	 

	IF exists(select Countrycode from TempHotelMaster 
		-- where CHAR_LENGTH(RTRIM( LTRIM(rtrim(Countrycode))))>0)= 0)
        where LENGTH(RTRIM( LTRIM(rtrim(ifnull(Countrycode,''))))) = 0 limit 1)
	THEN
		UPDATE TempHotelMaster 
		Set ErrorStatus = case when ErrorStatus != '' then concat( ErrorStatus,';Invalid Record - Country Code column having blank value') 
						else 'Invalid Record - Country Code column having blank value' end
					,ErrorFlag = 1
		where LENGTH(RTRIM( LTRIM(rtrim(ifnull(Countrycode,''))))) = 0;  
	 END IF;  

	IF exists(select Countryname from TempHotelMaster 
		-- where CHAR_LENGTH(RTRIM( LTRIM(rtrim(Countryname))))>0) = 0)
        where LENGTH(RTRIM( LTRIM(rtrim(ifnull(Countryname,''))))) = 0 limit 1)
	THEN
	   UPDATE TempHotelMaster 
	  Set ErrorStatus = case when ErrorStatus != '' then concat( ErrorStatus,';Invalid Record - Country Name column having blank value') 
						else 'Invalid Record - Country Name column having blank value' end
					,ErrorFlag = 1
       where LENGTH(RTRIM( LTRIM(rtrim(ifnull(Countryname,''))))) = 0;  
	 END IF;  

	IF exists(select ZipCode from TempHotelMaster 
		-- where CHAR_LENGTH(RTRIM( LTRIM(rtrim(ZipCode))))>0) = 0)
        where LENGTH(RTRIM( LTRIM(rtrim(ifnull(ZipCode,''))))) = 0 limit 1)
	 THEN
	   UPDATE TempHotelMaster 
	 Set ErrorStatus = case when ErrorStatus != '' then concat( ErrorStatus,';Invalid Record - Zip Code column having blank value') 
				else 'Invalid Record - Zip Code column having blank value' end
			,ErrorFlag = 1
       where LENGTH(RTRIM( LTRIM(rtrim(ifnull(ZipCode,''))))) = 0;  
	 END IF;  
	 
	 IF exists(select Citycode from TempHotelMaster -- where CHAR_LENGTH(RTRIM( LTRIM(rtrim(Citycode))))>0) = 0)
		where LENGTH(RTRIM( LTRIM(rtrim(ifnull(Citycode,''))))) = 0 limit 1)
	 THEN
	   UPDATE TempHotelMaster 
	 Set ErrorStatus = case when ErrorStatus != '' then concat( ErrorStatus,';Invalid Record - City Code column having blank value') 
				else 'Invalid Record - City Code column having blank value' end
			,ErrorFlag = 1
       where LENGTH(RTRIM( LTRIM(rtrim(ifnull(Citycode,''))))) = 0;  
	 END IF; 

	IF exists(select Cityname from TempHotelMaster -- where CHAR_LENGTH(RTRIM( LTRIM(rtrim(Cityname))))>0) = 0)
		where LENGTH(RTRIM( LTRIM(rtrim(ifnull(Cityname,''))))) = 0 limit 1)
	 THEN
	   UPDATE TempHotelMaster 
	  Set ErrorStatus = case when ErrorStatus != '' then concat( ErrorStatus,';Invalid Record - City Name column having blank value') 
						else 'Invalid Record - City Name column having blank value' end
					,ErrorFlag = 1       
       where LENGTH(RTRIM( LTRIM(rtrim(ifnull(Cityname,''))))) = 0;  
	 END IF; 
	 

	IF exists(select nvcrHotelStatus from TempHotelMaster -- where CHAR_LENGTH(RTRIM( LTRIM(rtrim(nvcrHotelStatus))))>0) = 0)
		where LENGTH(RTRIM( LTRIM(rtrim(ifnull(nvcrHotelStatus,''))))) = 0 limit 1)
	 THEN
	   UPDATE TempHotelMaster 
	  Set ErrorStatus = case when ErrorStatus != '' then concat( ErrorStatus,';Invalid Record - Hotel status column having blank value') 
						else 'Invalid Record - Hotel status column having blank value' end
					,ErrorFlag = 1       
       where LENGTH(RTRIM( LTRIM(rtrim(ifnull(nvcrHotelStatus,''))))) = 0;  
	 END IF;  
  
	UPDATE TempHotelMaster Set ErrorStatus = 'Invalid Record - Website Hotel Code Should not have blank record ',ErrorFlag = 1    
	-- FROM TempHotelMaster TD    
	WHERE IFNULL(WebSiteHotelCode,'')= ''  AND ErrorFlag = 0;     
       
          
	UPDATE TempHotelMaster TDO
      inner join
      (    
      SELECT  WebSiteHotelCode
      FROM TempHotelMaster TDI 
      GROUP BY WebSiteHotelCode
      HAVING Count(WebSiteHotelCode) > 1
         
     ) TDI ON   TDO.Websitehotelcode = TDI.WebSiteHotelCode AND ErrorFlag = 0  
    SET ErrorStatus = 'Invalid Record - Website Hotel Code Should not have duplicate record', ErrorFlag =1 ;  
         
        
       
	UPDATE TempHotelMaster Set ErrorStatus = 'Invalid Record - Website Hotel Code Should have numeric value ',ErrorFlag = 1     
	WHERE fn_IsNumeric(WebSiteHotelCode)=0 AND ErrorFlag = 0;   
      
      
	UPDATE TempHotelMaster 
	SET ErrorStatus = 'Invalid Record - Same Websitehotel duplicate in same city ',ErrorFlag = 1  
	 WHERE Websitehotelcode IN
	(
	SELECT A.Websitehotelcode from   
		 ( 
	 SELECT t1.Websitehotelcode,t1.Citycode from TempHotelMaster t1  
	 Where t1.errorflag = 0  
	 group by t1.Websitehotelcode,t1.Citycode  
	 having count(Websitehotelcode)> 1
	)A
	 )
	and errorflag = 0; 
    
      
	    
      -- Remain funcition craetion 
	UPDATE TempHotelMaster Set ErrorStatus = 'Invalid Record - Invalid Hotel Name',ErrorFlag = 1    
	WHERE  ErrorFlag = 0    and  CHAR_LENGTH(RTRIM(Hotelname))<>CHAR_LENGTH(RTRIM(udf_StripHTML(Hotelname)));
     
	UPDATE TempHotelMaster Set ErrorStatus = 'Invalid Record - Hotel Name Should not have blank record ',ErrorFlag = 1    
	WHERE IFNULL(Hotelname,'') = '' AND  ErrorFlag = 0;       
      
      
      
	UPDATE TempHotelMaster set starrating=RemoveCharctersForHotelStar(starrating); 
	UPDATE TempHotelMaster set starrating = replace(starrating,'_','.'); 
	UPDATE TempHotelMaster set starrating = 0 where starrating = '' or starrating is null;

	UPDATE TempHotelMaster Set ErrorStatus = 'Invalid Record - Star rating must be numeric ',ErrorFlag = 1    
	WHERE fn_IsNumeric(Starrating)=0 AND ErrorFlag = 0;     




	UPDATE TempHotelMaster Set ErrorStatus = 'Invalid Record - Country Code Should  have only 2 digit',ErrorFlag = 1    
	WHERE char_length(rtrim(Countrycode)) > 2 AND ErrorFlag = 0;    

	UPDATE TempHotelMaster Set ErrorStatus = 'Invalid Record - Country Code Should not have blank',ErrorFlag = 1    
	-- FROM TempHotelMaster TD    
	WHERE IFNULL(Countrycode,'') = '' AND ErrorFlag = 0;   

	-- Added Start by Mahesh 20160722
		   UPDATE TempHotelMaster Set ErrorStatus = 'Invalid Record - Longitude Should accept only numeric , dot(.) and dash(-).',ErrorFlag = 1    
	-- FROM TempHotelMaster TD    
	-- WHERE ISNUMERIC(ISNULL(Longitude,'') = '') AND ErrorFlag = 0   
	WHERE fn_IsNumeric(ifnull(Longitude,''))=0 AND ErrorFlag = 0 
	-- Added by Bhushan Gaud for master list update Start
		And ifnull(Longitude,'') != ''; 
	-- Added by Bhushan Gaud for master list update End
        
	UPDATE TempHotelMaster Set ErrorStatus = 'Invalid Record - Latitude Should accept only numeric , dot(.) and dash(-).',ErrorFlag = 1    
	-- FROM TempHotelMaster TD    
	-- WHERE ISNULL(Latitude,'') = '' AND ErrorFlag = 0   
	WHERE fn_IsNumeric(ifnull(Latitude,''))=0 AND ErrorFlag = 0 
	-- End by Mahesh 20160722
	-- Added by Bhushan Gaud for master list update Start
	And ifnull(Latitude,'') != ''; 
            
     UPDATE TempHotelMaster  SET ErrorStatus = 'Invalid Record - Same Country Code mapped with different countries name',ErrorFlag = 1  
     WHERE CountryCode IN(  
     SELECT A.CountryCode from   
     (  
      SELECT t1.CountryCode,t1.Countryname from TempHotelMaster t1 
      Where t1.errorflag = 0  
      group by t1.CountryCode,t1.Countryname  
     ) A  
     Where errorflag = 0      
     Group By A.CountryCode  
     Having Count(A.Countryname) > 1);
     
	UPDATE TempHotelMaster t 
   	INNER JOIN tbl_CountryMaster c 
	ON t.Countrycode = c.CountryCode  
    SET ErrorStatus = 'Invalid Record - Same Country Code mapped with different country in master table',ErrorFlag = 1  
    WHERE t.Countryname <> c.CountryName AND errorflag = 0;  

  
     UPDATE TempHotelMaster Set ErrorStatus = 'Invalid Record - Invalid Country Name missing',ErrorFlag = 1    
     WHERE IFNULL(Countryname,'') = '' AND ErrorFlag = 0;    
     
	UPDATE TempHotelMaster  SET ErrorStatus = 'Invalid Record - Same Country Name mapped with different country code in master table',ErrorFlag = 1    
	WHERE CountryName IN(  
	SELECT A.Countryname from   
	(  
	SELECT t1.CountryCode,t1.Countryname from TempHotelMaster t1 
	Where t1.errorflag = 0  
	group by t1.CountryCode,t1.Countryname  
	) A  
	Where errorflag = 0   
	Group By A.Countryname  
	Having Count(A.Countryname) > 1);    
        
	UPDATE TempHotelMaster Set ErrorStatus = 'Invalid Record - Hotel Status Should not have blank',ErrorFlag = 1    
	WHERE IFNULL(nvcrHotelStatus,'') = '' AND ErrorFlag = 0;  

	UPDATE TempHotelMaster Set nvcrHotelStatus='Inactive' where UPPER(ltrim(rtrim(nvcrHotelStatus)))='NOT ACTIVE';

    UPDATE TempHotelMaster Set ErrorStatus = 'Invalid Record - Invalid City Code missing',ErrorFlag = 1    
    WHERE IFNULL(Citycode,'') = '' AND ErrorFlag = 0;  
  
     UPDATE TempHotelMaster Set ErrorStatus = 'Invalid Record - Invalid City Name missing',ErrorFlag = 1    
     WHERE IFNULL(Cityname,'') = '' AND ErrorFlag = 0;  
     
     UPDATE TempHotelMaster SET ErrorStatus = 'Invalid Record - Same city Name mapped with different city code in master table',ErrorFlag = 1  
     WHERE CityName IN(  
     SELECT A.CityName from   
     (  
      SELECT t1.CityCode,t1.CityName,t1.Countrycode from TempHotelMaster t1 
      Where t1.errorflag = 0  
      group by t1.CityCode,t1.CityName,t1.Countrycode  
     ) A  
     Where errorflag = 0   
     Group By A.CityName , A.countrycode   
     Having Count(A.CityName) > 1) ; 
  
  

    
     
     UPDATE TempHotelMaster Set ErrorStatus = 'Invalid Record - Hotel Status does not exist in Master Database',ErrorFlag = 1    
     WHERE IFNULL(nvcrHotelStatus,'')  Not in (Select HotelStatus From HotelStatus) AND ErrorFlag = 0;  
-- added by Bhavin.Dhimmar
UPDATE TempHotelMaster Set ErrorStatus = 'Invalid Record - Star Rating does not exist in Master Database',ErrorFlag = 1    
WHERE IFNULL(Starrating,'')  Not in (Select Starrating From StarRatings) AND ErrorFlag = 0;  
        
     
     UPDATE TempHotelMaster TDO 
	INNER JOIN    
     (    
      SELECT  Websitehotelcode,Hotelname,Starrating,Address1,Countrycode,Countryname,ZipCode,Longitude,Latitude,Citycode,Cityname  
      FROM TempHotelMaster TDI 
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
	
		update TempHotelMaster inner join		 
		(
		select c.CountryCode , t.Countryname tCountryname  ,c.CountryName cCountryName   -- Bhavin.Dhimmar; 01-Jun-2018; Given alias
		from TempHotelMaster t  
			inner join tbl_CountryMaster c 
				on t.Countrycode=c.CountryCode 
		where c.CountryName <> t.Countryname
		group by  c.CountryCode ,t.Countryname ,c.CountryName
		)a
        on TempHotelMaster.Countrycode=a.CountryCode
        set Countryname = a.cCountryName;   -- Bhavin.Dhimmar; 01-Jun-2018; set Countryname equals to cCountryName
    
       	
        Drop temporary table if exists Temp_Cities;-- Bhavin.Dhimmar; 01-Jun-2018; Add the query
        
        Create temporary table Temp_Cities
        (nvcrcitycode nvarchar (50),
         nvcrcityname nvarchar(100),
         CountryCode nvarchar(1000)
         );
         
        insert into Temp_Cities
        select a.citycode,a.cityname ,b.CountryCode 
		from Cities a inner join tbl_CountryMaster b
			on a.countryid=b.countryid;

		Update TempHotelMaster 
		inner join 
		(
			select c.nvcrcitycode,c.nvcrcityname  ,c.CountryCode 
			from TempHotelMaster t 
				inner join Temp_Cities c 
					on t.Countrycode=c.CountryCode
						and t.citycode=c.nvcrcitycode
			where t.cityname <> c.nvcrcityname
			group by  c.nvcrcitycode,c.nvcrcityname  ,c.CountryCode
		)a
        set cityname = a.nvcrcityname
		where TempHotelMaster.citycode= a.nvcrcitycode
		and TempHotelMaster.Countrycode=a.CountryCode;  
    
    
       update TempHotelMaster set Hotelname = ReplaceSpanishChars(Hotelname);  -- from TempHotelMaster   
	   update TempHotelMaster set Countryname = ReplaceSpanishChars(Countryname);  -- from TempHotelMaster   
       update TempHotelMaster set Cityname = ReplaceSpanishChars(Cityname);  -- from TempHotelMaster   
	   update TempHotelMaster set Hotelname = replace(Hotelname,'(!)',''); 
	   update TempHotelMaster set Hotelname = replace(Hotelname,'(.)',''); 
	   update TempHotelMaster set Countryname = replace(Countryname,'(!)',''); 
	   update TempHotelMaster set Countryname = replace(Countryname,'(.)',''); 
	   update TempHotelMaster set Cityname = replace(Cityname,'(!)',''); 
	   update TempHotelMaster set Cityname = replace(Cityname,'(.)',''); 		
    
	  	if NOT EXISTS( select RecRowId from TempHotelMaster where errorflag = 1  limit 1) Then 
		 
		
			truncate table  bkpMSTHotel; 
			truncate table  bkpMSTCity ;
			truncate table  bkpMSTCountry;
		    set v_intVersion =1;	

			
			 INSERT INTO bkpMSTCountry(  
			   intCountryId, nvcrCountryShortCode, nvcrCountryName, bitCountryActive, intVersion)  
            SELECT CountryId, CountryCode, CountryName, Active as CountryActive , v_intVersion 
			FROM tbl_CountryMaster; 
			
            INSERT INTO bkpMSTCity(  
			   intCityId, nvcrCityName, intCountryId, nvcrcitycode, bitCityActive, intVersion
			   )  
            SELECT CityId, CityName,  CountryId, citycode, Active as bitCityActive , v_intVersion  
			FROM Cities;
            
			select min(CompetitorId), max(CompetitorId) into minCompetitorId, maxCompetitorId 
			from Hotels ;

			while maxCompetitorId >= minCompetitorId do
				INSERT INTO bkpMSTHotel(  
				   `intHotelId`,`nvcrWebSiteHotelId`,`nvcrHotelName`,`nvcrHotelAddress1`,`nvcrHotelAddress2`
					,`intCityId`,`nvcrHotelBrandName`,`nvcrHotelStar`,`nvcrHotelPostCode`,`intSupplierId`
					,`tintHotelMatchStatus`,`nvcrHotelDescription`,`intUsrId`,`bitisProceesed`
					,`sdtAddedDateTime`,`nvcrMatchHotelName`,`intDipBagSyncId`,`bitIsMailed`
					,`intDiPBagDynamicId`,`intVersion`,nvcrYieldManager,nvcrContractManager,nvcrDemandGroup)  
				SELECT HotelId, WebSiteHotelId, HotelName, HotelAddress1, HotelAddress2,  
				   CityId, HotelBrandName, StarRatingId nvcrHotelStar, HotelPostCode, CompetitorId as intSupplierId,  
				   HotelMatchStatus as tintHotelMatchStatus, HotelDescription, CreatedBy as intUsrId, isProceesed,  
				   CreatedDate as sdtAddedDateTime, MatchHotelName, DipBagSyncId, IsMailed, 
				   ifnull(RequestId,0) as intDiPBagDynamicId, v_intVersion, YieldManager, ContractManager, DemandGroup
				FROM Hotels where CompetitorId= minCompetitorId;  		
				
                set minCompetitorId = minCompetitorId + 1;
			end while;
			
            INSERT INTO tbl_CountryMaster -- ( nvcrCountryShortCode, nvcrCountryName)  
            (CountryCode, CountryName)
			select distinct tm.Countrycode,tm.CountryName  
			from TempHotelMaster tm
			left join tbl_CountryMaster hc 
				 on tm.Countrycode = hc.CountryCode
					and tm.CountryName = hc.CountryName
			where hc.CountryCode is null  
			and hc.CountryName is null  
			and   tm.ErrorFlag = 0  ; 
             
		   -- --------------------End Insert New country in HotelMonitor.MSTCountry table----------------------  
		  
		   -- -----------------------start Update countryid of TempHotelMaster table ------------------------------  
			UPDATE TempHotelMaster TD  
				INNER JOIN tbl_CountryMaster C 
					ON TD.Countrycode = C.CountryCode
						and TD.CountryName = C.CountryName
			SET TD.Countryid = C.Countryid 
			WHERE TD.ErrorFlag = 0 ; 
		   -- -----------------------end Update countryid of TempHotelMaster table ------------------------------   

			 
				Drop  Temporary table if exists NewCity;
				Create Temporary table NewCity
				(
				`RecRowId` numeric(18, 0),
				`Citycode` nvarchar(100) NULL,
				`Cityname` nvarchar(100) NULL,
				`Countrycode` nvarchar(100) NULL
				); 
				insert into NewCity (RECRowID,cityname)
				select min(RECRowID) as RECRowID ,cityname  
				from TempHotelMaster -- where citycode not in(select nvcrcitycode from hotelmonitor.Mstcity with(nolock) )
				group by  cityname;

				Drop temporary table if exists NewCity_copy;-- Bhavin.Dhimmar; 01-Jun-2018; Add the query
				CREATE TEMPORARY TABLE NewCity_copy LIKE NewCity;
				insert into NewCity_copy (RECRowID,cityname)
				select RECRowID,cityname from NewCity;
                
				update NewCity 
				inner join
				(
				select t.RecRowId, t.Citycode,t.Countrycode
				from TempHotelMaster t , NewCity_copy n
				where t.RecRowId=n.RecRowId
				) a
                set NewCity.Citycode = a.citycode , NewCity.Countrycode=a.Countrycode
				where NewCity.RecRowId=a.RecRowId;

				Drop temporary table if exists NewCity_copy;-- Bhavin.Dhimmar; 01-Jun-2018; Add the query

		
				update TempHotelMaster 
				inner join 
				(
				select t.RecRowId from TempHotelMaster t , NewCity n where
				t.cityname=n.cityname 
				and t.citycode<>n.citycode
				and t.Countrycode<>n.countrycode
				) b
                set cityname = cityname + '_' + countrycode 
				where TempHotelMaster.RecRowId=b.RecRowId;

				Drop temporary table if exists NewCity;
            
			Drop temporary table if exists temp;
             Create temporary table temp
             (citycode nvarchar(100),
             countryid nvarchar (100)
            );
             insert into temp
			select  citycode,countryid 
			from  TempHotelMaster 
			where citycode in( select distinct citycode from Cities )
			group by citycode,countryid;
					
				-- drop table #temp2
			Drop temporary table if exists temp2;
			Create temporary table temp2
             (citycode nvarchar(100),
             countryid nvarchar (100)
            );
                
			insert into temp2
			select t.*
			from temp t  ,Cities c 
			where t.citycode = c.citycode
			and t.countryid = c.countryid;

			
			Update TempHotelMaster t 
			left join temp2 
			on t.citycode=temp2.citycode
			and t.countryid=temp2.countryid
			set cityname =  concat(cityname , '_' , countrycode)  
			where temp2.citycode is null
			and temp2.countryid is null
			and ErrorFlag = 0  
            and t.citycode in( select distinct citycode from Cities );	
	
		 -- ---------------------------------Code for new city change city name--------------------------------------------

		   -- ---------------------Start insert new city in HotelMonitor.MSTCity table----------------------     
			INSERT INTO Cities(  
			   CityName, CountryId,  citycode,CreatedBy)  
			select distinct tm.Cityname,tm.Countryid,tm.Citycode, p_intUserId
			from  TempHotelMaster tm 
				left join Cities hc 
					on tm.Countryid = hc.CountryId   
						and tm.Citycode = hc.citycode    
			 where 
			  hc.CountryId is null  
			 and hc.citycode is null  
			 and tm.ErrorFlag = 0 ;  
  

  
		   -- ---------------------End insert new city in HotelMonitor.MSTCity table----------------------     
		     
		  -- -----------------------start Update cityid of TempHotelMaster table -----------------------   
			 UPDATE TempHotelMaster TD 
					INNER JOIN Cities C 
					ON TD.Citycode = C.citycode  
						and TD.Countryid=C.CountryId	
                        SET TD.Cityid = C.CityId  
			 WHERE ErrorFlag = 0;   
		  -- -----------------------end Update cityid of TempHotelMaster table ------------------------------  
            UPDATE TempHotelMaster TD 
			 INNER JOIN HotelStatus MHS 
					ON TD.nvcrHotelStatus = MHS.HotelStatus
                    SET IntHotelStatusID = MHS.HotelStatusId
			 WHERE ErrorFlag = 0;  
		   -- -----------------------Added by Bhushan Gaud end Update Hotel Status TempHotelMaster table ------------------------------  




		  -- ---------------------Start insert new Hotel in HotelMonitor.MSTHotel table----------------------     
		  INSERT INTO Hotels(  
			   WebSiteHotelId,  
			   HotelName,  
			   HotelAddress1,  
			   CityId,  
			   StarRatingId, -- nvcrHotelStar,  
			   HotelPostCode, 
			   Longitude,
			   Latitude, 
			   CompetitorId, -- intSupplierId,  
			   HotelMatchStatus,  
			   CreatedBy, -- intUsrId,  
			   isProceesed,  
			   CreatedDate, -- sdtAddedDateTime,  
			   IsMailed,
			   HotelStatusId, -- intStatusID,
			   YieldManager, -- Added by sandeep sharma
			   ContractManager, -- Added by sandeep sharma
			   DemandGroup
			  )    -- Added by sandeep sharma
			 SELECT t.Websitehotelcode,  
			   fn_HotelNameReplaceSpecialChars(t.Hotelname),  
			   t.Address1,  
			   t.Cityid,  
			   -- ecube1.0 t.Starrating,  
               star.StarRatingId,  
			   t.ZipCode, 
			   t.Longitude,
			   t.Latitude, 
			   p_intSupplierId as intSupplierId ,  
			   0 as tintHotelMatchStatus ,  
			   p_intUserId as intUsrId,  
               0 as bitisProceesed ,  
			   now() as sdtAddedDateTime ,  
			   0 as bitIsMailed,
			   t.IntHotelStatusID as IntnvcrHotelStatusID,
			   t.nvcrYieldManager,
			   t.nvcrContractManager,
			   t.nvcrDemandGroup -- Added by Bhushan Gaud   
			 FROM TempHotelMaster t
				left join Hotels h 
					 on  t.Websitehotelcode = h.WebSiteHotelId   
					 and t.Cityid = h.CityId  
					 and h.CompetitorId=p_intSupplierId   
				left join StarRatings star
					on star.StarRating = t.Starrating
			 where h.WebSiteHotelId is null  
			 and h.CityId is null  
			 and errorflag = 0 ;  
	
		  -- ---   ------------------End insert new Hotel in HotelMonitor.MSTHotel table----------------------       
		  
		  -- ----------Start Update ids for Hotel-----------------------  
 			 UPDATE TempHotelMaster TD 
					INNER JOIN Hotels h 
					ON TD.Websitehotelcode = h.WebSiteHotelId  
						and TD.Cityid=h.CityId	
						and h.CompetitorId=p_intSupplierId		
                        SET TD.HotelID = h.HotelId  
			 WHERE ErrorFlag = 0 ;  
		  -- ----------End Update ids for Hotel-----------------------  
		  
		  -- ---------------Start update HotelMonitor.msthotel all details--------   
			UPDATE  Hotels H   
			INNER JOIN  TempHotelMaster T 
				ON 
				T.Websitehotelcode = H.WebSiteHotelId   
				 and H.CompetitorId in(1,6,25)  
			left join StarRatings star
					on star.StarRating = T.Starrating
			   SET H.HotelName = fn_HotelNameReplaceSpecialChars(T.Hotelname),  
			   H.HotelAddress1 =Address1 ,  
			   H.CityId = T.Cityid,  
			   H.StarRatingId = star.StarRatingId,  
			   H.HotelPostCode =ZipCode ,			           
			   H.CreatedBy = p_intUserId ,
			   H.HotelStatusId = T.IntHotelStatusID, -- Added by Kiran.Kadam on 06-Feb-2016 - For nvcrHotelStatus Update.  
			   H.Longitude = case when ifnull(T.Longitude,'')='' then H.Longitude else T.Longitude end,-- T.Longitude,
			   H.Latitude = case when ifnull(T.Latitude,'')='' then H.Latitude else T.Latitude end,-- T.Latitude,
			   H.YieldManager=  case when ifnull(T.nvcrYieldManager,'')='' then H.YieldManager else T.nvcrYieldManager end,-- T.nvcrYieldManager,
			   H.ContractManager=case when ifnull(T.nvcrContractManager,'')='' then H.ContractManager else T.nvcrContractManager end,-- T.nvcrContractManager,
			   H.DemandGroup=case when ifnull(T.nvcrDemandGroup,'')='' then H.DemandGroup else T.nvcrDemandGroup end -- T.nvcrDemandGroup
			WHERE errorflag = 0;  
		
		  call usp_DipBagHM_CrawlManager_AddNewlyHotel_DummyForhotelopia_Upload (0);
            
	end if;


    
    
   /*  SELECT     
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
	  Concat('"',replace(replace( nvcrHotelStatus,',',''),'"',''),'"') as nvcrHotelStatus,	
      Concat('"',replace(replace( ErrorStatus,',',''),'"',''),'"') as ErrorStatus  
   FROM TempHotelMaster  WHERE ErrorFlag = 1   ; 
 */
	SELECT     
     replace(replace(Websitehotelcode,',',''),'"','') as Websitehotelcode,  
     replace(replace( Hotelname,',',''),'"','') as Hotelname,  
      replace(replace( Starrating,',',''),'"','') as Starrating,  
      replace(replace(Address1,',',''),'"','') as Address1,  
      replace(replace( Countrycode,',',''),'"','') as Countrycode,  
      replace(replace(OrignalCountryname,',',''),'"','') as Countryname,  
	  replace(replace( Countryname,',',''),'"','') as UpdatedCountryname, 		
      replace(replace( ZipCode,',',''),'"','') as ZipCode, 
      replace(replace( Longitude,',',''),'"','') as Longitude,
      replace(replace(Latitude,',',''),'"','') as Latitude, 
      replace(replace(Citycode,',',''),'"','') as Citycode,  
      replace(replace( OrignalCityName,',',''),'"','')  as CityName,
	  replace(replace(CityName,',',''),'"','') as UpdatedCityname,
	  replace(replace( nvcrHotelStatus,',',''),'"','') as nvcrHotelStatus,	
      replace(replace( ErrorStatus,',',''),'"','') as ErrorStatus  
   FROM TempHotelMaster  WHERE ErrorFlag = 1   ;       -- Leave sp_lbl;    
     

        -- Set p_nvcrErrorMsg = ERROR_MESSAGE() ;   
	
         
       


    
END ;;
