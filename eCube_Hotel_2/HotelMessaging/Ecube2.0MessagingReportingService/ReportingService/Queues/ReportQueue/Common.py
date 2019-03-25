import csv
import re
import codecs
from pdb import set_trace as st
#folderPath = '/home/tech/Ecube2.0MessagingQueueLatest/ReportingService/Reports/'

folderPath = '/home/tech/ReportGeneration/'

entries = ('_id', 'RequestId', 'SubRequestId','RequestRunId','DomainName','PointOfSale','ProxyIp','ProxyUserName','ProxyPort','CategoryScrappingScript','ProductScrappingScript','ProductParsingScriptName','IsCategory','ScrapingStarttime','ScrapingEndtime','ParsingStarttime','ParsingEndtime')

class Commmon:

    def entries_to_remove(dict):
        for key in entries:
            if key in dict:
                del dict[key]
        return dict

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


    # def CreateCSVReport(self,objData, filename,fieldsRequired):
    #
    #     fieldsRequired.append('subRequestId')
    #     report_data = open(folderPath + filename, 'w', newline='')
    #     csvwriter = csv.writer(report_data)
    #     count = 0
    #
    #     for data in objData:
    #         #print("OutPut data",data)
    #         if count == 0:
    #             header = data.keys()
    #             #st()
    #             #csvwriter.writerow(header)
    #             csvwriter.writerow(fieldsRequired)
    #             count += 1
    #
    #         data1=[]
    #
    #         for key in fieldsRequired:
    #             try:
    #                 value=str(data[key])
    #             except KeyError as e:
    #                 value='NA'
    #
    #             if '\\' in value or '->' in value:
    #                 while '\\' in value:
    #                     value=codecs.escape_decode(value)[0].decode('utf-8')
    #                 #value=re.sub('\s+', ' ', value)
    #                 value='->'.join([i for i in re.sub('\s+',' ',value).split('->') if i !=' ' if i!=''])
    #             if 'Category' in key:
    #                 value=value.replace('|','->',3)
    #             '''
    #             if (value is not None) and ('http' not in value):
    #                 while '\\' in value:
    #                     value=codecs.escape_decode(value)[0].decode('utf-8')
    #                 value=re.sub('\W+', ' ', value)
    #             '''
    #             data1.append(str(value))
    #             #st()
    #
    #             '''
    #         for key,value in data.items():
    #             while '\\' in value:
    #                 value=codecs.escape_decode(value)[0].decode('utf-8')
    #             data[key]=value
    #             '''
    #             '''
    #             try:
    #                 data[key] = codecs.escape_decode(value.replace('\\\\r', '').replace('\\\\t', '').replace('\\\\n', '').replace('\\\\x', '\\x'))[0].decode('utf-8')
    #             except UnicodeDecodeError as e:
    #                 data[key] = codecs.escape_decode(value.replace('\\\\r', '').replace('\\\\t', '').replace('\\\\n', '').replace('\\\\x', '\\x'))[0].decode('cp1252')
    #             '''
    #             # try:
    #             #     data[key]=re.sub('\W+','',codecs.escape_decode(value)[0].decode('utf-8'))
    #             # except UnicodeDecodeError as e:
    #             #      data[key]=re.sub('\W+','',codecs.escape_decode(value)[0].decode('cp1252'))
    #             # # except Exception as e:
    #             # #     data[key]=value
    #
    #         #st()
    #         csvwriter.writerow(data1)
    #     report_data.close()
    #     return "Report Created Successfully"
