import json
# import win32com.client
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
from datetime import datetime
# import final_crawler_19_02_2018
from pdb import set_trace as st
from eCubeLog import logger

class ScriptsExecution:
    import os
    if 'http_proxy' in os.environ:
        os.environ.pop('http_proxy')
    if 'https_proxy' in os.environ:
        os.environ.pop('https_proxy')

    global RequestId,RequestUrl,Attributes, RequestRunId, SubRequestId, htmlElement, DomainName, PointOfSale, IsCategory, ScraperScript, ParserScript, ScraperModuleName, ParserModuleName, Country, ParserScript


    def ConsumerRequestData(self, **consume_data):

        # # changes  added by ankush
        #
        #consume_data = consume_data['consume_data']



        global RequestId,RequestUrl,Attributes, RequestRunId, SubRequestId, htmlElement, DomainName, PointOfSale, IsCategory, ScraperScript, ParserScript, ScraperModuleName, ParserModuleName, Country, ParserScript


        RequestId = str(consume_data["requestId"])
        RequestRunId = consume_data["RequestRunId"]
        SubRequestId = consume_data["subRequestId"]
        htmlElement = consume_data['response']
        DomainName = consume_data["domainName"]
       # ScraperScript = consume_data["pythonScriptName"]
        RequestUrl = consume_data["sourceUrl"]
        ParserScript = consume_data["ParserScript"]

        #Country = consume_data["Country"]
        # PointOfSale = consume_data["PointOfSale"]
        # IsCategory = consume_data["IsCategory"]
        # consume_data[" pythonScriptName"] = "MouserPython_US.py"



        # if consume_data["pythonScriptName"]:
        #     ScraperModuleName = consume_data["pythonScriptName"]
        #     ScraperModuleName = re.sub(".py", "", ScraperModuleName)
        #
        if consume_data["ParserScript"]:
            ParserModuleName = consume_data["ParserScript"]
            ParserModuleName = re.sub(".py", "", ParserScript)

        a = ScriptsExecution.Product('')


        return a

    def getInstance(self,htmlEle):
        module = __import__(ParserModuleName)
        class_ = getattr(module, ParserModuleName)
        instance = class_(htmlEle)
        return instance

    def Product(self):

        # # Added for ML script
        #try:
        #    soup = BeautifulSoup(htmlElement['htmlElement'])
        #except:
        #    soup = BeautifulSoup(htmlElement)

        #html_out = final_crawler_19_02_2018.wrapper_func(soup)


        dictResult = {}
        #st()

        if htmlElement== False :
            return 'PNF'



        '''
                Code  Added by Rahul R and Ankush To Handle Meta Data Is Robot or  
        '''


        try:
            try:
                html_Element = BeautifulSoup(htmlElement['htmlElement'], 'html.parser')

            except:
                html_Element = BeautifulSoup(htmlElement, 'html.parser')
            data = html_Element.findAll("meta")[0]['name']
            if data.lower() == "robots":
                # print("PNF")
                return "PNF"
        except:
            pass

        try:
            try:

                html_Element = BeautifulSoup(htmlElement['htmlElement'], 'html.parser')
            except:
                html_Element = BeautifulSoup(htmlElement, 'html.parser')


            data = html_Element.findAll("title")[0].text
            print(data)
            if data == "Access Denied":
                return "Access Denied"
        except:
            pass




        Instance = ScriptsExecution.getInstance('',htmlElement)
        Attributes = ScriptsExecution.GetAttributes('',RequestId)

        # for product in listUrl:
        # try:

        for item in Attributes['ResultData']:
                print("%%%%%%%%%%%%%%%%%%%%%",item)
                Method_for_call = getattr(Instance, item['FieldName'])
                result = Method_for_call()
                #result = 'Hi'
                dictkey = item['FieldName']
                dictResult[dictkey] = result
                # print("'"+item+"' : '"+result+"'")
        # except TypeError as e:
        #     return 'Error'
        r = json.dumps(dictResult)
        loaded_r = json.loads(r)
        jsondata = {'DataPoints': [loaded_r], "requestId": str(RequestId), "subRequestId": str(SubRequestId),
                    "RequestRunId":int(RequestRunId),
                     "DomainName": DomainName,
                    "RequestUrl": RequestUrl, "IsCategory": "No","status":"Completed"}
        jsondata['IsCategory'] = "No"
        print("************************")
        # ML Script append
        #jsondata['html_file'] = html_out


        print ('final'+str(jsondata))
        result = requests.post('http://192.168.8.7/site3/api/v1/SaveResponseData',json = jsondata)
        print("RESPONSE OUTPUT",result.content)
        return result

    def GetAttributes(self,RequestId):
        import os
        if 'http_proxy' in os.environ:
            os.environ.pop('http_proxy')
        if 'https_proxy' in os.environ:
            os.environ.pop('https_proxy')
        result = requests.get('http://192.168.8.7/site3/api/v1/GetCrawledDataMapper?requestId='+RequestId)
        if result.status_code == 200:
            my_json = result.content.decode('utf8').replace("'", '"')
            resultData = json.loads(my_json)
            return resultData
        else:
            return result.content




# Added for ML Script

# with open ("/home/tech/Ecube2.0MessagingQueueLatest/ParsingService/newhtml",'r') as fp:
#     file = fp.read()
#
# consume_data = {
#     "requestId": "1555",
#     "subRequestId":"82222",
#     "htmlElement":str(file),
#     "domainName":"chxjkch",
#     "pythonScriptName":"dsad.py",
#     'response':str(file),
#     'RequestRunId':'123',
#     'sourceUrl':'',
#     'ParserScript':'ConradPython_IT.py',
#
#
# }
# x = ScriptsExecution()
# x.ConsumerRequestData(consume_data=consume_data)





