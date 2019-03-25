#!/usr/bin/env python
from RabbitConnections import Rabbit_connection
from DBConnection import DBconnection
from Common import Commmon
import json
import threading
import requests
from pdb import set_trace as st

class ReportConsumer():
    # print ("calling first consumer")
    def callback(ch, method, properties, body):
        print(body)
        objDBCon =  DBconnection()
        objCommon = Commmon()


        print("Recieving Messages -- %r" % body)
        data = body.decode('utf-8')


        # time.sleep(0.1)
        consume_data = data.replace("'", "\"")
        consume_data = json.loads(consume_data)  # convert string to python dict

        requestRunId = consume_data['RID_RequestRunId']

        reportName = consume_data['ReportName'] + '.csv'

        print("CCCCCCCCCCCCCCCCCC",requestRunId)


        # Update Report Status
        objDBCon.UpdateReportStatus(int(requestRunId),'WIP')
        # Update Report Status End


        # Fetch Crawl Response
        resulData = objDBCon.GetCrawlResponse(requestRunId)

        # Crawl Response End

        if resulData:

            import os
            if 'http_proxy' in os.environ:
                os.environ.pop('http_proxy')
            if 'https_proxy' in os.environ:
                os.environ.pop('https_proxy')

            fieldsRequired= requests.get('http://192.168.8.7/site3/api/v1/GetCrawledDataMapper?requestId='+ str(resulData[0]['requestId']))
            print("%%%%%%%%%%%%%%%%%%%%%%%%%",fieldsRequired.content)
            fieldsRequired=eval(fieldsRequired.content.decode('utf-8'))['ResultData']
            fieldsRequired=[i['TextBoxValue'] for i in fieldsRequired]
            fieldsRequired.append('RequestUrl')

            # CSV Creation
            #objCommon.CreateCSVReport(resulData, reportName,fieldsRequired)

            objCommon.CreateCSVReport(resulData, reportName)
            # CSV Creation End

            # Save Report Link
            objDBCon.SaveReportLink(int(requestRunId), reportName)
            # Report Link End


            # Update Report Status
            objDBCon.UpdateReportStatus(int(requestRunId), 'Completed')
            # Update Report Status End



        ch.basic_ack(delivery_tag=method.delivery_tag)


    channel = Rabbit_connection.ReportQueueConnection("")   # calling Category Queue Connection class
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback,
                      queue='Report')
    channel.start_consuming()




t1 = threading.Thread(target=ReportConsumer,args=[])
t1.start()









