import re
from urllib import robotparser
from urllib.parse import urljoin
import requests
import Response
import datetime
import traceback
from lxml import etree,html
import abc
from GetProducts import *
import traceback


class ScrapperBase:
    '''
    Created on: 23-03-2018
    Created by: Anil Asnani and Sweety Bhatia
    '''
    def __init__(self,RequestData):
        print ('RequestInputs-------',RequestData)
        self.requestUrl = RequestData['RequestInput']['RequestUrl']
        self.domain = RequestData['DomainName']
        self.country = RequestData['Country']
        self.IsPreview = "No"
        self.Error = '0'
        self.result = []
        self.totalResponses = 0
        self.proxyserver = ''
        self.proxyuser = ''
        self.proxyport = ''
        self.htmlElem = ''
        self.SubRequestId = RequestData['SubRequestId']
        self.url = RequestData['RequestInput']['RequestUrl']
        '''Calling User Agent'''

        self.userAgent = Response.GetUserAgent(self.domain)  #'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'


        self.headers = {'User-Agent': self.userAgent.strip()}
        self.status = ""
        # self.headers = None


    def getProductCrawl(self,num_retries=3, proxy_retries = 3):
        '''for a url it retruns dictionary containing html,number of retries,proxylist used,status of crawl etc.'''
        '''proxyused contains list of proxy used for the crawl'''
        print ('UserAgent--',self.userAgent)
        proxyUsed = []
        '''Default values for dictionary to return'''
        dictResult = {
            "domainName": self.domain,
            "response": '',
            "sourceUrl": self.requestUrl,
            "proxyCountry": self.country,
            "proxyAddress": self.proxyserver,
            "proxyPort": self.proxyport,
            "proxyUsername": self.proxyuser,
            "status": "",
            "Error": '',
            "IsCategory": "No",
            "IsPreview": self.IsPreview
        }
        '''proxy_retries saves the number of times we failed to hit the page due to proxy blockage'''
        try:
            if proxy_retries:
                '''Calling getproxy service that returns ip,port,username and password'''

                jsondata = Response.GetProxy(self.domain, self.country)

                '''Checking if getProxy service does not return any data'''
                if (jsondata == False or jsondata['IP'] == None or jsondata['IP'] == ""):
                    dictResult['Error'] = 'Stop Crawling. Proxy not available'
                    self.status = 'Stop Crawling. Proxy not available'
                    # Alternate service call
                    return dictResult
                   #Alternate service call

                else:
                    '''Assigning values from getProxy'''
                    self.proxyserver = str(jsondata['IP'])
                    self.proxyport = str(jsondata['port'])
                    self.proxyaddress = self.proxyserver + ':' + self.proxyport
                    self.proxyuser = jsondata['UserName']
                    self.proxypassword = jsondata['Password']

            '''Setting the proxy for the page'''
            proxies = {"http": 'http://' + self.proxyuser + ':' + self.proxypassword + '@' + self.proxyaddress+'/'}
            '''Downloading the page'''
            try:
                resp = requests.get(self.requestUrl, headers=self.headers, proxies=proxies,timeout=10)
            except requests.exceptions.RequestException as e:
                dictResult['Error'] = str(e)
                self.htmlElem = None
                self.status = 'Timeout Error'
                proxy_retries = proxy_retries - 1
                proxyUsed.append(self.proxyserver + ':' + self.proxyport + '-Proxy Blocked')
                Response.SaveProxyDetails(self.domain, self.proxyserver, self.proxyport, self.proxyuser, 'Blocked',
                                          self.country, 'Europe', '1')
                if proxy_retries:

                    # self.requestUrl=self.requestUrl.replace('/' + str(lastPage),'')
                    return self.getProductCrawl(num_retries, proxy_retries)
                else:
                    dictResult["ProxiesUsed"] = proxyUsed
                    dictResult["ProxyAttempts"] = len(proxyUsed)
                    dictResult['ServerAttempts'] = 3 - int(num_retries)
                    dictResult['status'] = self.status
                    return dictResult
            # self.htmlElem = resp.text
            '''Check for status codes'''
            if resp.status_code >= 400:
                self.htmlElem = None
                '''Check if there is any server error'''
                if num_retries and 500 >= resp.status_code < 600:
                    num_retries = num_retries - 1
                    self.status = 'Server Error'
                    '''Check if there is any proxy blockage'''
                elif (proxy_retries and resp.status_code < 500):
                    proxy_retries = proxy_retries - 1
                    '''Craeting a list of proxies that are blocked'''
                    proxyUsed.append(self.proxyserver + ':' + self.proxyport + '-Proxy Blocked')
                    TimeStamp = datetime.datetime.now()
                    '''Calling saveproxyDetailsService that maintains the list of proxy used'''
                    Response.SaveProxyDetails(self.domain, self.proxyserver, self.proxyport, self.proxyuser,'Blocked', self.country, 'Europe', '1')
                    self.status = 'PNF'
                return self.getProductCrawl(num_retries ,proxy_retries)
            else:
                self.htmlElem = resp.text
                '''if there there is no server error and proxy blockage it will be proceeded here'''
                res = self.getPNFStatus(self.htmlElem)
                if res == 'PNF':
                    dictResult['Error'] = 'PNF'
                    self.htmlElem = None
                    self.status = 'PNF'
                    proxy_retries = proxy_retries - 1
                    proxyUsed.append(self.proxyserver + ':' + self.proxyport + '-Proxy Blocked')
                    Response.SaveProxyDetails(self.domain, self.proxyserver, self.proxyport, self.proxyuser,
                                              'Blocked',
                                              self.country, 'Europe', '1')
                    if proxy_retries:
                        # self.requestUrl = self.requestUrl.replace('/' + str(lastPage), '')
                        return self.getProductCrawl(num_retries, proxy_retries)
                    else:
                        dictResult["ProxiesUsed"] = proxyUsed
                        dictResult["ProxyAttempts"] = len(proxyUsed)
                        dictResult['ServerAttempts'] = 3 - int(num_retries)
                        dictResult['status'] = self.status
                        return dictResult

                '''Contains list of proxies that were used and its status'''
                proxyUsed.append(self.proxyserver + ':' + self.proxyport + '-Proxy Success')


                TimeStamp = datetime.datetime.now()
                Response.SaveProxyDetails(self.domain, self.proxyserver, self.proxyport, self.proxyuser,'UnBlocked', self.country, 'Europe', '1')
                self.status = 'Success'
        except Exception as e:
            dictResult['Error'] = traceback.format_exc()
            self.htmlElem = None
            self.status = 'Error'

        dictResult['response'] = self.htmlElem
        dictResult["ProxiesUsed"] =  proxyUsed
        dictResult["ProxyAttempts"] = len(proxyUsed)
        dictResult['ServerAttempts'] = 3 - (num_retries)
        dictResult['status'] = self.status
        dictResult["proxyAddress"] = self.proxyserver,
        dictResult["proxyPort"] = self.proxyport,
        dictResult["proxyUsername"] = self.proxyuser
        return dictResult

    def getCategoryCrawl(self,num_retries=3, proxy_retries = 3,lastPage = 1,totalResponses=0,result = None,isPreview="No"):
        '''This method takes input as url and output is the dictionary containing list of product url,total number of product url,status,proxyused etc'''
        print ('%%%%%%%%%%%%%%%%%%------',self.requestUrl)
        self.requestUrl = self.url
        proxyUsed = []
        result = result or list()
        '''Default values for dictionary to return'''
        dictResult = {
            "domainName": self.domain,
            "response": '',
            "sourceUrl": self.requestUrl,
            "totalResponse": 0,
            "proxyCountry": self.country,
            "proxyAddress": self.proxyserver,
            "proxyPort": self.proxyport,
            "proxyUsername": self.proxyuser,
            "status": "",
            "Error": '',
            "IsCategory": "Yes",
            "IsPreview": self.IsPreview
        }

        '''proxy_retries saves the number of times we failed to hit the page due to proxy blockage'''
        if lastPage:
            if proxy_retries:

                '''Calling getproxy service that returns ip,port,username and password'''
                jsondata = Response.GetProxy(self.domain, self.country)

                '''Checking if getProxy service does not return any data'''
                if (jsondata == False or jsondata['IP'] == None or jsondata['IP'] == ""):
                    dictResult['Error'] = 'Stop Crawling. Proxy not available'
                    self.status = 'Stop Crawling. Proxy not available'
                    # Alternate service call
                    return dictResult
                else:
                    '''Assigning values from getProxy'''
                    self.proxyserver = str(jsondata['IP'])
                    self.proxyport = str(jsondata['port'])
                    self.proxyaddress = self.proxyserver + ':' + self.proxyport
                    self.proxyuser = jsondata['UserName']
                    self.proxypassword = jsondata['Password']
                    # self.proxyserver = '103.4.19.223'
                    # self.proxyport = '80'
                    # self.proxyaddress = self.proxyserver + ':' + self.proxyport
                    # self.proxyuser = 'prx110'
                    # self.proxypassword = 'lzPGXuZ3aV'
            try:
                '''Setting the proxy for the page'''
                proxies = {
                    "http": 'http://' + self.proxyuser + ':' + self.proxypassword + '@' + self.proxyaddress + '/'}

                # paginationStr = PaginationString.get(self.domain)


                # self.requestUrl = self.requestUrl + paginationStr + str(lastPage)
                self.requestUrl = self.requestUrl.replace('/prl/results', '/prl/results/' + str(lastPage))

                previousPage =lastPage

                '''Downloading the page'''
                try:
                    resp = requests.get(self.requestUrl, headers=self.headers, proxies=proxies, timeout=100)


                except requests.exceptions.RequestException as e:

                    dictResult['Error'] = str(e)
                    self.htmlElem = None
                    self.status = 'Timeout Error'
                    proxy_retries = proxy_retries - 1
                    proxyUsed.append(self.proxyserver + ':' + self.proxyport + '-Proxy Blocked')
                    Response.SaveProxyDetails(self.domain, self.proxyserver, self.proxyport, self.proxyuser, 'Blocked',
                                              self.country, 'Europe', '1')
                    if proxy_retries:

                        # self.requestUrl=self.requestUrl.replace('/' + str(lastPage),'')
                        return self.getCategoryCrawl(num_retries, proxy_retries, lastPage, totalResponses, result)
                    else:
                        dictResult["ProxiesUsed"] = proxyUsed
                        dictResult["ProxyAttempts"] = len(proxyUsed)
                        dictResult['ServerAttempts'] = 3 - int(num_retries)
                        dictResult['status'] = self.status
                        dictResult['totalResponse'] = len(result)
                        return dictResult
                '''Check for status codes'''
                if resp.status_code >= 400:
                    self.htmlElem = None
                    '''Check if there is any server error'''
                    if num_retries and 500 <= resp.status_code < 600:
                        num_retries = num_retries - 1
                        self.status = 'Server Error'
                        '''Check if there is any proxy blockage'''
                    elif (proxy_retries and resp.status_code < 500):
                        proxy_retries = proxy_retries - 1
                        '''Creating a list of proxies that are blocked'''
                        proxyUsed.append(self.proxyserver + ':' + self.proxyport + '-Proxy Blocked')
                        TimeStamp = datetime.datetime.now()
                        '''Calling saveproxyDetailsService that maintains the list of proxy used'''
                        Response.SaveProxyDetails(self.domain, self.proxyserver, self.proxyport, self.proxyuser,'Blocked', self.country, 'Europe', '1')
                        self.status = 'PNF'
                    # self.requestUrl = self.requestUrl.replace('/' + str(lastPage), '')
                    return self.getCategoryCrawl(num_retries, proxy_retries, lastPage, totalResponses, result)
                else:
                    '''if there there is no server error and proxy blockage it will be proceeded here'''
                    '''Contains list of proxies that were used and its status'''
                    proxyUsed.append(self.proxyserver + ':' + self.proxyport + '-Proxy Success')
                    self.htmlElem = resp.text

                    res=self.getPNFStatus(self.htmlElem)
                    if res=='PNF':
                        dictResult['Error'] = 'PNF'
                        self.htmlElem = None
                        self.status = 'PNF'
                        proxy_retries = proxy_retries - 1
                        proxyUsed.append(self.proxyserver + ':' + self.proxyport + '-Proxy Blocked')
                        Response.SaveProxyDetails(self.domain, self.proxyserver, self.proxyport, self.proxyuser,
                                                  'Blocked',
                                                  self.country, 'Europe', '1')
                        if proxy_retries:
                            # self.requestUrl = self.requestUrl.replace('/' + str(lastPage), '')
                            return self.getCategoryCrawl(num_retries, proxy_retries, lastPage, totalResponses, result)
                        else:
                            dictResult["ProxiesUsed"] = proxyUsed
                            dictResult["ProxyAttempts"] = len(proxyUsed)
                            dictResult['ServerAttempts'] = 3 - int(num_retries)
                            dictResult['status'] = self.status
                            dictResult['totalResponse'] = len(result)
                            return dictResult
                    else:
                        # htmlElem = html.document_fromstring(resp.text)
                        # txt = etree.tostring(htmlElem, pretty_print=True)


                        tree = html.fromstring(self.htmlElem)
                        if (lastPage == 1):
                            '''Getting last page for navigation'''
                            lastPage = int(self.getLastPage(tree))
                            lastPage = lastPage + 1
                        '''Getting all the products using lxml'''

                        product_xpath = ProductXpath.get(self.domain)
                        ProductList = tree.xpath(product_xpath)
                        '''Adding total number of product urls for page'''
                        totalResponses = totalResponses + len(ProductList)
                        result.extend(ProductList)
                        TimeStamp = datetime.datetime.now()
                        Response.SaveProxyDetails(self.domain, self.proxyserver, self.proxyport, self.proxyuser,'UnBlocked', self.country, 'Europe', '1')
                        self.status = 'Success'


                lastPage = lastPage - 1
                if (self.domain.find('mouser') != -1):
                    lastPage = lastPage * 25
                if (lastPage != 1 and isPreview == "No"):
                    # self.requestUrl = self.requestUrl.replace('/' + str(previousPage), '')
                    return self.getCategoryCrawl(num_retries, proxy_retries, lastPage,totalResponses,result)
            except Exception as e:
                dictResult['Error'] = traceback.format_exc()
                self.htmlElem = None
                self.status = 'Error'


        dictResult['response'] = result
        dictResult["ProxiesUsed"] = proxyUsed
        dictResult["ProxyAttempts"] = len(proxyUsed)
        dictResult['ServerAttempts'] = 3 - int(num_retries)
        dictResult['status'] = self.status
        dictResult['totalResponse'] = len(result)
        return dictResult


    @abc.abstractmethod
    def getLastPage(self,tree):
        pass
    @abc.abstractmethod
    def getPNFStatus(self, htmlElements):
        pass
        '''
        PNF And Access Denied Check Code
        '''





