from pymongo import MongoClient
import  time
import datetime
from pdb import set_trace as st
from collections import Counter


client = MongoClient('mongodb://192.168.7.134:27017/')
mongodb = client.HTMLDumps

status=[]
#result = mongodb.HTMLRepository_sf_14032018_1908.find({'requestId':374}).count()
reqid=552
result = mongodb.PNFData.find({'requestId': reqid })
for row in result:
    st()
# print('Scrap:',result)
#result1 = mongodb.CrawlResponse.find({'requestId': reqid }).count()
#result = mongodb.HTMLRepository_sf_14032018_1908.find({'subRequestId':'197469'})
# print('Parse:',result1)
#
# for i in ['401','408']:
#     result1=mongodb.CrawlResponse.find({'requestId': i })
#     for row in result1:
#         st()

# result6 = mongodb.HTMLRepository.find({'requestId': 552}).count()
# print ('Count----',result6)
# print('result-----', result6)
# for row in result6:
#     print('Each Row', row)
        # if row['RequestUrl']=='http://cn.element14.com/1001129?ost=1001129':
#             st()
    # result1=mongodb.CrawlResponse.find({'requestId': i }).count()
    # print(i,"-->",result1)

# result1=mongodb.HTMLRepository.find({'requestId': '470' })
# for row in result1:
#     print(row['response'])

# # result=mongodb.CrawlResponse.find({'requestId': '386'})
# result=mongodb.HTMLRepository.find({'requestId': '416'}).count()
# print(result1)
# count=0
#
# for i in ['369','371','372','461','465']:
# for i in ['369','371','372','461','465']:
#     result1=mongodb.HTMLRepository.find({'requestId': i })
#     for row in result1:
#         st()

# for row in result:
#     print(row['MinimumQty'],row['tariffNo'],row['ManPartId'])
#     if row['RequestUrl']=='http://cn.element14.com/1014111?ost=1014111':
#         st()
#     # if row['Proxy Attempts']<3:
#     #     count+=1
# print(count)
#print(result)

# requestcount={}
# result = mongodb.HTMLRepository_sf_15032018_2110.find()
# for row in result:
#     #st()
#     if row['requestId'] not in requestcount.keys():
#         requestcount[row['requestId']]=1
#     else:
#         requestcount[row['requestId']] += 1
#
# print(requestcount)


# requestlist=[]
#
# statusReport={}
# for req in ['369','371','372','461','465']:
#     urllibfailed=0
#     distil_capture=0
#     success=0
#     failedothers=0
#     result = mongodb.HTMLRepository.find({'requestId': str(req)})
#     for row in result:
#         if row['response'] ==False:
#             failedothers+=1
#         elif 'urllib3.response' in row['response']:
#             urllibfailed+=1
#         elif 'distil_r_captcha.html' in row['response']:
#             distil_capture+=1
#         else:
#             #st()
#             success+=1
#             with open('SuccessCNHU.txt','a') as file:
#                 file.write(row['requestId'] + '|' + row['domainName'] + '|' + row['sourceUrl'] + '\n')
#             # print(row['response'])
#             # st()
#     print("Request Done ", str(req))
#     statusReport[str(req)]={'Sucess': success,
#                             'PNF': urllibfailed,
#                             'Distil': distil_capture,
#                             'Failed Others': failedothers}
#
# print(statusReport)

# print("Urllib Failed ", urlibfailed)
# print('Distil Capture ', distil_capture)
# print('Success', success)
#

# with open('Request_380.status','w') as  statlog:
#     for row in result:
#         st()
        # if len(row['response']['htmlElement'])<1:
        #     statlog.write( str(row['sourceUrl']) + '|' + 'NO HTML\n' )
        # elif len(row['response']['htmlElement']) >1 and len(row['response']['htmlElement']) <200:
        #     statlog.write(str(row['sourceUrl']) + '|' + 'Incomplete HTML'  +'|' + str(row['response']['htmlElement'])+ '\n')
        # else:
        #     statlog.write( str(row['sourceUrl']) + '|' + 'HTML Found\n' )

#result=mongodb.HTMLRepository.find()
# for row in result:
#     st()
# print(result)
# for row in result:
#     status.append(row['ProxyInformation'])
#
# c=Counter(status)
# print(c)

# result = mongodb.HTMLRepository.find({'requestId':'372'}).count()
# print(result)
#
# result = mongodb.HTMLRepository.find({'requestId':'371'}).count()
# print(result)
#
# result = mongodb.HTMLRepository.find({'requestId':'369'}).count()
# print(result)



# for row in result:
#     print(row)
