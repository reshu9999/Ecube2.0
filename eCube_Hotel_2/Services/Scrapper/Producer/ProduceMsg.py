#Python Producer

from models.config import Base,session
from multiprocessing import Process
from datetime import timedelta
import pika
import json
from pdb import set_trace as st


def produceMsg(runid):
    hotelCrawlRequesttbl=Base.classes.tbl_HotelCrawlRequestDetail
    domainMasttbl=Base.classes.tbl_DomainMaster
    competitortbl=Base.classes.tbl_Competitor
    data=session.query(hotelCrawlRequesttbl).filter_by(RequestRunId=runid).all()
    domainlist=session.query(domainMasttbl,competitortbl).filter(competitortbl.Id==domainMasttbl.competitorid).all()
    domainData={}
    for rec in domainlist:
        '''
        domainData Dictionary stores '|' separated data first index is domain and second index is Scrapper File name from domain master.
        '''
        domainData[rec.tbl_Competitor.name]=rec.tbl_DomainMaster.DomainName+'|'+('' if rec.tbl_DomainMaster.ParsingScriptName is None else 
                                                                                rec.tbl_DomainMaster.ParsingScriptName)
    data_row_dict={}
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    for rec in data:
        data_row_dict['requestId']=rec.RequestId or ""
        data_row_dict['subRequestId']=rec.HotelReqestInputDetailsId or ""
        data_row_dict['requestRunId']=rec.RequestRunId or ""
        data_row_dict['domainName']= domainData[rec.CompetitorName].split('|')[0]
        data_row_dict['CrawlerScript']=domainData[rec.CompetitorName].split('|')[1]
        data_row_dict['country']=rec.CountryName or ""
        RequestInputs={}
        RequestInputs['city']=rec.CityName or ""
        RequestInputs['children']=rec.Child or ""
        RequestInputs['adults']=rec.Adult or ""
        RequestInputs['room']=rec.RoomType or ""
        RequestInputs['board']=rec.BoardType or ""
        RequestInputs['checkIn']=rec.CheckInDate.strftime('%d-%m-%Y') or ""
        RequestInputs['checkOut']=(rec.CheckInDate+timedelta(days=rec.RentalLength)).strftime('%d-%m-%Y') or ""
        RequestInputs['nights']=((rec.CheckInDate+timedelta(days=rec.RentalLength))-rec.CheckInDate).days or ""
        RequestInputs['days']=rec.RentalLength
        RequestInputs['hotelName']=rec.HotelName
        RequestInputs['starRating']=rec.StarRating
        RequestInputs['webSiteHotelId']=rec.WebSiteHotelId
        RequestInputs['pos']=rec.PointOfSale
        RequestInputs['crawlMode']=rec.CrawlMode
        data_row_dict['RequestInputs']=RequestInputs

        channel.queue_declare(queue=rec.CompetitorName+'Crawl')
        data=json.dumps(data_row_dict)

        channel.basic_publish(exchange='',
                            routing_key=rec.CompetitorName+'Crawl',
                            body=str(data))
        data_row_dict={}
    connection.close()
'''
ph=Process(target=produceMsg,args=(1,))
ph.run()		
print("End")
'''
