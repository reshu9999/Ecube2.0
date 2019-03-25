DELIMITER ;;

CREATE PROCEDURE `sp_HotelDateDetails`(
IN EntryMode int(11)
)
BEGIN
	DROP TEMPORARY TABLE IF EXISTS Temp_Request;
    DROP TEMPORARY TABLE IF EXISTS Temp_Request_Split;


	Create Temporary Table  Temp_Request
	(
		IntId Int unique key auto_increment,
		RequestId Int,
		RequestName varchar(500),
		MultipleDates varchar(4000),
        Nights varchar(100)
	);
    
    
    Create Temporary Table  Temp_Request_Split
	(
		IntId Int,
		RequestId Int,
		RequestName varchar(500),
		MultipleDates varchar(4000),
        Nights varchar(100),
		FromDate varchar(50),
		ToDate varchar(50)
	);
    
    If(EntryMode = 1) Then -- HotelMode
    
		Insert into Temp_Request (RequestId, RequestName, MultipleDates, Nights)
		Select Distinct HRI.HotelReqestInputDetailsId, RM.RequestName, HRI.RequestURL, HRI.RentalLength  from temp_Hotel T Inner Join tbl_RequestMaster RM
			On T.`Batch Name` = RM.RequestName Inner Join tbl_hotelrequestinputdetails HRI
			On RM.RequestId = HRI.RequestId
			Where HRI.BookingPeriodID = 3;
	End If;

    If(EntryMode = 2) Then -- Hotel+FlightMode
    
		Insert into Temp_Request (RequestId, RequestName, MultipleDates, Nights)
		Select Distinct HRI.hotelflightrequestinputdetailsId , RM.RequestName, HRI.RequestURL, HRI.RentalLength  from temp_Hotel T Inner Join tbl_RequestMaster RM
			On T.`Batch Name` = RM.RequestName Inner Join tbl_hotelflightrequestinputdetails HRI
			On RM.RequestId = HRI.RequestId
			Where HRI.BookingPeriodID = 3;
	End If;	
	
    
    Select max(IntId) into @MaxId From Temp_Request;
    Select 1 Into @Counter;
   
       
    While(@MaxId > 0) Do
		
        Select MultipleDates into @MultipleDates
				From Temp_Request Where IntID = @MaxId;
		Select Nights into @MultipleNights
				From Temp_Request Where IntID = @MaxId;
        
        SELECT 
			(ROUND (   
				(
					LENGTH(@MultipleDates)
					- LENGTH( REPLACE (@MultipleDates, ";", "") ) 
				) / LENGTH(";")        
			)  + 1) AS count into @Counter_Max;
		
        
        
        
        
        While(@Counter < @Counter_Max) Do
        	
            
            
            Set @MultipleDates = SPLIT_STR(@MultipleDates,';',@Counter);
            
            Select Cast(FromDate As Date) Into @FromDate  From 
            (
				Select 
					CONCAT(SPLIT_STR(FromDate,'-',3),'-',SPLIT_STR(FromDate,'-',2),'-',SPLIT_STR(FromDate,'-',1)) FromDate,
					CONCAT(SPLIT_STR(ToDate,'-',3),'-',SPLIT_STR(ToDate,'-',2),'-',SPLIT_STR(ToDate,'-',1)) ToDate
				From (
						Select Ltrim(Rtrim(SPLIT_STR(@MultipleDates,'to',1))) FromDate, 
							Ltrim(Rtrim(SPLIT_STR(@MultipleDates,'to',2))) ToDate 
					 )A
             ) B; 
             
             Select Cast(ToDate As Date) into @ToDate From 
            (
				Select 
					CONCAT(SPLIT_STR(FromDate,'-',3),'-',SPLIT_STR(FromDate,'-',2),'-',SPLIT_STR(FromDate,'-',1)) FromDate,
					CONCAT(SPLIT_STR(ToDate,'-',3),'-',SPLIT_STR(ToDate,'-',2),'-',SPLIT_STR(ToDate,'-',1)) ToDate
				From (
						Select Ltrim(Rtrim(SPLIT_STR(@MultipleDates,'to',1))) FromDate, 
							Ltrim(Rtrim(SPLIT_STR(@MultipleDates,'to',2))) ToDate 
					 )A
             ) B;
				
			
            
            
           /*
            Insert into Temp_Request_Split (IntId, RequestId, RequestName, MultipleDates, Nights, FromDate, ToDate)
				Select IntId, RequestId, RequestName, MultipleDates, Nights, 
					CONCAT(SPLIT_STR(FromDate,'-',3),'-',SPLIT_STR(FromDate,'-',2),'-',SPLIT_STR(FromDate,'-',1)) FromDate,
					CONCAT(SPLIT_STR(ToDate,'-',3),'-',SPLIT_STR(ToDate,'-',2),'-',SPLIT_STR(ToDate,'-',1)) ToDate
				From (
				Select IntId, RequestId, RequestName, MultipleDates, Nights, 
					Ltrim(Rtrim(SPLIT_STR(@MultipleDates,'to',1))) FromDate, 
					Ltrim(Rtrim(SPLIT_STR(@MultipleDates,'to',2))) ToDate 
					From Temp_Request Where IntID = @MaxId) A;
			*/
			           
            
			While @FromDate <= @ToDate Do
             	
				 Select 1 Into @CounterNights;
                 
                 SELECT 
					(ROUND (   
						(
							LENGTH(@MultipleNights)
							- LENGTH( REPLACE (@MultipleNights, ",", "") ) 
						) / LENGTH(",")        
					)  + 1) AS count into @CounterNights_Max;
                 
                 While(@CounterNights <= @CounterNights_Max) Do
                 
					Set @MultipleNights = SPLIT_STR(@MultipleNights,';',@CounterNights);
                    
					Insert into Temp_Request_Split (IntId, RequestId, RequestName, MultipleDates, Nights, FromDate, ToDate)
					Select IntId, RequestId, RequestName, MultipleDates, Nights, 
						FromDate, Date_Add(@FromDate , interval  @MultipleNights Day) ToDate
					From (
					Select IntId, RequestId, RequestName, MultipleDates, Nights, 
						@FromDate FromDate, @ToDate ToDate 
						From Temp_Request Where IntID = @MaxId) A;
					
                    Set @CounterNights = @CounterNights + 1;
                 End While;
                             
                
                Set @FromDate = Date_Add(@FromDate , interval  1 Day);
                
            End While;
            
            
            
            
			
            Set @Counter = @Counter + 1;
			
        End While;
        
        Set @Counter = 1;
        Set @MAXID = @MAXID - 1;
        
        
    End While;


    If(EntryMode = 1) Then -- HotelMode
    
		Insert into tbl_HotelRequestsDateDetails (HotelRequestInputDetailsId, CheckInDate
			, CheckOutDate, CreatedDatetime)
		Select Distinct R.RequestId, R.FromDate, R.ToDate, now() CreatedDatetime From Temp_Request_Split R;
		 
	End If;

    If(EntryMode = 2) Then -- Hotel+FlightMode
    
		Insert into tbl_hotelflightRequestsDateDetail (hotelflightrequestinputdetailsId, CheckInDate
			, CheckOutDate, CreatedDatetime)
		 Select Distinct R.RequestId, R.FromDate, R.ToDate , now() CreatedDatetime From Temp_Request_Split R;
	End If;	



Select * From Temp_Request_Split;

END ;;
