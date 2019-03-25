DELIMITER ;;

CREATE PROCEDURE `sp_UploadAdhocLeadTimeTemplate`( 
 p_intUserId nvarchar(50))
Begin  
  declare v_bitStatus tinyint;  
  declare v_nvcrErrorMsg longtext;  
  declare v_intDataCount int;  
  declare v_smdtGetdate datetime;  
  declare v_nonbitActiveStatus varchar(100);  
  declare v_bitErrorStatus int;  
 
  set v_smdtGetdate = NOW();  
  set v_bitErrorStatus = 0;  

	Truncate Table tempAdhocLeadTime;
    -- Delete from  tempAdhocLeadTime;
    
	Insert into tempAdhocLeadTime (
	nvcrBookingDate,
	nvcrBatchName,
	nvcrDestination,
	nvcrLeadTime,
	nvcrEventType,
	nvcrNights,
	NvcrAccountName,
	NvcrPrimarySupplier,
	ErrorStatus,
	ErrorFlag
	) 
	SELECT  `Booking date`,`Batch Name`,`Destination`,`Lead time Value`,
	`Event Type Value`,`Nights`,`Account Name`,`Primary`,'' As ErrorStatus, 0 As ErrorFlag 
	FROM  tempLeadtimeAdhoc_Excel;

	update tempAdhocLeadTime   
		set ErrorStatus = '',ErrorFlag = 0;    
 

	update tempAdhocLeadTime   
		set ErrorStatus = 'Row contains empty string; ',ErrorFlag = 1      
	where nvcrBookingDate IN ('',NULL) or nvcrDestination IN ('',NULL) or nvcrLeadTime IN ('',NULL);  

	update tempAdhocLeadTime   
		set ErrorStatus =CONCAT(ErrorStatus , ' Invalid Booking Date;'),ErrorFlag = 1      
	where DATEDIFF(nvcrBookingDate, "1900-01-01") IS NULL;   
     
	update tempAdhocLeadTime   
		set ErrorStatus =CONCAT(ErrorStatus , 'Invalid batch; '),ErrorFlag = 1     
	where nvcrBatchName not in (select RequestName from tbl_RequestMaster);    
  
	update tempAdhocLeadTime   
	set ErrorStatus =CONCAT(ErrorStatus , 'Invalid destination; '),ErrorFlag = 1      
	where nvcrDestination not in (select CityCode from Cities); 
  

    
	Set @MaxIntID = 0;
	Set @MinIntID = 1;
	Select Max(IntID) into @MaxIntID From tempAdhocLeadTime;
    
	While @MinIntID <= @MaxIntID Do

		Select nvcrLeadTime into @nvcrLeadTime From tempAdhocLeadTime Where IntId = @MinIntID;
		Call sp_split(@nvcrLeadTime,'/');

-- select * from tempAdhocLeadTime Full join SplitValue i;

		Update tempAdhocLeadTime Full join SplitValue i
		Set ErrorStatus =CONCAT(ErrorStatus , 'Invalid Lead Time; '),ErrorFlag = 1 
		Where IntId = @MinIntID And 
			( i.items = '' 
		-- or (i.items not like '%(+%[0-9]%)%' and i.Items not like '%(%-%)%' ) 
		-- or (i.items like '%(%-%)%' and char_length(rtrim(SUBSTRING(Ltrim(Rtrim(items)),Position('-' in Ltrim(Rtrim(items)))+1,char_length(rtrim(Ltrim(Rtrim(items))))-((Position('-' in Ltrim(Rtrim(items)))+1) ) ) ))!=8);  
		or  ( !( (i.items  REGEXP '(.\\()*\\(\\+[0-9]+\)$')  or  (i.items REGEXP '(.\\()*[0-9]{8}-[0-9]{8}\)$') ))
		or 	(  (i.items REGEXP '(.\\()*[0-9]{8}-[0-9]{8}\)$') 
				 and char_length(rtrim(SUBSTRING(Ltrim(Rtrim(items)),Position('-' in Ltrim(Rtrim(items)))+1,char_length(rtrim(Ltrim(Rtrim(items))))-((Position('-' in Ltrim(Rtrim(items)))+1) ) ) ))!=8
			)
		);
		Set @MinIntID = @MinIntID + 1;
	End While;

	
    Set @MaxIntID = 0;
	Set @MinIntID = 1;
	Select Max(IntID) into @MaxIntID From tempAdhocLeadTime;
    
	While @MinIntID <= @MaxIntID Do

		Select nvcrEventType into @nvcrEventType From tempAdhocLeadTime Where IntId = @MinIntID;
		Call sp_split(@nvcrEventType,'/');

		Update tempAdhocLeadTime Full join SplitValue i
		Set ErrorStatus =CONCAT(ErrorStatus , 'Invalid Event Time; '),ErrorFlag = 1 
		where i.items <> 'Free' AND i.Items <> 'Fixed' AND i.Items <> '' 
			And  IntId = @MinIntID;

		Set @MinIntID = @MinIntID + 1;
	End While;

	update   tempAdhocLeadTime    
		set ErrorStatus =CONCAT(ErrorStatus , 'Invalid Nights; '),ErrorFlag = 1      
	Where concat('',nvcrNights * 1) != nvcrNights;  

	Drop temporary table if exists tmpDuplicateLeadTime;
	Create Temporary Table tmpDuplicateLeadTime (nvcrBatchName varchar(500) , nvcrDestination varchar(500)); 
 
	Insert into tmpDuplicateLeadTime (nvcrBatchName, nvcrDestination)
		Select nvcrBatchName, nvcrDestination   
		From tempAdhocLeadTime 
		group by nvcrBatchName, nvcrDestination
		having COUNT(*) > 1;

   
	update tempAdhocLeadTime t  inner join tmpDuplicateLeadTime tmp  
		on (t.nvcrBatchName=tmp.nvcrBatchName)  and t.nvcrDestination=tmp.nvcrDestination
	set ErrorStatus = CONCAT(ErrorStatus , 'Duplicate Destination found ; '),ErrorFlag = 1;      
       


	-- IF not exists(select nvcrBookingDate from tempAdhocLeadTime where ErrorFlag=1 limit 1) Then  
    IF exists(select nvcrBookingDate from tempAdhocLeadTime where ErrorFlag=1 limit 1) Then  
		select nvcrBookingDate as BookingDate,nvcrBatchName as BatchName,nvcrDestination as Destination,nvcrLeadTime as LeadTime,ErrorStatus 
        from tempAdhocLeadTime 
        WHERE ErrorFlag = 1;    
	/* Else  
		select nvcrBookingDate as BookingDate,nvcrBatchName as BatchName,nvcrDestination as Destination,nvcrLeadTime as LeadTime,ErrorStatus 
        from tempAdhocLeadTime;    
	*/
	END IF;

 
    drop table tmpDuplicateLeadTime;  
  

	IF not exists(select nvcrBookingDate from tempAdhocLeadTime where ErrorFlag=1 Limit 1) Then 
 -- select 'a';
		select COUNT(1) into v_intDataCount from tempAdhocLeadTime; 
        
        IF v_intDataCount > 0 THEN  
-- select 'b';
			delete from MstAdhocLeadTimeTemplateHistory where timestampdiff(day,smdAddToHistoryDate,now())>30;
			  
  
			Insert into MstAdhocLeadTimeTemplateHistory  
			( nvcrBookingDate,nvcrBatchName,nvcrDestination,nvcrLeadTime,smdtUpdatedDate,
		      intUpdatedUser,smdAddToHistoryDate,intLTime,nvcrType,
              smdtCheckindate,nvcrEventType,intNights,
              NvcrAccountName,NvcrPrimarySupplier) 
            
			SELECT  
				nvcrBookingDate,nvcrBatchName,nvcrDestination,nvcrLeadTime,
				smdtUpdatedDate,intUpdatedUser,	now(),intLTime,nvcrType,
				smdtCheckindate,nvcrEventType,intNights,NvcrAccountName,
				NvcrPrimarySupplier
			FROM MstAdhocLeadTimeTemplate; 
	   
			-- truncate table MstAdhocLeadTimeTemplate;  
			Delete from MstAdhocLeadTimeTemplate;  
      
     
			Set @MaxIntID = 0;
			Set @MinIntID = 1;
			Select Max(IntID) into @MaxIntID From tempAdhocLeadTime;

			While @MinIntID <= @MaxIntID Do
-- select  @MinIntID , @MaxIntID ;
				Select nvcrEventType into @nvcrEventType From tempAdhocLeadTime Where IntId = @MinIntID;
				Call sp_split(@nvcrEventType,'/');

				Update tempAdhocLeadTime Full join SplitValue i
				Set ErrorStatus =CONCAT(ErrorStatus , 'Invalid Event Type; '),ErrorFlag = 1 
				where i.items <> 'Free' AND i.Items <> 'Fixed' AND i.Items <> '';

 				Select nvcrLeadTime into @nvcrLeadTime From tempAdhocLeadTime Where IntId = @MinIntID;
				Call sp_split(@nvcrLeadTime,'/');
-- select * 			From tempAdhocLeadTime Full join SplitValue i;

                
                
				insert into MstAdhocLeadTimeTemplate
                (nvcrBookingDate,nvcrBatchName,nvcrDestination, nvcrLeadTime,intLTime,smdtUpdatedDate,intUpdatedUser,nvcrType,smdtCheckindate,intNights
				,NvcrAccountName, NvcrPrimarySupplier)   
				select temp.nvcrBookingDate,temp.nvcrBatchName,temp.nvcrDestination,temp.items
                ,case when temp.ltime > 0 then temp.ltime else 0 end as ltime,now()
				,p_intUserId,temp.nvcrType
				,case when temp.nvcrType='Free' then Concat(substring(temp.smdtltime,1,2),'-',SUBSTRING(temp.smdtltime,3,2),'-',SUBSTRING(temp.smdtltime,5,4)) else '1900-01-01 00:00:00' end  smdtltime,      
				case when temp.nvcrType='Free' THEN DATEDIFF(Concat(substring(temp.smdtltime,5,4),'-',SUBSTRING(temp.smdtltime,3,2),'-',SUBSTRING(temp.smdtltime,1,2)) ,
				Concat(substring(temp.smdtChekout,5,4),'-',SUBSTRING(temp.smdtChekout,3,2),'-',SUBSTRING(temp.smdtChekout,1,2)) ) 
				ELSE temp.intNights END as intNights
				,NvcrAccountName, NvcrPrimarySupplier   From 
				(
					Select 
					nvcrBookingDate,
					nvcrBatchName,
					nvcrDestination,
                    (case when i.items like "%+%" then substring(i.items,1,Position("(" in i.items)-1) 
						  else substring(i.items,1,Position("(" in i.items) - 1) end) as items,
					case when i.items like "%+%" then SUBSTRING(items,Position("+" in items) + 1,length(items)-((Position("+" in items)+1) ) )else "" end as ltime,
					SUBSTRING(items,1,Position("(" in items) - 1) as timedescription,  
					case when i.items like "%+%" then "" else substring(i.items,Position("(" in i.items)+1,length(i.items)-(Position("-" in i.items)+1)) end as smdtltime,
					case when i.items like "%+%" then "Fixed" else "Free" end as nvcrType 
					,case when concat("",nvcrNights * 1) = nvcrNights THEN nvcrNights else 0 END as intNights
					,case when i.items like "%+%" then "" else substring(i.items,Position("-" in i.items)+1,length(i.items)-(Position("-" in i.items)+1)) end as smdtChekout 
					 ,NvcrAccountName, NvcrPrimarySupplier
				From tempAdhocLeadTime Full join SplitValue i
				Where IntId = @MinIntID
				  And errorFlag=0 and i.items != '' and  (i.items like "%+%" or i.items like "%-%" ) 
				) temp;

				Set @MinIntID = @MinIntID + 1;
			End While;
      
       
			Drop Temporary Table If Exists Temp_MstAdhocLeadTimeTemplate;
			Create Temporary Table Temp_MstAdhocLeadTimeTemplate
			(Rank int, intMstLeadTime int, nvcrBatchName Varchar(4000), nvcrEventType Varchar(4000));

			Set @rn1 = 1;
			Set @nvcrBatchName = '';
			Set @intMstLeadTime = 0;

			Insert into Temp_MstAdhocLeadTimeTemplate (Rank,intMstLeadTime, nvcrBatchName, nvcrEventType)
			Select Rank,intMstLeadTime, nvcrBatchName, nvcrEventType  From 
			(
				Select 
				@rn1 := 
				if(@nvcrBatchName = A.nvcrBatchName, 
				If(@intMstLeadTime = A.intMstLeadTime,@rn1,@rn1 +1)
				,  1) As Rank,  

				@nvcrBatchName := A.nvcrBatchName,
				@intMstLeadTime := A.intMstLeadTime
				intMstLeadTime, nvcrBatchName, nvcrEventType
				From (
					SELECT  intMstAdhocLeadTime intMstLeadTime, nvcrEventType, nvcrBatchName
					FROM MstAdhocLeadTimeTemplate
					ORDER BY  intMstAdhocLeadTime   
				) A
			) B;
            
            
		Update MstAdhocLeadTimeTemplate M inner join Temp_MstAdhocLeadTimeTemplate T
			on M.intMstAdhocLeadTime = T.intMstLeadTime
			Set M.nvcrEventType = SPLIT_STR(T.nvcrEventType,'/',Rank);

		Update MstAdhocLeadTimeTemplate LT INNER JOIN MstEventTypeTemplate ET 
			on LT.nvcrLeadTime=ET.nvcrLeadTime 
			SET LT.nvcrEventType=ET.nvcrEventType  where IFNULL(LT.nvcrEventType,'') ='';

		UPDATE MstAdhocLeadTimeTemplate SET nvcrEventType='Free' where IFNULL(nvcrEventType,'') ='';
           
        TRUNCATE TABLE AdhocLeadTimeLatest; 
      
       INSERT INTO  AdhocLeadTimeLatest 
		SELECT `nvcrBookingDate`
		  ,`nvcrBatchName`
		  ,`nvcrDestination`
		  ,`nvcrLeadTime`
		  ,`nvcrEventType`
		  ,`nvcrNights`
		  ,NvcrAccountName, NvcrPrimarySupplier -- Added by Bhushan Gaud For RTM and SM
		FROM tempAdhocLeadTime;
      
		 
		set v_bitStatus = 1;  

		End IF;
    
	End IF;
        
End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_UploadLeadTimeTemplate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
