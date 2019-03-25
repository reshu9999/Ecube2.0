
from flask import Flask, request,jsonify
from Common.HtmlResourceFile import HtmlResourceFile
from Common.CustomResponse import CustomResponse
from Common.getProxyrotation import getProxyrotation
from flaskext.mysql import MySQL
from dicttoxml import dicttoxml
import os
import json
import requests
import traceback
from pdb import set_trace as st


reportPath = 'http://www.ecube2.com/website/report/'


from Common.config_coordinator import config_fetcher

mysql_config = config_fetcher.get_mysql_config
redis_config = config_fetcher.get_redis_config

mysql = MySQL()
app = Flask(__name__)
app.secret_key=os.urandom(24)
app.config['MYSQL_DATABASE_USER'] = mysql_config['USER']
app.config['MYSQL_DATABASE_PASSWORD'] = mysql_config['PASSWORD']
app.config['MYSQL_DATABASE_DB'] = mysql_config['DB']
app.config['MYSQL_DATABASE_HOST'] = mysql_config['HOST']
mysql.init_app(app)


@app.after_request
def add_header(response):
    response.headers.add('Access-Control-Allow-Origin','*')
    response.headers.add('Access-Control-Allow-Headers','Content-Type-Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response


@app.route('/api/v1/saveHtml',methods = ['POST'])
def SaveHtml():
    content = request.get_json()
    objHRF = HtmlResourceFile()
    sourceHtml = content['sourceHtml']
    sourceUrl = content['sourceUrl']

    data = objHRF.SaveData(sourceHtml, sourceUrl)
    # result = CustomResponse.CustomAPIResponse(data)
    return data

@app.route('/api/v1/SaveSourceHtml',methods = ['POST'])
def SaveSourceHtml():
    try:
        print('Calling Method')

        content = request.get_json()
        print(content)
        objHRF = HtmlResourceFile()
        data = objHRF.SaveSourceData(content)
    except Exception as e:
        traceback.print_exc()
        return jsonify({'StatusCode': 500, 'ResultData': request.get_json()})
    else:
        return jsonify({'StatusCode': 200, 'ResultData': data})


@app.route('/api/v1/getProxy', methods = ['GET'])
def getProxy():
    domain = request.args.get('domain')
    country = request.args.get('country') or None

    PR = getProxyrotation()
    proxyrotation = PR.GetProxyData(domain,country)
    prjsonresult=jsonify(proxyrotation)
    return prjsonresult


# def SaveSourceHtml():
#     try:
#         content = request.get_json()
#         objHRF = HtmlResourceFile()
#         requestId = content['requestId']
#         subRequestId = content['subRequestId']
#         domainName = content['domainName']
#         sourceHtml = content['response']
#         totalResponse = content['totalResponse']
#         sourceUrl = content['sourceUrl']
#         pythonScriptName = content['pythonScriptName']
#         startDT = content['startDT']
#         endDT = content['endDT']
#         proxyCountry = content['proxyCountry']
#         proxyAddress = content['proxyAddress']
#         proxyPort = content['proxyPort']
#         proxyUsername = content['proxyUsername']
#         status = content['status']
#         data = objHRF.SaveSourceData(requestId, subRequestId, domainName, sourceHtml, totalResponse, sourceUrl, pythonScriptName,
#                                      startDT, endDT, proxyCountry, proxyAddress, proxyPort, proxyUsername, status)
#     except:
#         return jsonify({'StatusCode': 500, 'ResultData': None})
#     else:
#         return jsonify({'StatusCode': 200, 'ResultData': data})


# @app.route('/api/v1/getHtml',methods = ['POST'])
# def GetHtmlByUrl():
#     content = request.get_json()
#     objHRF = HtmlResourceFile()
#     url = content['URL']
#     data = objHRF.FindByUrl(url)
#
#     # result = CustomResponse.CustomAPIResponse(data)
#     return jsonify(data)

@app.route('/api/v1/GetHtml',methods = ['GET'])
def GetHtmlById():
    requestId = request.args.get('requestId')
    objHRF = HtmlResourceFile()
    data = objHRF.FindHTMLById(requestId)

    # result = CustomResponse.CustomAPIResponse(data)
    return jsonify({'StatusCode': 200,'ResultData': data})

@app.route('/api/v1/GetDomainHeader', methods = ['GET']) #not in use
def GetDomainHeader():
    domainName = request.args.get('domainName')
    cur = mysql.connect().cursor()
    try:
        cur.callproc('GetDomainHeader', [domainName])
        r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
    except (MySQL.Error, MySQL.Warning) as e:
        return jsonify({'StatusCode': 500, 'ResultData': None})
    except TypeError as e:
        return jsonify({'StatusCode': 500, 'ResultData': None})
    return jsonify({'StatusCode': 200,'ResultData' : r})


@app.route('/api/v1/GetCrawledDataMapper', methods = ['GET'])
def GetCrawledDataMapper():
    requestId = request.args.get('requestId')
    cur = mysql.connect().cursor()
    try:
        cur.callproc('GetCrawlDataMapper', [int(requestId)])

        r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        print(r)
    except (MySQL.Error, MySQL.Warning) as e:
        return jsonify({'StatusCode': 500, 'ResultData': None})
    except TypeError as e:
        return jsonify({'StatusCode': 500, 'ResultData': None})
    except Exception as e:
        return jsonify({'StatusCode': 500, 'ResultData': None})
    # return "Hello"
    return jsonify({'StatusCode': 200,'ResultData' : r})


@app.route('/api/v1/GetProductHTML', methods = ['POST'])
def GetProductHTML():
    res = request.get_json(force = True)
    requestId = res['RequestId']
    subRequestId = res['SubRequestId']
    requestUrl = res['RequestUrl']
    domainName = res['DomainName']
    proxyCountry = res['ProxyCountry']
    pythonScriptName = res['PythonScriptName']
    objHRF = HtmlResourceFile()
    if res:
        #Get Proxy
        objProxy = objHRF.GetProxy(domainName, proxyCountry) #Call Proxy Service

        #Get Header
        if domainName:
            resultHeader = objHRF.GetHeader(domainName) #Call Header Service
        htmlText = objHRF.GetSourceHtml(resultHeader, requestUrl, objProxy) #Call HTML Request Method

        result = objHRF.SaveSourceData(requestId, subRequestId, domainName, htmlText, '1', requestUrl, pythonScriptName,
                                     '', '',proxyCountry, objProxy.address, objProxy.port, objProxy.username, 'Pending')
        return jsonify({'StatusCode': 200,'ResultData' : result})
    else:
        return jsonify({'StatusCode': 200, 'ResultData': "Empty"})

@app.route('/api/v1/SaveResponseData', methods=['POST'])
def SaveResponseData():
    res = request.get_json(force=True)
    objHRF = HtmlResourceFile()
    conn = mysql.connect()
    cur = conn.cursor()
    if res:
        category = res['IsCategory']
        if 'Yes' in category:
            listProductUrl = res['response']
            for url in listProductUrl:
                res['response'] = url
                args = objHRF.GetCrawlArgs(**res)
                cur.callproc('sp_SaveCrawlRequestDetail', args)
                cur.callproc('sp_UpdateRequestRunDetail',
                         [res['status'], int(res['requestId']), int(res['subRequestId'])])
                conn.commit()
        else:
             objHRF.SaveCrawlData(res)
             cur.callproc('sp_UpdateRequestRunDetail',
                     [res['status'], int(res['requestId']), int(res['subRequestId'])])
             conn.commit()
        return jsonify({'StatusCode': 200, 'ResultData': "Saved Successfully"})
    else:
        return jsonify({'StatusCode': 200, 'ResultData': "No Data Found"})

@app.route('/api/v1/StartCrawl', methods=['GET'])
def StartCrawl():
    requestId = request.args.get('requestId')
    requestModeId = request.args.get('requestModeId')
    print ('vikash ')
    conn = mysql.connect()
    cur = conn.cursor()
    try:
        cur.callproc('sp_SaveRequestRunDetail', [int(requestId), int(requestModeId), None])
        conn.commit()
        
        cur = conn.cursor()
        cur.execute(
            """
            select RequestId ,RequestName, CreatedBy, UserName,EmailID from tbl_RequestMaster as r 
            inner join tbl_UserMaster  as u  on r.CreatedBy = u.UserId where  RequestId = """+requestId+""" ; 
            """
        )
        sp_res = cur.fetchall()
        cur.close()
       
        body = '''
        
            
            <style type="text/css">
            p.MsoNormal, li.MsoNormal, div.MsoNormal  {
                margin: 0in;
            margin:bottom:.0001pt;
            font:size:11.0pt;
            font:family:"Verdana", "sans:serif";
            }
            a:link, span.MsoHyperlink  {
            mso:style:priority:99;
            color:blue;
            text:decoration:underline;
            }
            a:visited, span.MsoHyperlinkFollowed  {
            mso:style:priority:99;
            color:purple;
            text:decoration:underline;
            }
            span.EmailStyle17  {
            mso:style:type:personal;
            font:family:"Verdana", "sans:serif";
            color:windowtext;
            }
            span.EmailStyle18  {
            mso:style:type:personal:reply;
            font:family:"Verdana", "sans:serif";
            color:#1F497D;
            }
            .MsoChpDefault  {
            mso:style:type:export:only;
            font:size:10.0pt;
            }
            @page Section1  {
                size: 8.5in 11.0in;
            margin:1.0in 1.0in 1.0in 1.0in;
            }
            div.Section1  {
                page: Section1;
            }
            table  {
            border:collapse:collapse;
            width :800px;
            
            }
            table, td, th  {
            border:1px solid black;
            
            }
            
            </style>
            
            <div style="font-family: verdana; font-size:12px; line-height: 18px;"> 
            <p style="font-family: verdana; ">    Dear User,   <br><br>  Following request has been initiated  </p> 
                
                <br>
                <table width="60%" border="0" cellspacing="0" cellpadding="10" style="border-collapse: collapse; border:1px solid #999; font-size: 12px; text-align: left;">
            <tbody>
                <tr>
		<th style="background:#365f91; color: #fff; text-align: left;"> Request Id  </th>
                <th style="background:#365f91; color: #fff; text-align: left;"> Request Name </th>
                <th style="background:#365f91; color: #fff; text-align: left;"> User Name </th>
                </tr>
                <tr>
		<td> '''+str(sp_res[0][0])+'''  </td>
                <td> '''+str(sp_res[0][1])+'''  </td>
                <td> '''+str(sp_res[0][3])+'''   </td>
                </tr>
            </tbody>
            </table>
            
            <br>
                    <p>          Regards,<br>
                    PricingTech<br>
                    <br><br></p>
                    <p>This message including attachment(s) is intended only for the personal and confidential use of the recipient(s) named above.This communication is for informational purposes only.Email transmission cannot be guaranteed to be secure or error-free.
                       All information is subject to change without notice. If you are not the intended recipient of this message you are hereby notified that any review, dissemination, distribution or copying of this message is strictly prohibited. If you are not the
                       intended recipient, please contact:<a href="mailto:helpdesk@eclerx.com">helpdesk@eclerx.com</a><br><br>
                    </p>
                    <p>
                        <font size="3pt" color="black" family="Tahoma"><strong>© 2016.eClerx Services Ltd. An ISO/IEC 27001:2013 Company</strong></font>
                    </p>
            </div>
        '''
       
        #body =body.replace('-',' ')
       
        
        dict1 = {}
        dict1 = {"cc": "PricingTech@eclerx.com", "to": sp_res[0][4], "bcc": "PricingTech@eclerx.com", "body": body,
                "subject": "eCube 2.0 - Request ("+str(sp_res[0][1])+") Initiated   ", "has_attachments": False}
        mail_args = json.dumps(dict1)      
        resp = requests.post('http://192.168.8.20/mail/api/v1/send_email/', data=mail_args)
        
    except Exception as e:
        return jsonify({'StatusCode': 500, 'ResultData': str(e)})
    return jsonify({'StatusCode': 200, 'ResultData': "Saved Successfully"})
@app.route('/api/v1/StartReport', methods=['GET'])
def StartReport():
    requestRunId = request.args.get('requestRunId')
    userId = request.args.get('userId')

    conn = mysql.connect()
    cur = conn.cursor()
    try:
        cur.callproc('sp_SaveReportRunDetail', [int(requestRunId), int(userId)])
        conn.commit()
    except (MySQL.Error, MySQL.Warning) as e:
        return jsonify({'StatusCode': 500, 'ResultData': None})
    except TypeError as e:
        return jsonify({'StatusCode': 500, 'ResultData': None})
    return jsonify({'StatusCode': 200, 'ResultData': "Saved Successfully"})

@app.route('/api/v1/GenerateReport', methods=['GET'])
def GenerateReport():
    requestRunId = request.args.get('requestRunId')
    objHRF = HtmlResourceFile()
    conn = mysql.connect()
    cur = conn.cursor()
    try:
        cur.callproc('sp_UpdateReportStatus', [int(requestRunId), 'WIP'])
        r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        if r[0]['ReportName'] is not None:
            reportName = r[0]['ReportName'] + '.csv'
        else:
            reportName = 'CrawlReport.csv'
        conn.commit()
        # Fetch Crawl Response
        resulData = objHRF.GetCrawlResponse(requestRunId)
        # Fetch Crawl Response End

        # CSV Creation
        objHRF.CreateCSVReport(resulData, reportName)
        # CSV Creation End

        # Download Link
        cur.callproc('sp_UpdateReportLink', [int(requestRunId), reportPath + reportName])
        conn.commit()
        # Download Link End

        cur.callproc('sp_UpdateReportStatus', [int(requestRunId), 'Completed'])
        conn.commit()
    except (MySQL.Error, MySQL.Warning) as e:
        return jsonify({'StatusCode': 500, 'ResultData': None})
    except TypeError as e:
        return jsonify({'StatusCode': 500, 'ResultData': None})
    return jsonify({'StatusCode': 200, 'ResultData': "Report Created Successfully"})

@app.route('/api/v1/GetCrawledResponse',methods = ['GET'])
def GetCrawledResponse():
    requestId = request.args.get('requestId')
    objHRF = HtmlResourceFile()
    data = objHRF.GetCrawledResponseByRequest(requestId)
    return jsonify({'StatusCode': 200,'ResultData': data})


@app.route('/api/v1/GetMatchingHotels',methods = ['GET'])
def GetMatchingDLL():
    city = request.args.get('city')
    country = request.args.get('country')
    supplier = request.args.get('supplier')
    
    conn = mysql.connect()
    cur = conn.cursor()
    cur.callproc('sp_MatchingDLL', [city, country, supplier])
    result = cur.fetchall()
    response = []       
    for res in result:
        response.append({'intHotelRelationid':res[0], 'intHotelid':res[1], 'intSupplierid':res[2],
                         'nvcrSupplierName': res[3], 'nvcrHotelName': res[4], 'nvcrWebSiteHotelId': res[5],
                         'nvcrHoteladdress1': res[6], 'Comhotel': res[7], 'ComHotelAddress1': res[8],
                         'intHotelRelationComHotelId': res[9], 'ComSupplierid': res[10], 'ComSupplierName': res[11],
                         'bitHotelRelationManualMatch': res[12], 'intUsrId': res[13], 'intAdminUsrid': res[14],
                         'intCityId': res[15], 'nvcrCityName': res[16], 'intCountryid': res[17],
                         'nvcrCountryName': res[18], 'ComCityId': res[19], 'ComCityName': res[20],
                         'ComCountryId': res[21], 'ComCountryname': res[22], 'LastApperanceDate': res[23]
                         })
    
    cur.close()    
    conn.close()
    xml = dicttoxml(response, custom_root='MatchingDLL', attr_type=False)
    
    return jsonify({'StatusCode': 200,'ResultData': xml.decode('utf-8')})


@app.route('/api/v1/GetMatchingPrimaryHotels', methods=['GET'])
def GetMatchingDLLPrimaryHotels():
    city = request.args.get('city')
    country = request.args.get('country')

    conn = mysql.connect()
    cur = conn.cursor()
    cur.callproc('sp_MatchingDLL_PrimaryHotels', [country, city])
    result = cur.fetchall()
    response = []
    for res in result:
        response.append({'nvcrWebSiteHotelId': res[0], 'nvcrHotelName': res[1],
                         'nvcrHotelChain': res[2], 'nvcrContractManager': res[3]
                         })

    cur.close()
    conn.close()
    xml = dicttoxml(response, custom_root='MatchingPrimaryHotels', attr_type=False)

    return jsonify({'StatusCode': 200, 'ResultData': xml.decode('utf-8')})


@app.route('/api/v1/GetMasterMappings', methods=['GET'])
def GetMasterMappingDLL():
    city = request.args.get('city')
    country = request.args.get('country')
    supplier = request.args.get('supplier')

    conn = mysql.connect()
    cur = conn.cursor()
    cur.callproc('sp_MasterMapping', [city, country, supplier])
    result = cur.fetchall()
    response = []
    for res in result:
        response.append({'supplier': res[0], 'Destination': res[1], 'Country': res[2],
                         'MultizoneCount': res[3], 'ZoneName': res[4], 'ZoneID': res[5],
                         'ZoneType': res[6]
                         })

    cur.close()
    conn.close()
    xml = dicttoxml(response, custom_root='MasterMappingDLL', attr_type=False)

    return jsonify({'StatusCode': 200, 'ResultData': xml.decode('utf-8')})


@app.route('/api/v1/GetPreviewData', methods = ['POST'])
def GetPreviewData():

    res = request.get_json(force = True)
    if res:
        print(res)
        requestUrl = res['RequestUrl']
        domainName = res['DomainName']
        country = res['Country']
        requestId = res['RequestId']
        objHRF = HtmlResourceFile()

        #Get Scripts
        # conn = mysql.connect()
        # cur = conn.cursor()
        # cur.callproc('GetScripts', [domainName])
        # r = [dict((cur.description[i][0], value)
        #           for i, value in enumerate(row)) for row in cur.fetchall()]
        # scrappingScript = r[0]['ScrapingScriptName']
        #parsingScript = r[0]['ParsingScriptName']

        scrappingScript = 'ScrapperConradPython_IT.py'
        parsingScript = 'ConradPython_IT.py'
        scrappedData = objHRF.ProductCrawl(requestUrl,domainName,country,scrappingScript)
        print(scrappedData)
        htmlElement = scrappedData['response']['htmlElement']
        print(htmlElement)
        parsedData = objHRF.ProductParse(htmlElement,requestId,parsingScript)
        print(parsedData)
        #Get Scripts End


        return jsonify({'StatusCode': 200,'ResultData' : parsedData})
    else:
        return jsonify({'StatusCode': 500, 'ResultData': "Empty"})

# if (__name__ == '__main__'):
#     app.run(debug=True,host='0.0.0.0', port=5001)




if(__name__ == '__main__'):
    # # app.run(port=8084)
    # app.run(debug=True)
    app.run()
