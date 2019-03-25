DELIMITER ;;

CREATE PROCEDURE `sp_DetailsSection`( 
p_intdipbagdynamicid int)
BEGIN

	DECLARE NOT_FOUND INT DEFAULT 0;
	declare v_nvcrDemandGroup longtext;
    Declare v_BIntLastResultID Int Default 0; 
    Declare v_RowCnt int Default 1;
	
    Declare v_StrSupplierName Longtext Default '';



	Drop Temporary Table If Exists Temp_DS;
	Create TEMPORARY table Temp_DS
	(
	`ID` Int Primary Key Auto_increment,  
	`dtmCrawlDateTime` nvarchar(100),
	 Hotel nvarchar(500),
	 HotelID nvarchar(100),
	 HotelCode nvarchar(100),
	 `Contract Manager` nvarchar(500),
	 `Yield Manager` nvarchar(500),
	 `Demand Group` nvarchar(500),
	 Segmentation nvarchar(500),
	 `Chain Name` nvarchar(500),
	 Status nvarchar(500),
	 `Hotel Contracting Type` nvarchar(500),
	 TPS nvarchar(500),
	 Dates nvarchar(100),
	 `Lead Time` nvarchar(100),
	 PointOfSale nvarchar(500),
	 Currency nvarchar(100),

	 Roomtype nvarchar(500),
	 Board nvarchar(500),
	 ContractName nvarchar(500),
	 RoomAvailability nvarchar(500),

	 Company nvarchar(500),
	 Price nvarchar(100),

	 BedsonlineRoomType nvarchar(500),
	 BedsonlineBoardType nvarchar(500),
	 BedsonlinePageUrl longtext,

	 CompetitorRoomType nvarchar(500),
	 CompetitorBoardType nvarchar(500),
	 CompetitorPageUrl longtext,

	  Destination nvarchar(500),
	 `Destination Code` nvarchar(500),
	 IntMsthotelID Int

	);


	Drop Temporary Table If Exists temp_ListPrice;
    Create Temporary Table temp_ListPrice
    As
	SELECT Distinct Hotel,HotelCode, date_format(Dates,'%m/%d/%Y') Dates,company,MIN(CAST(price AS DECIMAL(14,2)) ) price 
		FROM LastResultSummuryReport 
		WHERE intDiPBagDynamicId=p_intdipbagdynamicid
		GROUP BY Hotel,HotelCode,Dates,company;


	Insert into Temp_DS (
		`dtmCrawlDateTime`,Hotel,HotelID,HotelCode,`Contract Manager`, `Yield Manager`, `Demand Group`,Segmentation,`Chain Name`,Status,`Hotel Contracting Type`,TPS,
		Dates,`Lead Time`,PointOfSale,Company,Currency,Price,ContractName,RoomAvailability,
		BedsonlineRoomType,BedsonlineBoardType,BedsonlinePageUrl,CompetitorRoomType,
        CompetitorBoardType,CompetitorPageUrl,Destination,`Destination Code`,IntMsthotelID
		)

	SELECT   A.dtmCrawlDateTime,A.hotel,A.HotelId,A.HotelCode,A.nvcrContractManager,A.nvcrYieldManager,A.nvcrDemandGroup,
	A.nvcrSegmentation,A.nvcrHotelChain,A.nvcrhotelstatus as Status,A.nvcrHotelContractingType,A.nvcrTPS,date_format(A.Dates,'%m/%d/%Y') Dates,A.nvcrLeadTime,
	PointOfSale,
	A.Company,Currency,
	A.price as price,ContractName,nvcrRoomAvailability,roomtype,Board,PageURL,
	roomtype as CompetitorRoomType,Board as CompetitorBoardType,PageURL as CompetitorPageUrl,
	nvcrCity, city nvcrcitycode, IntMsthotelID
	FROM LastResultSummuryReport A
	INNER JOIN Temp_DS_ListPrice G
	ON Ltrim(Rtrim(A.hotel)) = Ltrim(Rtrim(G.Hotel)) AND Ltrim(Rtrim(A.HotelCode)) = Ltrim(Rtrim(g.HotelCode)) 
	AND Ltrim(Rtrim(A.Dates)) = Ltrim(Rtrim(g.Dates)) AND Ltrim(Rtrim(A.price)) = Ltrim(Rtrim(g.price)) AND Ltrim(Rtrim(A.Company)) = Ltrim(Rtrim(g.Company))
	Where A.intDiPBagDynamicId = p_intdipbagdynamicid;



	Update Temp_DS T Inner Join PointOfSale POS 
		On T.PointOfSale = POS.nvcrCountryShortCode set T.PointOfSale = POS.nvcrCountryName;


	Select Company Into v_StrSupplierName From Temp_DS Where Company != 'Bedsonline';

	Update Temp_DS Set Company = 'Booking' Where Company != 'Bedsonline';

	CReate TEMPORARY table Temp_DS1
	(
	`ID` Int Primary Key Auto_increment, 
	`dtmCrawlDateTime` nvarchar(100),
	 Hotel nvarchar(500),
	 HotelID nvarchar(100),
	 HotelCode nvarchar(100),
	 `Contract Manager` nvarchar(500),
	 `Yield Manager` nvarchar(500),
	 `Demand Group` nvarchar(500),
	 Segmentation nvarchar(500),
	 `Chain Name` nvarchar(500),
	 Status nvarchar(500),
	 `Hotel Contracting Type` nvarchar(500),
	 TPS nvarchar(500),
	 Dates nvarchar(100),
	 `Lead Time` nvarchar(100),
	 PointOfSale nvarchar(500),
	 Currency nvarchar(100),

	 Roomtype nvarchar(500),
	 Board nvarchar(500),
	 ContractName nvarchar(500),
	 RoomAvailability nvarchar(500),

	 Company nvarchar(500),
	 Price nvarchar(100),

	 BedsonlineRoomType nvarchar(500),
	 BedsonlineBoardType nvarchar(500),
	 BedsonlinePageUrl longtext,

	 CompetitorRoomType nvarchar(500),
	 CompetitorBoardType nvarchar(500),
	 CompetitorPageUrl longtext,


	 Booking  nvarchar(500),
	 BedsOnline  nvarchar(500),
	  Destination nvarchar(500),
	 `Destination Code` nvarchar(500)
	);


	CREATE INDEX Hotel ON Temp_DS1(`Hotel`);
    


	insert into Temp_DS1(`dtmCrawlDateTime` ,Hotel,HotelCode,Dates,Booking,BedsOnline )
	Select dtmCrawlDateTime ,Hotel,HotelCode, date_format(Dates,'%m/%d/%Y') Dates, 0 Booking, 0 BedsOnline 
		from 
        (
			select date_format(`dtmCrawlDateTime`,'%m/%d/%Y') as dtmCrawlDateTime,Hotel,HotelCode,Dates
			  from Temp_DS  
		) as S;


	Drop Temporary Table If Exists Temp_DS1_MinPrice;
    Create Table Temp_DS1_MinPrice
    As 
	select date_format(`dtmCrawlDateTime`,'%m/%d/%Y') as dtmCrawlDateTime,Hotel,HotelCode,Dates,
			company, Min(price) price from Temp_DS  
	Group by date_format(`dtmCrawlDateTime`,'%m/%d/%Y') ,Hotel,HotelCode,Dates,company;
    
    
	Update Temp_DS1 T Inner Join Temp_DS1_MinPrice TMP
		On T.dtmCrawlDateTime = TMP.dtmCrawlDateTime
        And T.Hotel = TMP.Hotel
        And T.HotelCode = TMP.HotelCode
        And T.Dates = TMP.Dates
        And T.company = "Booking"
    Set Booking = TMP.price;
    
	
    Update Temp_DS1 T Inner Join Temp_DS1_MinPrice TMP
		On T.dtmCrawlDateTime = TMP.dtmCrawlDateTime
        And T.Hotel = TMP.Hotel
        And T.HotelCode = TMP.HotelCode
        And T.Dates = TMP.Dates
        And T.company = "bedsonline"
    Set Booking = TMP.price;
    
    


 

	update Temp_DS1 tmp1
	inner join Temp_DS tmp
	on tmp1.hotel=tmp.hotel 
	And tmp1.Dates = tmp.Dates
	set 
	tmp1.Destination=tmp.Destination,
	tmp1.`Destination Code` = tmp.`Destination Code`
	where tmp.Company='bedsonline' or tmp.Company='booking';

	update Temp_DS1 tmp1
	inner join Temp_DS tmp
	on tmp1.hotel=tmp.hotel
	And tmp1.Dates = tmp.Dates
	set 
	tmp1.ContractName=tmp.ContractName,
	tmp1.RoomAvailability=tmp.RoomAvailability
	where tmp.Company='bedsonline'; 
 

	update Temp_DS1 tmp1 inner join Temp_DS tmp
		On tmp1.HotelCode = tmp.HotelCode
		And tmp1.Dates = tmp.Dates
		And tmp1.hotel=tmp.hotel
		inner join LastResultSummuryReport LR
		On LR.intMSTHotelId = tmp.IntMsthotelID
		And LR.Dates = tmp1.Dates
		set tmp1.`Chain Name` = LR.nvcrHotelChain,
			tmp1.Segmentation=LR.nvcrSegmentation,
			tmp1.`Demand Group` = LR.nvcrDemandGroup,
			tmp1.`Yield Manager` = LR.nvcrYieldManager,
			tmp1.`Contract Manager` = LR.nvcrContractManager 
			Where LR.intDiPBagDynamicId = p_intdipbagdynamicid;
		

	update Temp_DS1 tmp1 inner join Temp_DS tmp
		On tmp1.HotelCode = tmp.HotelCode
		And tmp1.Dates = tmp.Dates
		inner join Msthotel MH
		On MH.intHotelId = tmp.IntMsthotelID -- And MH.intSupplierId in (6,20)
		Inner Join HotelMonitor.MstHotelStatus MS
		On MH.intStatusID = MS.intStatusID
		set tmp1.Status= MS.vcrStatus;

-- Added by Bhushan Gaud on 22 Nov 2017 as Ops team facing status issue for secondary Hotel start
	Update Temp_DS1 Set 
			`Status` = '' 
			Where HotelCode < 0; 
-- Added by Bhushan Gaud on 22 Nov 2017 as Ops team facing status issue for secondary Hotel end




	update Temp_DS1 tmp1
	inner join Temp_DS tmp
	on tmp1.hotel=tmp.hotel
	And tmp1.Dates = tmp.Dates
	set tmp1.`Hotel Contracting Type`=tmp.`Hotel Contracting Type`
	, tmp1.TPS=tmp.TPS
	where tmp.Company='bedsonline'; 
 

	update Temp_DS1 tmp1
	inner join Temp_DS tmp
	on tmp1.hotel=tmp.hotel
	And tmp1.Dates = tmp.Dates
	set 
	tmp1.PointOfSale=tmp.PointOfSale, 
	tmp1.Currency=tmp.Currency
	where tmp.Company='bedsonline' or tmp.Company='booking';
 

	update Temp_DS1 tmp1
	inner join Temp_DS tmp
	on tmp1.hotel=tmp.Hotel and tmp1.hotelcode=tmp.Hotelcode and tmp1.dates=tmp.Dates
	set 
	tmp1.BedsonlineRoomType=tmp.BedsonlineRoomType,
	tmp1.BedsonlineboardType=tmp.BedsonlineboardType,
	tmp1.BedsonlinePageUrl=tmp.BedsonlinePageUrl
	where tmp.Company='bedsonline';

 

	update Temp_DS1 tmp1
	inner join Temp_DS tmp
	on tmp1.hotel=tmp.Hotel and tmp1.hotelcode=tmp.Hotelcode and tmp1.dates=tmp.Dates
	set 
	tmp1.competitorPageUrl=tmp.competitorPageUrl,
	tmp1.competitorRoomType=tmp.competitorRoomType,
	tmp1.competitorboardType=tmp.competitorboardType
	where tmp.Company='booking';

 


	Update Temp_DS1 Set 
		BedsonlineRoomType = '',
		BedsonlineBoardType = '',
		BedsonlinePageUrl = '',
		ContractName = '',
		RoomAvailability = ''
		Where Ifnull(BedsOnline,'') = '';

	Update Temp_DS1 Set 
		CompetitorRoomType = '',
		CompetitorBoardType = '',
		CompetitorPageUrl = ''
		Where Ifnull(Booking,'') = '';


			
            
	select `Demand Group` into v_nvcrDemandGroup from Temp_DS where `Demand Group` is not null 
		group by `Demand Group` Limit 1;

	update Temp_DS
	set `Demand Group`=v_nvcrDemandGroup;


	select `dtmCrawlDateTime` as `Report Delivery`,
	Hotel,
	HotelCode,
	`Contract Manager`,
	`Yield Manager`,
	`Demand Group`,
	Segmentation,
	`Chain Name`,
	Status,
	`Hotel Contracting Type` as `Distribution Source`,
	TPS,
	Dates   Dates,
	`Lead Time`,
	PointOfSale,
	Currency,
	BedsOnline as `BedsOnline Price`,
	BedsonlineRoomType as `Bedsonline Room Type`,
	BedsonlineBoardType as `Bedsonline Board Type`,
	ContractName as `Contract Name`,
	RoomAvailability as `Room Availability`,
	BedsonlinePageUrl as `Bedsonline Page Url`,
	v_StrSupplierName as `Competitor Name`,
	Booking as `Competitor Price`,
	CompetitorRoomType as `Competitor Room Type`,
	CompetitorBoardType as `Competitor Board Type`,
	CompetitorPageUrl as `Competitor Page URL`,
	Destination,
	`Destination Code`
	from Temp_DS1
	Order by Cast(HotelCode As unsigned) Desc, cast(Dates As date);


Drop table Temp_DS;
Drop Table Temp_DS1;
Drop Table Temp_DS_ListPrice;
 
	
	Select Max(BIntLastResultID) Into v_BIntLastResultID 
		From LastResultSummuryReport  Where intDiPBagDynamicId =  p_intdipbagdynamicid; 
	
	While (v_RowCnt > 0 )  
	Do  
		Delete from LastResultSummuryReport  
		where BIntLastResultID <= v_BIntLastResultID And intdipbagdynamicid = p_intdipbagdynamicid
        Limit 5000;
		SET v_RowCnt = Found_rows();
	End While;  
	 
 

 
END ;;
