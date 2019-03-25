import csv
import re
import codecs
from pdb import set_trace as st
import requests

from pymongo import  MongoClient

folderPath = '/home/tech/ManualReport/'

entries = ('_id', 'RequestId','RequestRunId','DomainName','PointOfSale','ProxyIp','ProxyUserName','ProxyPort','CategoryScrappingScript','ProductScrappingScript','ProductParsingScriptName','IsCategory','ScrapingStarttime','ScrapingEndtime','ParsingStarttime','ParsingEndtime')

class Commmon:

    def entries_to_remove(dict):
        for key in entries:
            if key in dict:
                del dict[key]
        return dict



    def CreateCSVReport(objData, filename,fieldsRequired):
        fieldsRequired.append('subRequestId')
        report_data = open(folderPath + filename, 'w', newline='')
        csvwriter = csv.writer(report_data)
        count = 0

        for data in objData:
            print("OutPut data",data)
            if count == 0:
                header = data.keys()

                csvwriter.writerow(fieldsRequired)
                count += 1

            data1=[]

            for key in fieldsRequired:
                try:
                    value=str(data[key])
                except KeyError as e:
                    value='NA'

                if '\\' in value or '->' in value:
                    while '\\' in value:
                        value=codecs.escape_decode(value)[0].decode('utf-8')
                    #value=re.sub('\s+', ' ', value)
                    value='->'.join([i for i in re.sub('\s+',' ',value).split('->') if i !=' ' if i!=''])
                if 'Category' in key:
                    value=value.replace('|','->',3)

                data1.append(str(value))

            csvwriter.writerow(data1)
        report_data.close()
        return "Report Created Successfully"


client = MongoClient('mongodb://192.168.7.134:27017/')
mongodb = client.HTMLDumps
resultData = []

# Pass  Request Run ID here
#result = mongodb.CrawlResponse.find({'RequestRunId': str(id)})
result = mongodb.CrawlResponse.find({'requestId': '465'})
#st()


for item in result:

    try:
        finaldict = Commmon.entries_to_remove(item)
        resultData.append(finaldict)
        fieldsRequired= requests.get('http://192.168.7.128/site3/api/v1/GetCrawledDataMapper?requestId='+ str(resultData[0]['requestId']))

        fieldsRequired=eval(fieldsRequired.content.decode('utf-8'))['ResultData']
        fieldsRequired=[i['TextBoxValue'] for i in fieldsRequired]
        fieldsRequired.append('RequestUrl')
        print(fieldsRequired)
    except:
        fieldsRequired = ['Category', 'ManPartDesc', 'OrderCode', 'ManPartId', 'ImgUrl', 'ManPackQty', 'UOM', 'TechnicalDataSheet', 'Specification', 'ManName', 'ComStockloc', 'NumberInStock', 'ListPrice', 'ROHs', 'MinimumQty', 'MultipleQty', 'BreakQty', 'Countryoforigin', 'tariffNo', 'Availability', 'marketid', 'Weight', 'Packaging', 'Currency', 'RequestUrl']
c1 = Commmon
c1.CreateCSVReport(resultData,"manual_465.csv",fieldsRequired)