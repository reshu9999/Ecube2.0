from models.config import Base,session
from threading import Thread
from datetime import datetime,time
from eCubelog import logger
from multiprocessing import Process
from ProduceMsg import produceMsg

from pdb import set_trace as st


'''
Declaring the tables in use, first started with Hotel Request. 
Hotel plus Flights tables are declared separately below
'''


#for Hotels 
hotelRequestInputtbl=Base.classes.tbl_hotelrequestinputdetails
hotelCrawlRequesttbl=Base.classes.tbl_HotelCrawlRequestDetail
requestDateDettbl=Base.classes.tbl_HotelRequestsDateDetails

#for Hotels Plus flights
hotelflightrequestinputtbl=Base.classes.tbl_hotelflightrequestinputdetails
hotelflightCrawlReqtbl=Base.classes.tbl_HotelFlightCrawlRequestDetail
hotelflightrequestDateDettbl=Base.classes.tbl_hotelflightRequestsDateDetail
airporttbl=Base.classes.AirportCodes

#common tables
requestRunDetailtbl=Base.classes.tbl_RequestRunDetail
requestMastertbl=Base.classes.tbl_RequestMaster
competitortbl=Base.classes.tbl_Competitor
statustbl=Base.classes.tbl_StatusMaster
ScheduleDatetbl=Base.classes.tbl_ScheduleDate
postbl=Base.classes.HotelPOS
crawlmode=Base.classes.CrawlModes
hoteltbl=Base.classes.Hotels
citytbl=Base.classes.Cities
countrytbl=Base.classes.tbl_CountryMaster
starratingtbl=Base.classes.StarRatings
boardtypetbl=Base.classes.BoardTypes
roomtypetbl=Base.classes.RoomTypes


def insertHRequestDetail(runId,hotelrequestinput):
    hotelrequestinput=hotelrequestinput.all()
    data2insert=[]
    for rec in hotelrequestinput:
        for competitor in rec.CompetitorIds.split(','):
            for length in rec.RentalLength.split(','):
                try:
                    starRec=session.query(starratingtbl).filter_by(StarRatingId=rec.StarRating).one_or_none()
                    boardRec=session.query(boardtypetbl).filter_by(BoardTypeId=rec.BoardType).one_or_none()
                    roomRec=session.query(roomtypetbl).filter_by(RoomTypeId=rec.RoomType).one_or_none()
                    hotelcrawlrequest=hotelCrawlRequesttbl(RequestId=rec.RequestId,RequestRunId=runId,
                                                    HotelReqestInputDetailsId=rec.HotelReqestInputDetailsId,StatusId=5,
                                                    CheckInDate=session.query(requestDateDettbl).filter_by(
                                                    HotelRequestInputDetailsId=rec.HotelReqestInputDetailsId).one().CheckInDate,
                                                    RentalLength=rec.RentalLength,CompetitorName=session.query(
                                                    competitortbl).filter_by(Id=competitor).one().name,
                                                    PointOfSale=session.query(postbl).filter_by(PointOfSaleId=rec.PointOfSaleId).one().PointOfSale,
                                                    Adult=rec.AdultId,Child=rec.ChildID,CrawlMode=session.query(
                                                    crawlmode).filter_by(CrawlModeId=rec.CrawlMode).one().CrawlMode,
                                                    HotelName=session.query(hoteltbl).filter_by(HotelId=rec.HotelId).one().HotelName,
                                                    WebSiteHotelId='',CityName=session.query(citytbl).filter_by(CityId=rec.CityId).one().CityName,
                                                    CountryName=session.query(countrytbl).filter_by(CountryID=rec.CountryId).one().CountryName,
                                                    StarRating=None if starRec is None else starRec.StarRating,
                                                    BoardType=None if boardRec is None else boardRec.BoardTypeCode,
                                                    RoomType=None if roomRec is None else roomRec.RoomType,
                                                    call_func=rec.call_func,
                                                    CreatedDatetime=datetime.now())
                    data2insert.append(hotelcrawlrequest)
                except Exception:
                    logger.error('Object hotelcrawlrequest failed to create for Request ID' + str(rec.RequestId) +': ',exc_info=True)
                    logger.error('-------------------------Error Ends----------------------------------------')
                    print("Error Occured check the Logs...")
                    continue
                 
    try:
        session.bulk_save_objects(data2insert)
        session.commit()
        ph=Process(target=produceMsg,args=(runId,))
        ph.run()
        print("Thread Ended")
    except Exception:
        logger.error('function hotelrequestinput failed to save in DB for RunID ' + str(runId) + ': ', exc_info=True)
        logger.error('------------------------Error Ends-----------------------------------------')
        print("Error Occured check the Logs...")


def insertHFRequestDetail(runId,hotelrequestinput):
    hotelflightrequestinput=hotelrequestinput.all()
    data2insert=[]
    for rec in hotelflightrequestinput:
        for competitor in rec.CompetitorIds.split(','):
            for length in rec.RentalLength.split(','):
                try:
                    checkin=session.query(hotelflightrequestDateDettbl).filter_by(
                                        hotelflightrequestinputdetailsId=rec.hotelflightrequestinputdetailsId).one_or_none()
                    hotelflightcrawlrequest=hotelflightCrawlReqtbl(RequestId=rec.RequestId,RequestRunId=runId,
                                                            hotelflightrequestinputdetailsId=rec.hotelflightrequestinputdetailsId,StatusId=5,
                                                            CheckInDate=datetime.now().strftime('%d-%m-%Y') if checkin is None else checkin.CheckInDate,
                                                            RentalLength=rec.RentalLength,CompetitorName=session.query(
                                                            competitortbl).filter_by(Id=competitor).one().name,
                                                            PointOfSale=session.query(postbl).filter_by(PointOfSaleId=rec.PointOfSaleId).one().PointOfSale,
                                                            Adult=rec.AdultId,Child=rec.ChildID,CrawlMode=session.query(
                                                            crawlmode).filter_by(CrawlModeId=rec.CrawlMode).one().CrawlMode,
                                                            HotelName=session.query(hoteltbl).filter_by(HotelId=rec.HotelId).one().HotelName,
                                                            WebSiteHotelId='',FromAirportCode=session.query(airporttbl).filter_by(
                                                            AirportCodeId=rec.FromAirportCodeId).one().AirportCode,ToAirportCode=session.query(
                                                            airporttbl).filter_by(AirportCodeId=rec.ToAirportCodeId).one().AirportCode,
                                                            call_func=rec.call_func,
                                                            CreatedDatetime=datetime.now())
                    data2insert.append(hotelflightcrawlrequest)
                except Exception:
                    logger.error('Object hotelflightcrawlrequest failed to create for Request ID' + str(rec.RequestId) +': ',exc_info=True)
                    continue
    
    try:
        session.bulk_save_objects(data2insert)
        session.commit()
        print("Thread Ended")
    except Exception: 
        logger.error('function insertHFRequestDetail failed to save in DB for RunID ' + str(runId) + ': ', exc_info=True)
     


if __name__=='__main__':
    '''Start of the Program to it will keep looking for now time records in ScheduleDatetbl '''

    timeNow=time(int(datetime.now().strftime('%H')),int(datetime.now().strftime('%M')))
    #--------------------------------------------------------------------------------------------
    ''' first line is for production, second line is for testing '''
    #data=session.query(ScheduleDatetbl).filter_by(ScheduleTime=timeNow).all()
    data=session.query(ScheduleDatetbl).filter_by(ScheduleDatesId=185).all()
    #data=session.query(ScheduleDatetbl).all()
    #--------------------------------------------------------------------------------------------
    for sched in data:
        reqID=sched.SD_RequestId
        print('Schedule Request ID', reqID)
        typeOfRequest=session.query(requestMastertbl).filter_by(RequestId=reqID).one().RequestModeId
        if typeOfRequest==2:
            requestinput=session.query(hotelRequestInputtbl).filter_by(RequestId=reqID)
        if typeOfRequest==3:
            requestinput=session.query(hotelflightrequestinputtbl).filter_by(RequestId=reqID)
        noOfReq=requestinput.count()
        reqRun=requestRunDetailtbl(FK_RequestId=reqID,TotalRequests=noOfReq,CompletedRequests=0,InQueRequests=noOfReq,
                                PNFCounts=0,FK_StatusId=session.query(statustbl).filter_by(StatusTitle='InQue').one().StatusId,
                                StartDatetIme=datetime.now())
        session.add(reqRun)
        session.commit()
        if typeOfRequest==2:
            #insertHRequestDetail(reqRun.RequestRunId,requestinput)
            t=Thread(target=insertHRequestDetail,args=(reqRun.RequestRunId,requestinput))
        if typeOfRequest==3:
            #insertHFRequestDetail(reqRun.RequestRunId,requestinput)
            t=Thread(target=insertHFRequestDetail,args=(reqRun.RequestRunId,requestinput))
        t.start()
    print("Program End")
