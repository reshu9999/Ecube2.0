import re
from urllib import robotparser
from urllib.parse import urljoin
import requests
from Response import *
import datetime
import traceback
from lxml import etree,html
from Scrapper import ScrapperBase
# from bs4 import Beautifulsoup


class ScrapperFarnellPython_AU(ScrapperBase):
    '''
    Created on: 23-03-2018
    Created by: Anil Asnani and Sweety Bhatia
    '''
    def __init__(self,RequestData):
        super().__init__(RequestData)

    def getLastPage(self, tree):
        listPages = []
        result = tree.xpath('//span[contains(@class,"pageLink")]//a/text()')
        print(result)
        listPages = []
        for item in result:
            if (str(item).isdigit()):
                listPages.append(int(item))
        print('List', listPages)
        if len(listPages) == 0:
            return '1';
        else:
            return max(listPages)

    def getPNFStatus(self, tree):
        tree = html.document_fromstring(tree)
        '''
        PNF And Access Denied Check Code
        '''
        print("HTML Source Page", tree)
        try:
            data = tree.xpath('//meta[1]/@name')[0].strip()
            if data.lower() == "robots":
                return "PNF"
        except Exception as e:
            pass
        try:
            data = tree.xpath('//p[1]/text()')[0].strip()

            if data.find("Access Denied") != -1:
                return "Access Denied"
        except Exception as e:
            pass
        try:
            data = tree.xpath('//title[0]/text()')[0].strip()

            if data == "Access Denied":
                return "Access Denied"
        except Exception as e:
            pass

# x = ScrapperFarnellPython_AU("http://au.element14.com/w/search/prl/results?brand=aavid-thermalloy&pageSize=100","au.element14.com", "Australia", "No", "1")
# y = x.getCategoryCrawl()
# print ('Result',y)








