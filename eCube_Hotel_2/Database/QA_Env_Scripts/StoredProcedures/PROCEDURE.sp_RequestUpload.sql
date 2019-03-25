DELIMITER ;;

CREATE PROCEDURE `sp_RequestUpload`(
IN KeyValue Varchar(100)
)
BEGIN

INSERT INTO `eCube_Centralized_DB`.`tbl_RequestMaster`
(`RequestName`, `RequestDescription`,`RequestFile`,`CategoryCount`,
`ProductCount`,`MPN_SKUCount`,`FK_StatusId`,`FK_GroupId`,`CreatedBy`,
`CreatedDatetime`,`UpdatedBy`,`UpdatedDatetime`,`NextScheduleDateTime`,
`FK_ScheduleTypeId`,`RequestModeId`,`IsPNFStopper`)

 Select D.batchname RequestName, D.batchname RequestDescription, 
 null RequestFile, null CategoryCount, null ProductCount, null MPN_SKUCount, 
 null FK_StatusId, null FK_GroupId,  1 CreatedBy, now() CreatedDatetime, 
 Null UpdatedBy, null UpdatedDatetime, Null NextScheduleDateTime, 
 null FK_ScheduleTypeId, Null RequestModeId, Null IsPNFStopper
 From temp_daily D Left Join tbl_RequestMaster RM
	On D.BatchName = RM.RequestName
    Where RM.RequestID is Null;
    
INSERT INTO `eCube_Centralized_DB`.`tbl_RequestMaster`
(`RequestName`, `RequestDescription`,`RequestFile`,`CategoryCount`,
`ProductCount`,`MPN_SKUCount`,`FK_StatusId`,`FK_GroupId`,`CreatedBy`,
`CreatedDatetime`,`UpdatedBy`,`UpdatedDatetime`,`NextScheduleDateTime`,
`FK_ScheduleTypeId`,`RequestModeId`,`IsPNFStopper`)

 Select D.batchname RequestName, D.batchname RequestDescription, 
 null RequestFile, null CategoryCount, null ProductCount, null MPN_SKUCount, 
 null FK_StatusId, null FK_GroupId,  1 CreatedBy, now() CreatedDatetime, 
 Null UpdatedBy, null UpdatedDatetime, Null NextScheduleDateTime, 
 null FK_ScheduleTypeId, Null RequestModeId, Null IsPNFStopper
 From temp_weekly D Left Join tbl_RequestMaster RM
	On D.BatchName = RM.RequestName
    Where RM.RequestID is Null;
    
INSERT INTO `eCube_Centralized_DB`.`tbl_RequestMaster`
(`RequestName`, `RequestDescription`,`RequestFile`,`CategoryCount`,
`ProductCount`,`MPN_SKUCount`,`FK_StatusId`,`FK_GroupId`,`CreatedBy`,
`CreatedDatetime`,`UpdatedBy`,`UpdatedDatetime`,`NextScheduleDateTime`,
`FK_ScheduleTypeId`,`RequestModeId`,`IsPNFStopper`)

 Select D.batchname RequestName, D.batchname RequestDescription, 
 null RequestFile, null CategoryCount, null ProductCount, null MPN_SKUCount, 
 null FK_StatusId, null FK_GroupId,  1 CreatedBy, now() CreatedDatetime, 
 Null UpdatedBy, null UpdatedDatetime, Null NextScheduleDateTime, 
 null FK_ScheduleTypeId, Null RequestModeId, Null IsPNFStopper
 From temp_monthly D Left Join tbl_RequestMaster RM
	On D.BatchName = RM.RequestName
    Where RM.RequestID is Null;

INSERT INTO `eCube_Centralized_DB`.`tbl_RequestMaster`
(`RequestName`, `RequestDescription`,`RequestFile`,`CategoryCount`,
`ProductCount`,`MPN_SKUCount`,`FK_StatusId`,`FK_GroupId`,`CreatedBy`,
`CreatedDatetime`,`UpdatedBy`,`UpdatedDatetime`,`NextScheduleDateTime`,
`FK_ScheduleTypeId`,`RequestModeId`,`IsPNFStopper`)

 Select D.batchname RequestName, D.batchname RequestDescription, 
 null RequestFile, null CategoryCount, null ProductCount, null MPN_SKUCount, 
 null FK_StatusId, null FK_GroupId,  1 CreatedBy, now() CreatedDatetime, 
 Null UpdatedBy, null UpdatedDatetime, Null NextScheduleDateTime, 
 null FK_ScheduleTypeId, Null RequestModeId, Null IsPNFStopper
 From temp_hotel_input D Left Join tbl_RequestMaster RM
	On D.BatchName = RM.RequestName
    Where RM.RequestID is Null;
    
INSERT INTO `eCube_Centralized_DB`.`tbl_RequestMaster`
(`RequestName`, `RequestDescription`,`RequestFile`,`CategoryCount`,
`ProductCount`,`MPN_SKUCount`,`FK_StatusId`,`FK_GroupId`,`CreatedBy`,
`CreatedDatetime`,`UpdatedBy`,`UpdatedDatetime`,`NextScheduleDateTime`,
`FK_ScheduleTypeId`,`RequestModeId`,`IsPNFStopper`)

 Select D.batchname RequestName, D.batchname RequestDescription, 
 null RequestFile, null CategoryCount, null ProductCount, null MPN_SKUCount, 
 null FK_StatusId, null FK_GroupId,  1 CreatedBy, now() CreatedDatetime, 
 Null UpdatedBy, null UpdatedDatetime, Null NextScheduleDateTime, 
 null FK_ScheduleTypeId, Null RequestModeId, Null IsPNFStopper
 From temp_hotel_flight_input D Left Join tbl_RequestMaster RM
	On D.BatchName = RM.RequestName
    Where RM.RequestID is Null;

 

INSERT INTO `eCube_Centralized_DB`.`tbl_ScheduleMaster`(
`StartDate`,
`EndDate`,
`TriggerDayDate`,
`Time`,
`Active`,
`SM_ScheduleTypeId`,
`SM_RequestId`,
`CreatedDate`,
`ModifiedDate`,
`Split`)
Select D.startdate, D.enddate, null TriggerDayDate, Cast(Concat(D.HH , ':' , D.MM) As Time)  `Time`,
	1 Active, 1 SM_ScheduleTypeId, RM.requestID SM_RequestId,
    now() CreatedDate, null ModifiedDate, 1 Split 
 From temp_daily D Inner Join tbl_RequestMaster RM
	On D.BatchName = RM.RequestName; 



INSERT INTO `eCube_Centralized_DB`.`tbl_ScheduleMaster`(
`StartDate`,
`EndDate`,
`TriggerDayDate`,
`Time`,
`Active`,
`SM_ScheduleTypeId`,
`SM_RequestId`,
`CreatedDate`,
`ModifiedDate`,
`Split`)
Select D.startdate, D.enddate, 
Concat(
Case When D.monday = '1' Then 'Mon,' else '' End,  
Case When D.tuesday = '1' Then 'Tue,'  else '' End, 
Case When D.wednesday = '1' Then 'Wed,'  else '' End, 
Case When D.thursday = '1' Then 'Thu,'  else '' End, 
Case When D.friday = '1' Then 'Fri,'  else '' End, 
Case When D.saturday = '1' Then 'Sat,'  else '' End, 
Case When D.sunday = '1' Then 'Sun,'  else '' End)
	  TriggerDayDate, 

Cast(Concat(D.HH , ':' , D.MM) As Time)  `Time`,
	1 Active, 3 SM_ScheduleTypeId, RM.requestID SM_RequestId,
    now() CreatedDate, null ModifiedDate, 1 Split 
 From temp_weekly D Inner Join tbl_RequestMaster RM
	On D.BatchName = RM.RequestName; 

INSERT INTO `eCube_Centralized_DB`.`tbl_ScheduleMaster`(
`StartDate`,
`EndDate`,
`TriggerDayDate`,
`Time`,
`Active`,
`SM_ScheduleTypeId`,
`SM_RequestId`,
`CreatedDate`,
`ModifiedDate`,
`Split`)
Select D.startdate, D.enddate, D.day TriggerDayDate, 
Cast(Concat(D.HH , ':' , D.MM) As Time)  `Time`,
	1 Active, 2 SM_ScheduleTypeId, RM.requestID SM_RequestId,
    now() CreatedDate, null ModifiedDate, 1 Split 
 From temp_monthly D Inner Join tbl_RequestMaster RM
	On D.BatchName = RM.RequestName;


INSERT INTO `eCube_Centralized_DB`.`tbl_hotelrequestinputdetails`
( 
`RequestId`,`RequestURL`,`RequestTypeId`,`FromDate`,`ToDate`,`BookingPeriodID`,
`DaysOfWeek`,`PointOfSaleId`,`RentalLength`,`AdvanceDates`,`AdultId`,`ChildID`,
`CrawlMode`,`HotelId`,`CityId`,`CountryId`,`StarRating`,`BoardType`,`RoomType`,
`HotelGroupId`,`CompetitorIds`,`CreatedDatetime`,`AdvanceWeeks`)


Select RM.RequestId, null RequestURL, null RequestTypeId,
	TH.`start date(date range)` FromDate, TH.`end date(date range)` ToDate,
	Case When TH.`days of weeks` != '' Then 1 
		 When TH.`advance days` != '' Then 2
         When TH.`multiple check-in dates` Then 3
         When TH.`advance weeks` Then 4 End BookingPeriodID,
	TH.`days of weeks` DaysOfWeek, POS.PointOfSaleId, TH.los RentalLength,  
    TH.`advance days` AdvanceDates, Replace(substring_index(TH.pax,'adts',1),' ','') AdultId,	
    Replace(Replace(substring_index(TH.pax,'+',1),' ',''),'Chd','') ChildID,
    Case When ifnull(TH.`hotel name` ,'') = '' Then 1 else 2 End CrawlMode,
    Null HotelId, C.CityID CityId, CM.CountryID CountryId,
    TH.`star rating` StarRating, TH.`board type` BoardType, TH.`room type` RoomType,
    HG.HotelGroupId HotelGroupId, Null CompetitorIds,
    now() CreatedDatetime, TH.`advance weeks`  AdvanceWeeks
    
From temp_hotel_input TH inner join tbl_RequestMaster RM
	On TH.batchname = RM.requestname Inner Join HotelPOS POS
    On TH.`source market` = POS.PointOfSale Inner Join tbl_CountryMaster CM
    On TH.country = CM.countryname Inner Join Cities C
    On TH.destination = C.Cityname and TH.`Destination code` = C.CityCode
    Left Join HotelGroups HG On HG.HotelGroup = TH.`city/beach group`;

INSERT INTO `eCube_Centralized_DB`.`tbl_hotelflightrequestinputdetails`
(`RequestId`,`RequestURL`,`RequestTypeId`,`CreatedDatetime`,
`UpdatedDatetime`,`FromDate`,`ToDate`,`BookingPeriodId`,`DaysOfWeek`,`PointOfSaleId`,
`RentalLength`,`AdvanceDates`,`AdultId`,
`ChildID`,`CrawlMode`,`HotelId`,`StarRating`,`BoardType`,`RoomType`,
`CompetitorIds`,`FlightSearchTypeID`,`AdvanceWeeks`,
`FromAirportCodeId`,`ToAirportCodeId`)


Select RM.RequestId, null RequestURL, null RequestTypeId,
now() CreatedDatetime, null UpdatedDatetime,
	TH.`start date(date range)` FromDate, TH.`end date(date range)` ToDate,
	Case When TH.`days of weeks` != '' Then 1 
		 When TH.`advance days` != '' Then 2
         When TH.`multiple check-in dates` Then 3
         When TH.`advance weeks` Then 4 End BookingPeriodID,
	TH.`days of weeks` DaysOfWeek, POS.PointOfSaleId, TH.los RentalLength,  
    TH.`advance days` AdvanceDates, Replace(substring_index(TH.pax,'adts',1),' ','') AdultId,	
    Replace(Replace(substring_index(TH.pax,'+',1),' ',''),'Chd','') ChildID,
    Case When ifnull(TH.`hotel name` ,'') = '' Then 1 else 2 End CrawlMode,
    Null HotelId, TH.`star rating` StarRating, TH.`board type` BoardType, TH.`room type` RoomType,
    Null CompetitorIds, null FlightSearchTypeID, TH.`advance weeks`  AdvanceWeeks,
    null FromAirportCodeId, null ToAirportCodeId
    
From temp_hotel_input TH inner join tbl_RequestMaster RM
	On TH.batchname = RM.requestname Inner Join HotelPOS POS
    On TH.`source market` = POS.PointOfSale Inner Join tbl_CountryMaster CM
    On TH.country = CM.countryname Inner Join Cities C
    On TH.destination = C.Cityname and TH.`Destination code` = C.CityCode
    Left Join HotelGroups HG On HG.HotelGroup = TH.`city/beach group`;

/*
Drop Table temp_daily;
Drop Table temp_monthly;
Drop Table temp_weekly;
Drop Table temp_hotel_input;
Drop Table temp_hotel_flight_input;



INSERT INTO `eCube_Centralized_DB`.`tbl_hotelrequestinputdetails`
( 
`RequestId`,`RequestURL`,`RequestTypeId`,`FromDate`,`ToDate`,`BookingPeriodID`,
`DaysOfWeek`,`PointOfSaleId`,`RentalLength`,`AdvanceDates`,`AdultId`,`ChildID`,
`CrawlMode`,`HotelId`,`CityId`,`CountryId`,`StarRating`,`BoardType`,`RoomType`,
`HotelGroupId`,`CompetitorIds`,`CreatedDatetime`,`AdvanceWeeks`)

Select RM.RequestId, null RequestURL, null RequestTypeId,
	TH.`start date(date range)` FromDate, TH.`end date(date range)` ToDate,
	Case When TH.`days of weeks` != '' Then 1 
		 When TH.`advance days` != '' Then 2
         When TH.`multiple check-in dates` Then 3
         When TH.`advance weeks` Then 4 End BookingPeriodID,
	TH.`days of weeks` DaysOfWeek, POS.PointOfSaleId, TH.los RentalLength,  
    AdvanceDates
    
From temp_hotel_input TH inner join tbl_RequestMaster RM
	On TH.batchname = RM.requestname Inner Join HotelPOS POS
    On TH.`source market` = POS.PointOfSale
*/


END ;;
