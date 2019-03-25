import urllib3
# from lxml import html
from pymongo import MongoClient
from datetime import datetime
import httpagentparser
import re
import ssl
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# import requests
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
#
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from Common.config_coordinator import config_fetcher



mysql_config = config_fetcher.get_mysql_config
mongodb_config = config_fetcher.get_mongodb_config


class UserAgent:

    def GetDbConnection(self):
        client = MongoClient(mongodb_config['URL'])
        db = client.UserAgents
        return db

   #  def CrawleUserAgents(self):
   #      ListURL = 'http://www.useragentstring.com/pages/useragentstring.php?typ=Browser'
   #      proxyaddress = '77.75.127.122:41998'
   #      proxyuser = 'eclerx'
   #      proxypassword = 'a6UzaMYtY'
   #      proxyheaders = urllib3.make_headers(proxy_basic_auth=proxyuser + ':' + proxypassword,user_agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
   #      proxy = urllib3.ProxyManager('http://' + str(proxyaddress), proxy_headers=proxyheaders, ssl_version=ssl.PROTOCOL_TLSv1_2 )
   #      response = proxy.urlopen(method='GET', url=ListURL, headers=None)
   #      sourceCode = response.data
   #      htmlElem = html.document_fromstring(sourceCode)
   #      links = htmlElem.xpath("//li//a")
   #      p = []
   #
   #      for link in links:
   #          p.append(UserAgent.checkAgent(link.text))
   #
   #      for x in p:
   #          if x != 'None':
   #              UserAgent.SaveData(ListURL, x)
   #
   #      # print(len(p))
   #      # print(len(temp))
   #      return "User Agents saved successfully!!!"
   #
   # # url = 'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/windows/'
   #
    # def CrawleUserAgents1(self):
    #     ListURL = 'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/windows/'
    #     # for i in range(1, 3307):
    #     UA = UserAgent()
    #     for i in range(1, 100):
    #         url = ListURL + str(i)
    #         proxyaddress = 'pune.wonderproxy.com:80'
    #         # proxyaddress = '217.182.98.176:29842'
    #         # proxyaddress = '192.198.113.185:58327'
    #         # proxyaddress = '77.75.127.122:41998'
    #         proxyuser = 'eclerxSMS'
    #         proxypassword = 'Tealorange447'
    #         # proxyuser = 'csimonra'
    #         # proxypassword = 'h19VA2xZ'
    #         var_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    #         'Host': 'developers.whatismybrowser.com:443'}
    #         proxyheaders = urllib3.make_headers(proxy_basic_auth=proxyuser + ':' + proxypassword)
    #         proxy = urllib3.ProxyManager('http://' + str(proxyaddress), proxy_headers=proxyheaders, ssl_version=ssl.PROTOCOL_TLSv1_2 )
    #         response = proxy.urlopen(method='GET',
    #                                  url=url,
    #                                  headers=var_headers)
    #         sourceCode = response.data
    #         htmlElem = html.document_fromstring(sourceCode)
    #         links = htmlElem.xpath('//div[@class = "useragent"]//a/text()')
    #
    #         #print(links)
    #         if not links:
    #             "List Is empty"
    #         else:
    #             p = []
    #             for link in links:
    #                 p.append(UA.dbcheckAgent(link))
    #
    #             for x in p:
    #                 if x != 'None':
    #                     UA.SaveUserAgent(ListURL, x)
    #     return "User Agents saved successfully!!!"

    def checkAgent(self,agentString):
        p = str(httpagentparser.detect(agentString, True))
        x = re.findall(r"'name': (.*?),", p)
        x = ' '.join(x)
        if 'None' not in x:
            return agentString
        else:
            return 'None'

    def SaveUserAgent(self,URLName, UserAgentName):
        agent = UserAgent()
        db = agent.GetDbConnection()
        db.UserAgents_Master.insert_one({
            "_id": int(db.system_js.getNextSequence("agentId")),
            "SourceUrl": URLName,
            "Name": UserAgentName,
            "TimeStamp": str(datetime.now()),
            "ActiveStatus": True
        })

    def SaveURL_UserAgentsData(self,domainName, UserAgentName):
         agent = UserAgent()
         db = agent.GetDbConnection()
         agent.SaveURLDomain(domainName)
         resultUserAgent = db.UserAgents_Master.find({'$and': [{'Name': UserAgentName}]},{'_id': 1})
         resultURL = db.URL_Master.find({'$and': [{'Name': domainName}]},{'_id': 1})
         UserAgentId= resultUserAgent[0]['_id']
         url_id = resultURL[0]['_id']

         resultURLCheck = db.URL_UserAgents.find({'$and': [{'URL_ID': int(url_id)},{'UserAgent': int(UserAgentId)}]})
         if resultURLCheck.count() == 0:
             db.URL_UserAgents.insert_one({
                "_id": int(db.system_js.getNextSequence("URLUserId")),
                "URL_ID": int(url_id),
                "UserAgent": int(UserAgentId),
                "TimeStamp": str(datetime.now()),
                "ActiveStatus" : True
                })
             return "Data saved succefully!"
         else:
             return "Data already present!"

    def SaveLogs(self,domainName, UserAgentName,URLStatusComments):
        agent = UserAgent()
        db = agent.GetDbConnection()
        resultUserAgent = db.UserAgents_Master.find({'$and': [{'Name': UserAgentName}]}, {'_id': 1})
        resultURL = db.URL_Master.find({'$and': [{'Name': domainName}]}, {'_id': 1})
        UserAgentId = resultUserAgent[0]['_id']
        # print(resultURL[0])
        url_id = resultURL[0]['_id']

        db.URL_UserAgents_Logs.insert_one({
            "_id": int(db.system_js.getNextSequence("LogId")),
            "URL_ID": url_id,
            "UserAgent": UserAgentId,
            "URLStatus": URLStatusComments,
            "TimeStamp": str(datetime.now())
        })

    def UpdateUserAgent(self,Name):
            agent = UserAgent()
            db = agent.GetDbConnection()
            resultAgent = db.UserAgents_Master.find({'$and': [{'Name': Name}]})

            for f in resultAgent:
                userAgentName = f['_id']

            db.UserAgents_Master.update_one({'_id': userAgentName},
            {'$set': {
            "TimeStamp": str(datetime.now()),
            "ActiveStatus": False}},upsert=False)

            db.URL_UserAgents.update_one({'UserAgent': userAgentName},
            {'$set': {
            "TimeStamp": str(datetime.now()),
            "ActiveStatus" : False}},upsert=False)
            return "User Agent deactivated!!!!"

    def GetAgent(self,domainName, comments):
        agent = UserAgent()
        db = agent.GetDbConnection()
        userAgentName = ''#newly added
        resultUAdata = db.UserAgents_Master.find({'ActiveStatus': {'$eq': True}})
        # resultUAdata = db.UserAgents_Master.find()
        resultUserAgentId = db.URL_UserAgents.aggregate([
            {'$match': {'ActiveStatus' : True}},
            {'$group':{"_id": "$UserAgent", "total_num": { '$sum': 1}}},
            {"$sort": {"total_num": 1, "_id": 1}}
        ]);
        uagentMasterList=[]
        for val1 in resultUAdata:
            uagentMasterList.append(val1['_id'])

        agentList=[]
        for val in resultUserAgentId:
            agentList.append(val['_id'])

        T = set(uagentMasterList) - set(agentList)
        if len(list(T)) !=0:
            Tval = list(T)[0]
            # resultAgent = db.UserAgents_Master.find({'$and': [{'_id': int(Tval)}, {'ActiveStatus': True}]})
            resultAgent = db.UserAgents_Master.find({'$and': [{'_id': int(Tval)}]})
            for f in resultAgent:
                userAgentName = f['Name']
        else:
            counter = 0
            for i in agentList:
                userAgentId = i
                # resultUserAgent = db.UserAgents_Master.find({'$and':[{'_id':int(userAgentId)},{'ActiveStatus':True}]},{'Name': 1})
                resultUserAgent = db.UserAgents_Master.find({'$and': [{'_id': int(userAgentId)}, {'ActiveStatus': True}]})
                if resultUserAgent.count() != 0:
                    for k in resultUserAgent:
                        userAgentName = k['Name']
                        counter = counter + 1
                        break

                    break
                else:
                    counter = counter+1

        if domainName is not None and userAgentName is not None:
            agent.SaveURL_UserAgentsData(domainName,userAgentName)
            agent.SaveLogs(domainName,userAgentName,comments)

        if domainName:
            agent.SaveURLDomain(domainName)
        return userAgentName

    def urlMaster(self): #run
        ListURL = ["www.akizuki.jp.com","http://www.all-batteries.de","http://www.all-batteries.es","http://www.all-batteries.fr","http://www.all-batteries.it","http://www.allbatteries.co.uk","www.amazon.co.uk","https://www.amazon.de","http://www.arco.co.uk","http://www.automation24.de","http://www.automation24.co.uk","https://www.avnet.com","https://www.buckandhickman.com/","www.buerklin.com","https://www.carltonbates.com","http://www.chip1stop.com/web/USA/en/","www.conrad.it","http://www.conrad.biz/ce/de/","http://www.conrad.fr/","http://business.conrad.it","http://www.conrad-electronic.co.uk/ce/","http://datatec.de/","http://www.digikey.com.au/","http://www.digikey.cn","http://www.digikey.de/","www.digikey.jp.com","http://www.digikey.sg/","http://www.digikey.co.uk/","http://www.digikey.com/","https://www.distrelec.com","www.distrelec.se","www.distrelec.de","http://www.elfadistrelec.dk","http://www.elfadistrelec.fi","http://www.distrelec.it/","http://www.elfadistrelec.no","https://www.elfaelektronika.pl","http://www.west-l.ru","https://www.elfa.se","www.esy.de","at.farnell.com","http://au.element14.com","http://be.farnell.com/","http://cn.element14.com","http://de.farnell.com","dk.farnell.com","http://es.farnell.com/","http://fr.farnell.com","hk.element14.com","http://hu.farnell.com/","http://in.element14.com","http://it.farnell.com/","http://my.element14.com","nl.farnell.com","http://no.farnell.com","ph.element14.com","pl.farnell.com","ru.farnell.com","http://se.farnell.com/","http://sg.element14.com/","th.element14.com","http://tr.farnell.com","http://tw.element14.com/","http://uk.farnell.com","www.farnell.com/","http://express.co.za/","http://item.grainger.cn/","www.heilind.com","www.isswww.uk","http://www.kempstoncontrols.co.uk","https://www.mabeo-direct.com","http://www.misco.co.uk","http://jp.misumi-ec.com/","http://www.monotaro.com/s/c-123413/","www.mouser.au","http://cn.mouser.com/","http://www.mouser.de","http://hu.mouser.com/","http://www.mouser.co.in","http://www.mouser.jp/","www.mouser.pl","http://www.mouser.sg","http://www.mouser.co.uk/","http://www.mouser.com/","www.mouser.co.za","www.omnical.com","https://www.orexad.com/","https://www.orexad.com/","www.parmley.co.uk","https://www.pcworldbusiness.co.uk","www.reichelt.de","https://www.scan.co.uk","http://www.scatts.co.uk","http://techno.com.my/online/","http://www.test4less.co.uk","www.tme.de","www.tme.eu","http://www.dq-fx.com","www.zyd.com"]
        for urlName in ListURL:
           UserAgent.SaveURLDomain(urlName)

    def SaveURLDomain(self,urlName):
         agent = UserAgent()
         db = agent.GetDbConnection()
         resultURL = db.URL_Master.find({'$and': [{'Name': urlName}]})
         if resultURL.count() == 0:
             db.URL_Master.insert_one({
                 "_id": int(db.system_js.getNextSequence("UrlId")),
                 "Name": urlName,
                 "Status": True,
                 "TimeStamp": str(datetime.now())
                 })
             resultMesaage = "URL saved successfully!"
             return resultMesaage
         else:
             resultMesaage = "URL already present in the table!"
             return resultMesaage


# p = UserAgent.GetAgent('','http://www.mouser.com/','comments')
# print(p)
# p = UserAgent.UpdateUserAgent('','')
# p= UserAgent.CrawleUserAgents1("")
# print(p)
# s = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1;   .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)"
# #print (httpagentparser.simple_detect(s))
# #print (httpagentparser.detect(s))
# result = UserAgent.UpdateUserAgent('','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0')
# print(result)
