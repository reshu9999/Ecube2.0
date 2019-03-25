from pymongo import MongoClient
from datetime import datetime
from Common.ProxyClass import ProxyClass
import requests
import json
from lxml import html, etree

client = MongoClient('mongodb://localhost:27017/')
db = client.HTMLDumps
# db.Counters.insert_one({
#             "_id": 'UId',
#             "seq": 1
# })
class HtmlResourceFile:
    def SaveData(self,sourceHtml, sourceUrl):
        db.Htmls.insert_one({
            "_id": int(db.system_js.getNextSequence("UId")),
            "SourceHTML": sourceHtml,
            "SourceURL": sourceUrl,
            "TimeStamp": str(datetime.now())

        })
        return "Saved successfully"

    # def SaveData(objRequest):
    def SaveSourceData(self, requestId, subRequestId, domainName, sourceHtml, sourceUrl, pythonScriptName, proxyCountry, proxyAddress, proxyPort, proxyUsername, status):
        db.HTMLRepository.insert_one({
            "_id": int(db.system_js.getNextSequence("HTMLId")),
            "RequestId": requestId,
            "SubRequestId": subRequestId,
            "DomainName": domainName,
            "SourceHTML": sourceHtml.decode('utf8'),
            "SourceUrl": sourceUrl,
            "PythonScriptName":pythonScriptName,
            "ProxyCountry": proxyCountry,
            "ProxyAddress": proxyAddress,
            "ProxyPort": proxyPort,
            "ProxyUserName": proxyUsername,
            "Status": status,
            "TimeStamp": str(datetime.now())
        })
        return "Saved successfully"

    def FindByUrl(self,url):
        self.resultData = db.Htmls.find_one({'SourceURL': url})
        return self.resultData

    def FindHTMLById(self, requestId):
        resultData = db.HTMLRepository.find_one({'SubRequestId': int(requestId)})
        if resultData:
            output = {'RequestId': resultData['RequestId'], 'SourceHTML': resultData['SourceHTML']}
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
        result = requests.post('http://38.76.27.161/site2/api/v1/getUserAgentName',
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
            userAgent = HtmlResourceFile.GetUserAgent(domainName)
            result = requests.get('http://localhost:5001/getDomainHeader?domainName=' + domainName)
            print(result.status_code)
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
    # def FindAll(self):
    #     resultData = db.Mouser.find()
    #     return resultData

