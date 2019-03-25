from pymongo import MongoClient
from datetime import datetime
from Common.ProxyClass import ProxyClass
import requests
import json
import csv
from lxml import html, etree
import importlib
import importlib.util
from Common.config_coordinator import config_fetcher

mysql_config = config_fetcher.get_mysql_config
mongodb_config = config_fetcher.get_mongodb_config
services_config = config_fetcher.get_services_config

scriptPath = '/var/www/eCube2.0/GUI/sourceCode/Scripts/'
folderPath = '/var/www/eCube2.0/GUI/sourceCode/Common/Reports/'
entries = ('_id', 'RequestId', 'SubRequestId','RequestRunId','DomainName','PointOfSale','RequestUrl','ProxyIp','ProxyUserName','ProxyPort','CategoryScrappingScript','ProductScrappingScript','ProductParsingScriptName','IsCategory','ScrapingStarttime','ScrapingEndtime','ParsingStarttime','ParsingEndtime')
html_client = MongoClient(mongodb_config['HTML']['URL'])
html_db = html_client.HTMLDumps

crawled_client = MongoClient(mongodb_config['CRAWLED']['URL'])
crawled_db = crawled_client.HTMLDumps


class HtmlResourceFile:

    def entries_to_remove(entries, dict):
        for key in entries:
            if key in dict:
                del dict[key]
        return dict


    def SaveData(self,sourceHtml, sourceUrl):
        html_db.Htmls.insert_one({
            "_id": int(html_db.system_js.getNextSequence("UId")),
            "SourceHTML": sourceHtml,
            "SourceURL": sourceUrl,
            "TimeStamp": str(datetime.now())

        })
        return "Saved successfully"


    # def SaveData(objRequest):
    # def SaveSourceData(self, requestId, subRequestId, domainName, sourceHtml, totalResponse, sourceUrl, pythonScriptName, startDT, endDT, proxyCountry, proxyAddress, proxyPort, proxyUsername, status):
    #     db.HTMLRepository.insert_one({
    #         "_id": int(db.system_js.getNextSequence("HTMLId")),
    #         "RequestId": requestId,
    #         "SubRequestId": subRequestId,
    #         "DomainName": domainName,
    #         "Responses": sourceHtml.decode('utf8'),
    #         'TotalResponses': totalResponse,
    #         "SourceUrl": sourceUrl,
    #         "ParsingScriptName":pythonScriptName,
    #         "ScrappingStartDT": startDT,
    #         "ScrappingEndDT": endDT,
    #         "ProxyCountry": proxyCountry,
    #         "ProxyAddress": proxyAddress,
    #         "ProxyPort": proxyPort,
    #         "ProxyUserName": proxyUsername,
    #         "Status": status,
    #         "TimeStamp": str(datetime.now())
    #     })
    #     return "Saved successfully"

    def SaveSourceData(self, objRequest):
        print ('Hello')
        jsonData = json.loads(objRequest)
        date = datetime.now()
        jsonData['TimeStamp'] = str(datetime.strftime(date,'%Y-%m-%d %H:%M:%S'))
        try:

             jsonData['response'] = jsonData['response'].encode('utf-8')

        except Exception as e:
            print("%%%%%%%%%%%%%%%%%%",e)
        print ('Request Id---',str(jsonData['requestId'] ))
        if(jsonData['status'] == "Success"):
            print('ResponseStart---------------------------')
            res = int(html_db.system_js.getNextSequence("HTMLId"))
            jsonData['_id'] = res
            try:
                print(jsonData)
                html_db.HTMLRepository.insert(jsonData)
            except Exception as e:
                print('Exception', e)
            print('inserted')
        else:

            print ('-------------------------')
            print('PNF')
            res = int(crawled_db.system_js.getNextSequence("PNF_id"))
            print('PNF1')
            jsonData['_id'] = res
            print('PNF2')
            crawled_db.PNFData.insert(jsonData)
            print('PNF3')

        return "Saved successfully"
    # c = d.jsonify({"domainName": "business.conrad.it", "startDT": "2018-01-31 04:54:12.944919", "endDT": "2018-01-31 04:56:30.789373", " totalResponse": 0, " status": "Completed", " pythonScriptName": "ScrapperConradPython_IT.py", " proxyUsername": "", " proxyCountry": "IT", "requestId": "1", "subRequestId": "1", " response": [], " sourceUrl": "http://business.conrad.it/ce/it/product/186821/Piezo-accenditore-13-kV-PR-81-E-2?ref=list", " proxyAddress": "", " proxyPort": ""})
    # HR = HtmlResourceFile()
    # HR.SaveSourceData('',c)

    def FindByUrl(self,url):
        self.resultData = html_db.Htmls.find_one({'SourceURL': url})
        return self.resultData

    def FindHTMLById(self, requestId):
        resultData = html_db.HTMLRepository.find_one({'subRequestId': requestId})
        if resultData:
            output = {'RequestId': resultData['subRequestId'], 'SourceHTML': resultData['response'], 'SourceURL': resultData['sourceUrl']}
        else:
            output = "No Data Found"
        return output

    def GetProxy(self, domainName, proxyCountry):
        objProxy = ProxyClass()
        objProxy.address = ''
        objProxy.port = ''
        objProxy.username = ''
        objProxy.password = ''
        return objProxy

    def GetUserAgent(self, domainName):
        result = requests.post('http://%s/site2/api/v1/getUserAgentName' % services_config['SERVICES_IP'],
                               json={"domainName": domainName, "comments": "Comments"})
        # result = requests.post('http://192.168.7.128/site2/api/v1/getUserAgentName',
        #                        json={"domainName": referer, "comments": "Comments"})
        if result.status_code == 200:
            userAgent = result.text
        else:
            userAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        return userAgent

    def GetHeader(self, domainName):
        try:
            # get Useragent to create headers
            userAgent = HtmlResourceFile().GetUserAgent(domainName)
            result = requests.get('http://%s/getDomainHeader?domainName=%s' % (services_config['SERVICES_IP'], domainName))
            if result.status_code == 200:
                jsonData = {}
                my_json = result.content.decode('utf8').replace("'", '"')
                result = json.loads(my_json)
                for item in result['ResultData']:
                    jsonData[item['HeaderName']] = item['HeaderValue']
                jsonData['User-Agent'] = userAgent
                return jsonData
            else:
                return ''
        except Exception as e:
            print(e)

    def GetSourceHtml(self, header, url, objProxy):
        global proxyaddress
        global proxyuser
        global proxypassword
        headers = header
        txt = ''


        proxyaddress = objProxy.address+':'+ objProxy.port
        #
        #
        # proxies = {"https": 'https://' + proxyaddress}
        proxies = {"https": 'https://' + objProxy.username + ':' + objProxy.password + '@' + proxyaddress}
        s = requests.Session()

        try:
            content = s.get(url, proxies=proxies, headers=headers, verify=False)
        except requests.exceptions.RequestException as e:
            print('Error')

        else:
            print('Success')

            sourceCode = content.text
            htmlElem = html.document_fromstring(sourceCode)
            txt = etree.tostring(htmlElem, pretty_print=True)
        return txt

    def SaveCrawlData(self,objRequest):
        jsonData = {}
        datapoints = objRequest['DataPoints']
        for key, value in datapoints[0].items():
            jsonData[key] = value
        del objRequest['DataPoints']
        for key, value in objRequest.items():
            jsonData[key] = value
        jsonData['_id'] = int(crawled_db.system_js.getNextSequence("Crawl"))
        crawled_db.CrawlResponse.insert(jsonData)
        return "Saved successfully"

    def GetCrawlArgs(self, **objRequest):
        requestId = objRequest['requestId']
        subRequestId = objRequest['subRequestId']
        requestUrl = objRequest['sourceUrl']
        response = objRequest['response']
        status = objRequest['status']
        startDatetime = objRequest['startDT']
        endDatetime = objRequest['endDT']
        isCategory = objRequest['IsCategory']
        pointOfSale = '' #objRequest['PointOfSale']

        #categoryScraperScript = objRequest['pythonScriptName']
        categoryScraperScript = objRequest['ScrapperScript']

        parserScript = '' #objRequest['ProductParsingScriptName']
        domainName = objRequest['domainName']
        productScraperScript = '' #objRequest['ProductScrappingScript']
        args = [int(requestId), int(subRequestId), requestUrl, response, status, startDatetime, endDatetime,
                isCategory,
                pointOfSale, categoryScraperScript, parserScript, domainName, productScraperScript]
        return args

    def GetCrawlResponse(self,id):
        resultData = []
        result = crawled_db.CrawlResponse.find({'RequestRunId': id})
        for item in result:
            finaldict = HtmlResourceFile.entries_to_remove(entries, item)
            resultData.append(finaldict)
        return resultData

    def GetCrawledResponseByRequest(self, id):
        resultData = []
        result = crawled_db.CrawlResponse.find({'requestId': id})
        for item in result:
            resultData.append(item)
        return resultData


    def CreateCSVReport(self, objData, filename):
        report_data = open(folderPath + filename, 'w', newline='')
        csvwriter = csv.writer(report_data)
        count = 0
        for data in objData:
            if count == 0:
                header = data.keys()
                csvwriter.writerow(header)
                count += 1
            csvwriter.writerow(data.values())
        report_data.close()
        return "Report Created Successfully"

    def getScraperInstance(self,ScraperModuleName):
        spec = importlib.util.spec_from_file_location("module.name",
                                                      scriptPath+ScraperModuleName)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        instance = module.ScrapperConradPython_IT()
        return instance

    def getParserInstance(self,htmlEle,ParserModuleName):
        spec = importlib.util.spec_from_file_location("module.name",
                                                      scriptPath + ParserModuleName)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        instance = module.ConradPython_IT(htmlEle)
        return instance

    def GetAttributes(self,RequestId):
        result = requests.get('http://%s/site3/api/v1/GetCrawledDataMapper?requestId=%s' % (services_config['SERVICES_IP'], str(RequestId)))
        if result.status_code == 200:
            my_json = result.content.decode('utf8').replace("'", '"')
            resultData = json.loads(my_json)
            return resultData
        else:
            return result.content

    def ProductCrawl(self,RequestUrl,DomainName,Country, ScraperModuleName):
        objHRF = HtmlResourceFile()
        Instance = objHRF.getScraperInstance(ScraperModuleName)
        print("Instance", Instance)
        dict = Instance.getProductCrawl(RequestUrl,DomainName,Country)

        r = json.dumps(dict)
        loaded_r = json.loads(r)
        return loaded_r

    def ProductParse(self, htmlElement, requestId, parserModuleName):
        htmlElement = html.fromstring(htmlElement)
        dictResult = {}
        objHRF = HtmlResourceFile()
        Instance = objHRF.getParserInstance(htmlElement,parserModuleName)
        Attributes = objHRF.GetAttributes(requestId)
        for item in Attributes['ResultData']:
            Method_for_call = getattr(Instance, item['FieldName'])
            result = Method_for_call()
            dictkey = item['FieldName']
            dictResult[dictkey] = result
        r = json.dumps(dictResult)
        loaded_r = json.loads(r)
        return loaded_r
    # def FindAll(self):
    #     resultData = db.Mouser.find()
    #     return resultData

