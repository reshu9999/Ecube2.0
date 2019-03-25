DELIMITER ;;

CREATE PROCEDURE `spInsertHotelFlightCrawlRequestDetails`(
	IN RequestId INT,
	IN RequestRunId INT,
	IN HotelFlightRequestInputDetailsId INT, 
	IN CheckinDate DATE
)
BEGIN
/*******************************************************************         
'	Name					: spInsertHotelFlightCrawlRequestDetails
'	Desc					: To insert data into tbl_HotelFlightCrawlRequestDetail
'	Called by				: 
'	Example of execution	: call spInsertHotelFlightCrawlRequestDetails(1, 4, 10, '2018-05-28');
INPUT PARAMETRS		 	 
	RequestId INT,
	RequestRunId INT,
	HotelFlightRequestInputDetailsId INT, 
	CheckinDate DATE
OUTPUT PARAMETRS

'	Created by				: Bhavin.Dhimmar
'	Date of creation		: 05-Jun-2018

******************************************************************************************************
Change History
******************************************************************************************************
Sr.No.		Date:			Changed by:					Description:
******************************************************************************************************/	
	Drop temporary table if exists tbl_Numbers_Comp;
	CREATE TEMPORARY TABLE tbl_Numbers_Comp LIKE tbl_Numbers;
	INSERT INTO tbl_Numbers_Comp SELECT * FROM tbl_Numbers;

	Drop temporary table if exists tbl_Numbers_Star;
	CREATE TEMPORARY TABLE tbl_Numbers_Star LIKE tbl_Numbers;
	INSERT INTO tbl_Numbers_Star SELECT * FROM tbl_Numbers;

	Drop temporary table if exists tbl_Numbers_Board;
	CREATE TEMPORARY TABLE tbl_Numbers_Board LIKE tbl_Numbers;
	INSERT INTO tbl_Numbers_Board SELECT * FROM tbl_Numbers;

	Drop temporary table if exists tbl_Numbers_RoomType;
	CREATE TEMPORARY TABLE tbl_Numbers_RoomType LIKE tbl_Numbers;
	INSERT INTO tbl_Numbers_RoomType SELECT * FROM tbl_Numbers;

	INSERT INTO `eCube_Centralized_DB`.tbl_HotelFlightCrawlRequestDetail
        (
        RequestId,
		RequestRunId,
		hotelflightrequestinputdetailsId,
		StatusId,
		FlightSearchType,
		CheckInDate,
		RentalLength,
		CompetitorName,
		PointOfSale,
		Adult,
		Child,
		CrawlMode,
		FromAirportCode,
		ToAirportCode,
		HotelName,
		WebSiteHotelId,
		FromCountryName,
		FromCityName,
		ToCountryName,
		ToCityName,
		StarRating,
		BoardType,
		RoomType,
		CreatedDatetime,
		call_func
        )
	Select a.RequestId, RequestRunId,a.HotelFlightRequestInputDetailsId,5 as status 
 		, flitype.FlightSearchType
        , CheckInDate as CheckInDate
		-- , a.RentalLength
        , SUBSTRING_INDEX(SUBSTRING_INDEX(a.rentalLength, ',', tnr.num), ',', -1) as RentalLength
        -- , a.CompetitorIds -- , SUBSTRING_INDEX(SUBSTRING_INDEX(a.CompetitorIds, ',', tncompId.num), ',', -1) as CompetitorIds
        -- 		(select name from tbl_Competitor where Id=a.CompetitorIds) as CompletitorName,
        , com.Name as CompletitorName
        -- ,(select PointOfSale from HotelPOS where PointOfSaleId=a.PointOfSaleId) as POS,
        , pos.PointOfSale
		, a.AdultId,a.ChildID -- ,(select CrawlMode from CrawlModes where CrawlModeId=a.CrawlMode) as CrawlMode,
        , cmode.CrawlMode
        , aircodefrom.AirportCode, aircodeto.AirportCode
        , hot.HotelName as HotelName, hot.WebSiteHotelId as WebSiteHotelId
		-- (select HotelName from Hotels where HotelId=a.HotelId) as HotelName,'WebSiteHotelId',
        -- , city.CityName -- (select CityName from Cities where CityId=a.CityId) as CityName,
		-- , countr.CountryName -- (select CountryName from tbl_CountryMaster where CountryId=a.CountryId) as CountryName,
        -- ,a.StarRating
        , countrfrom.CountryName, cityfrom.CityName
        , countrto.CountryName, cityto.CityName
 		, Astar.StarRating as StarRatting-- (select StarRating from StarRatings where StarRatingId=a.StarRating) as StarRatting,
 		, aBoard.BoardTypeDescription-- (select BoardTypeCode from BoardTypes where BoardTypeId=a.BoardType)  as BoardType,
		-- (select RoomType from RoomTypes where RoomTypeId=a.RoomType) as RoomType,
        , aRoomType.RoomType
		,now(),a.call_func
       from tbl_hotelflightrequestinputdetails as a 
		inner join tbl_Numbers tnr on CHAR_LENGTH(a.rentalLength)-CHAR_LENGTH(REPLACE(a.rentalLength, ',', ''))>=tnr.num-1
        inner join tbl_Numbers_Comp tncompId on CHAR_LENGTH(a.CompetitorIds)-CHAR_LENGTH(REPLACE(a.CompetitorIds, ',', ''))>=tncompId.num-1
		inner join tbl_Competitor com on com.id = SUBSTRING_INDEX(SUBSTRING_INDEX(a.CompetitorIds, ',', tncompId.num), ',', -1)
        inner join FlightSearchType flitype on a.FlightSearchTypeID = flitype.FlightSearchTypeID
        inner join HotelPOS pos on pos.PointOfSaleId=a.PointOfSaleId
        inner join CrawlModes cmode on cmode.CrawlModeId=a.CrawlMode
        left join Hotels hot on hot.HotelId=a.HotelId
        inner join AirportCodes aircodefrom on a.FromAirportCodeId = aircodefrom.AirportCodeId
        inner join Cities cityfrom on cityfrom.CityId=aircodefrom.CityId
        inner join tbl_CountryMaster countrfrom on  countrfrom.CountryId=aircodefrom.CountryId
        inner join AirportCodes aircodeto on a.ToAirportCodeId = aircodeto.AirportCodeId
        inner join Cities cityto on cityto.CityId=aircodeto.CityId
        inner join tbl_CountryMaster countrto on  countrto.CountryId=aircodeto.CountryId
		left join (
					select Astar.RequestId,Astar.hotelflightrequestinputdetailsId, group_concat(StarRating) StarRating
					from (
						select Astar.RequestId,Astar.hotelflightrequestinputdetailsId, Astar.StarRating as StarRatingIds-- , a.* 
						, star.StarRating
						from tbl_hotelflightrequestinputdetails as Astar 
								inner join tbl_Numbers_Star tnstar on CHAR_LENGTH(Astar.StarRating)-CHAR_LENGTH(REPLACE(Astar.StarRating, ',', ''))>=tnstar.num-1
								inner join StarRatings star on star.StarRatingId=SUBSTRING_INDEX(SUBSTRING_INDEX(Astar.StarRating, ',', tnstar.num), ',', -1)
						where Astar.hotelflightrequestinputdetailsId =HotelFlightRequestInputDetailsId -- Astar.RequestId= RequestId and 
						) Astar 
					group by Astar.RequestId,Astar.hotelflightrequestinputdetailsId
					) Astar
                    on a.RequestId = Astar.RequestId and a.hotelflightrequestinputdetailsId = Astar.hotelflightrequestinputdetailsId
		left join (
						select aBoard.RequestId,aBoard.hotelflightrequestinputdetailsId, group_concat(BoardTypeDescription) BoardTypeDescription
						from (
							select aBoard.RequestId,aBoard.hotelflightrequestinputdetailsId, aBoard.BoardType -- , aBoard.* 
							 -- , SUBSTRING_INDEX(SUBSTRING_INDEX(aBoard.BoardType, ',', tnboard.num), ',', -1) as BoardType
							 , boar.BoardTypeDescription
							from tbl_hotelflightrequestinputdetails as aBoard 
									inner join tbl_Numbers_Board tnboard on CHAR_LENGTH(aBoard.BoardType)-CHAR_LENGTH(REPLACE(aBoard.BoardType, ',', ''))>=tnboard.num-1
									inner join BoardTypes boar on boar.BoardTypeId=SUBSTRING_INDEX(SUBSTRING_INDEX(aBoard.BoardType, ',', tnboard.num), ',', -1)
							where aBoard.hotelflightrequestinputdetailsId =HotelFlightRequestInputDetailsId -- aBoard.RequestId= RequestId and 
						) aBoard
						group by aBoard.RequestId,aBoard.hotelflightrequestinputdetailsId
					) aBoard
                    on a.RequestId = aBoard.RequestId and a.hotelflightrequestinputdetailsId = aBoard.hotelflightrequestinputdetailsId
		left join (
					select aRoomType.RequestId,aRoomType.hotelflightrequestinputdetailsId, group_concat(RoomType) RoomType
					from (
						select aRoomType.RequestId,aRoomType.hotelflightrequestinputdetailsId, aRoomType.RoomType as RoomTypeIds -- , aRoomType.* 
						 -- , SUBSTRING_INDEX(SUBSTRING_INDEX(aRoomType.BoardType, ',', tnboard.num), ',', -1) as BoardType
						 , room.RoomType
						from tbl_hotelflightrequestinputdetails as aRoomType 
								inner join tbl_Numbers_RoomType tnroom on CHAR_LENGTH(aRoomType.RoomType)-CHAR_LENGTH(REPLACE(aRoomType.RoomType, ',', ''))>=tnroom.num-1
								inner join RoomTypes room on room.RoomTypeId=SUBSTRING_INDEX(SUBSTRING_INDEX(aRoomType.RoomType, ',', tnroom.num), ',', -1)
						where aRoomType.hotelflightrequestinputdetailsId =HotelFlightRequestInputDetailsId -- aRoomType.RequestId= RequestId and 
					) aRoomType
					group by aRoomType.RequestId,aRoomType.hotelflightrequestinputdetailsId
                    )aRoomType 
                    on a.RequestId = aRoomType.RequestId and a.hotelflightrequestinputdetailsId = aRoomType.hotelflightrequestinputdetailsId
  where a.hotelflightrequestinputdetailsId = HotelFlightRequestInputDetailsId -- a.RequestId= RequestId 
	;
        
END ;;
