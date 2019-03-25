import json
#import win32com.client
import os
from bs4 import BeautifulSoup
import random
import urllib3, ssl
from lxml import html, etree
import re
import requests
import json
import math
from requests.auth import HTTPProxyAuth
# from datetime import datetime
# from Queues import *
# import Queues
import sys
# from __future__ import print_function
import sys
import ast
import importlib
import datetime
from eCubeLog import logger
from pdb import set_trace as st


class ScriptsExecution:
    #global StartTime


    #global IsPreview, RequestId , RequestRunId, SubRequestId, RequestUrl, DomainName, PointOfSale, IsCategory, ScraperScript, ParserScript,ScraperModuleName,ParserModuleName,Country


    def __init__(self, consume_data):


        #global IsPreview,StartTime,RequestId, RequestRunId, SubRequestId, RequestUrl, DomainName, PointOfSale, IsCategory, ScraperScript, ParserScript, ScraperModuleName, ParserModuleName, Country
        #IsCategory = "1"
        self.RequestInputs = consume_data
        self.IsPreview = "No"
        self.StartTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.RequestId = consume_data["RequestId"]
        self.RequestRunId = consume_data["RequestRunId"]
        self.SubRequestId = consume_data["SubRequestId"]
        self.RequestUrl = consume_data['RequestUrl']
        self.DomainName = consume_data["DomainName"]
        self.PointOfSale = consume_data["PointOfSale"]
        self.IsCategory = consume_data["IsCategory"]
        self.ScraperScript = consume_data["ScraperScript"]
        #ScraperScript = "ConradPython_IT"
        self.ParserScript = consume_data["ParserScript"]
        self.Country = consume_data["Country"]
        self.ScraperModuleName = ''
        # Country = consume_data["Region"]

        # Added by Ankush for Retais /hotel Request Input JSON
        # self.RequestInputs = consume_data['RequestInputs']


        # Added by ankush for Dynamic Queuing
        self.GroupName = consume_data['GroupName']

        if consume_data["ScraperScript"]:
            self.ScraperModuleName = consume_data["ScraperScript"]
            self.ScraperModuleName = re.sub(".py", "", self.ScraperModuleName)

            #ScraperModuleName ="ScrapperConradPython_IT"
        if consume_data["ParserScript"]:
            self.ParserModuleName = consume_data["ParserScript"]
            self.ParserModuleName = re.sub(".py", "", self.ParserModuleName)

        logger.debug('Initialisation complete...:' + str(self.RequestUrl))

    def run(self):
        a = ScriptsExecution.Classification(self)
        return a


    def getInstance(self):

        module = None


        module = importlib.import_module(self.ScraperModuleName)

        # module = __import__('ScrapperConradPython_IT')
        class_ = getattr(module, self.ScraperModuleName)
        instance = class_(self.RequestInputs)
        return instance

    def Classification(self):
        logger.debug("Classfication Called")
        if (self.IsCategory == 1 or self.IsCategory == '1'):


            return ScriptsExecution.Category(self)
        else:

            #return self.Product()
            return ScriptsExecution.Product(self)


    def Category(self):
        #Instance = self.getInstance()
        Instance = ScriptsExecution.getInstance(self)

        dict = Instance.getCategoryCrawl()
        dict['requestId'] = int(self.RequestId)
        dict['subRequestId'] = int(self.SubRequestId)
        dict['RequestRunId'] = int(self.RequestRunId)
        #dict['startDT'] = str(StartTime)
        #dict['endDT'] = str(datetime.now())


        StartTime = datetime.datetime.now()
        StartTimeConverted = datetime.date.strftime(StartTime, '%Y-%m-%d %H:%M:%S')
        dict['startDT'] = str(StartTimeConverted)

        EndTime = datetime.datetime.now()
        EndTimeConverted = datetime.date.strftime(EndTime, '%Y-%m-%d %H:%M:%S')
        dict['endDT'] = str(EndTimeConverted)
        dict['ParserScript'] = str(self.ParserModuleName)

        dict['ScrapperScript'] = str(self.ScraperModuleName)

        # added by ankush
        dict['groupName'] = self.GroupName
        dict['parsingStatus'] = 1  # Message ready for Parsing


        try:
            r = json.dumps(dict)
        except Exception as e:
            logger.error('JSON Dump issue:', exc_info=True)

        # loaded_r = json.loads(r)

        try:
            Data = json.dumps(self.RequestInputs)
            updateSubID = requests.post('http://192.168.8.7/site7/api/v1/update_subrequest_details', json=Data)
            print("UPDATE SbRequestID Service", updateSubID)
        except Exception as e:
            pass

        if (self.IsPreview == "No"):
            result = requests.post('http://192.168.8.7/site3/api/v1/SaveSourceHtml', json=r)
            #result = requests.post('http://192.168.7.128/site3/api/v1/SaveSourceHtml', json=r)
            print("Final OUT",result.content)

        return result.content



    def Product(self):
        logger.debug("Product Called from Category :" + str(self.RequestUrl))
        Instance = ScriptsExecution.getInstance(self)
        dict=Instance.getProductCrawl()

        # dict['Starttime'] = str(StartTime)
        # dict['EndTime'] = str(datetime.now())
        #
        #StartTime = datetime.datetime.now()
        #StartTimeConverted = datetime.date.strftime(StartTime, '%Y-%m-%d %H:%M:%S')
        dict['startDT'] = self.StartTime


        EndTime = datetime.datetime.now()
        EndTimeConverted = datetime.date.strftime(EndTime, '%Y-%m-%d %H:%M:%S')
        dict['endDT'] = EndTimeConverted


        dict['requestId'] = int(self.RequestId)
        dict['subRequestId'] = int(self.SubRequestId)
        dict['RequestRunId'] = int(self.RequestRunId)
        # Added by Ankush
        dict['ParserScript'] = str(self.ParserScript)


        # added by ankush
        dict['groupName'] = self.GroupName
        dict['parsingStatus'] = 1  # Message ready for Parsing

        r = None

        try:
            r = json.dumps(dict)
        except Exception as e:

            logger.error('JSON Dump error: ', exc_info=True)

        loaded_r = json.loads(r)


        logger.debug('Scrapping Done : ' + self.RequestUrl)
        self.result = requests.post('http://192.168.8.7/site3/api/v1/SaveSourceHtml', json=r)

        #self.result = requests.post('http://192.168.7.128/site3/api/v1/SaveSourceHtml', json=r)
        logger.debug("Database Saving Response for "+ str(self.RequestId)  + " : " +self.RequestUrl +" : "+ str(self.result.content) )
        print("Saved Response------",self.result.content)


        try:
            Data = json.dumps(self.RequestInputs)
            updateSubID = requests.post('http://192.168.8.7/site7/api/v1/update_subrequest_details', json=Data)
            print("UPDATE SbRequestID Service", updateSubID)
        except Exception as e:
            pass

        #print("Response recieved",self.result.content)
        return self.result.content




