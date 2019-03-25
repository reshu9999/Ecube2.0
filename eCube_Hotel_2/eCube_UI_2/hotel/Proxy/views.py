from django.shortcuts import render
from hotel.master.models import DomainMaster
import pymysql
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.conf import settings
import os
from django.contrib import messages
import numpy as np
import pandas as pd
import json
import requests
from .models import ProxyMaster
from django.core.files.storage import FileSystemStorage
from hotel.utils import PandasSQLUpload

def index(request):
    domain = DomainMaster.objects.filter(active=True).values('id', 'domainname').order_by('domainname')
    dicdomain = {}
    for i in domain:
        dicdomain[i['id']] = i['domainname']
    db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                            user=settings.DATABASES['default']['USER'],
                            passwd=settings.DATABASES['default']['PASSWORD'],
                            db=settings.DATABASES['default']['NAME'])

     
        
    cur1 = db.cursor()
    query1 = """SELECT Vendor_Name FROM eCube_Centralized_DB.tbl_ProxyMaster group by Vendor_Name;
    """
    cur1.execute(query1)
    dataObj1 = cur1.fetchall()
    dataObjlist1 = []
    loop_Counter=0
    for row in dataObj1:
        loop_Counter= loop_Counter+1
        dicVendor = {}
        dicVendor[loop_Counter] = row[0]
        dataObjlist1.append(dicVendor)
    context = {
        'domain' : dicdomain ,
        'vendor' : dataObjlist1
    }
    return render(request, 'hotel/Proxy/index.html',context)


@csrf_exempt
def download_proxy(request):
    if request.method == 'POST' or request.is_ajax():
        domainid = request.POST['domain_id']
        domainname = request.POST['domain_name']
        #proxydetails = sp_get_by_param('sp_GetProxyByDomain', [int(domainid)])
        conn = PandasSQLUpload.get_engine()
        file_path = 'Proxy/' + domainname + '.csv'
        query = 'SELECT `ProxyName`,`ProxyPort`,`ProxyUserName`,`ProxyPassword`,' \
                '`ProxyTypeName` as ProxyType, `CountryName`,`RegionId`,'\
                '`Vendor_Name` as VendorName,`nvcrCountryName` as POS,`PageType` FROM tbl_proxysummary_details_New pd' \
                ' inner join tbl_ProxyMaster pm on pd.Proxy_Id = pm.ProxyMasterId' \
                ' left join tbl_CountryMaster cm on pd.Country_Id=cm.CountryID' \
                ' left join PointOfSale ps on pm.POS=ps.intCountryId'\
                ' left join tbl_ProxyTypeMaster ptm on pd.ProxyTypeId=ptm.ProxyTypeId' \
                ' where pd.Domain_Id={domain_id};'.format(domain_id=domainid)
        pd.read_sql(sql=query, con=conn).to_csv(settings.STATIC_ROOT + file_path, index=False)
        return JsonResponse({'msg': 'Proxy Download successful','path': settings.STATIC_URL + file_path}, safe=False)

    return JsonResponse({'msg': 'No Proxy Found for this domain', 'path':''}, safe=False)


def sp_get_by_param(sp_name , list_args):
        db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                         user=settings.DATABASES['default']['USER'],
                         passwd=settings.DATABASES['default']['PASSWORD'],
                         db=settings.DATABASES['default']['NAME'])
        if not isinstance(list_args, list):
            list_args = [list_args]
        cursor = db.cursor()
        args = list_args
        cursor.callproc(procname=sp_name , args=args )
        cursor.close()
        db.commit()

def sp_get_records_by_param(sp_name , list_args):
        db = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                         user=settings.DATABASES['default']['USER'],
                         passwd=settings.DATABASES['default']['PASSWORD'],
                         db=settings.DATABASES['default']['NAME'])
        if not isinstance(list_args, list):
            list_args = [list_args]
        cursor = db.cursor()
        args = list_args
        cursor.callproc(procname=sp_name , args=args)
        records = cursor.fetchall()
        cursor.close()
        db.commit()
        return records

@csrf_exempt
def upload(request, request_id=None):
    
    domainid = request.POST['domainId']
    #domainId = domainid.split(",")
    vendors = list()
    Proxy = list()
 
    # saved_files = list()
    for upload_name, uploaded_file in request.FILES.items():
        fs = FileSystemStorage()
        saved_file = fs.save(uploaded_file.name, uploaded_file)
        
        output , proxyName = ProxyMaster.upload_csv(saved_file)

        if not output:
            data = {'msg': "Blank csv file is not allowed",'flag' :1}
            return JsonResponse(data, safe=False) 
        # saved_files.append(saved_file)
        vendors.extend(output)
        Proxy.extend(proxyName)


    print("^^^^^^^^^^^^^^^^^")
    print("vendors",vendors)
    print("ProxyName" , Proxy)
    print(list(set(vendors)))

    sp_get_by_param('sp_RemovePreviousProxyOfDomain', [domainid])
    for vendor in list(set(vendors)):
        for name in Proxy:
            sp_get_by_param('sp_AddProxyToDomainNew',[domainid,vendor,name])
    
    data = {'msg': 'Domain Mapped Successfully'}
    return JsonResponse(data, safe=False)

def getAllValue(domainid):

        dataObj =  sp_get_records_by_param('sp_getVendorTotalMappedProxy',[domainid])

        dataObjlist = []
        

        for row in dataObj:
            datadict = {}
            # datadict['id'] = row[0]
            datadict['vendor_name'] = row[0]
            datadict['vendor_count'] = row[1]
            datadict['mapped_count'] = row[2]
            dataObjlist.append(datadict)
          
        for i in dataObjlist:
            if i['mapped_count'] == None:
                i['mapped_count'] = 0
                i['unmapped_count'] = i['vendor_count'] - i['mapped_count']
            else:
                i['unmapped_count'] = i['vendor_count'] - i['mapped_count']
                if i['unmapped_count'] < 0 :
                    i['unmapped_count'] = 0
         
        return dataObjlist

@csrf_exempt
def get_proxy(request):
    if request.method == 'POST' or request.is_ajax():
        domainid = request.POST['proxyId']
        request.session['domainid'] = domainid
        
    
        dataObjlist = getAllValue(domainid)

        data = {
            'proxy': dataObjlist
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def allMappedProxy(request): 
    if request.method == 'POST' or request.is_ajax():
        vendorName = request.POST['vendorName']
        request.session['vendorName'] = vendorName
 
        dataObjlist = mappedProxies(vendorName)

        data = {
            'domainName': dataObjlist
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

def mappedProxies(vendorName):
    domainName = sp_get_records_by_param('sp_getDomainNameMappedProxy',vendorName)  
    dataObjlist = []

    for row in domainName:
        datadict = {}
        # datadict['id'] = row[0]
        datadict['domain_id'] = row[0]
        datadict['domain_name'] = row[1]
        dataObjlist.append(datadict)
    return dataObjlist

@csrf_exempt
def unmapped_proxies(request):
    if request.method == 'POST' or request.is_ajax():

        vendName = request.POST['requestUnMapped']
        vendName = json.loads(vendName)
        domainid = request.session['domainid']
        proxyIdList = []
        for i in vendName:
            proxyIdList.append(sp_get_records_by_param('sp_getMappedProxyId',[domainid,i]))

        for i in proxyIdList:
            for j in i:
                sp_get_by_param('sp_deleteRecordsProxyDetails',[domainid,j])
        
        dataObjlist = getAllValue(domainid)
        
        data = {
            'proxy': dataObjlist,
            'msg' : "Proxies are UnMapped"
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def unmapped_proxies_by_vendor(request):
    if request.method == 'POST' or request.is_ajax():

        dName = request.POST['requestUnMapped']
        domainId = json.loads(dName)
        vendorName = request.POST['vendorName']
        proxyIdList = []
        for i in domainId:
            proxyIdList.append(sp_get_records_by_param('sp_getMappedProxyId',[i,vendorName]))
        for x in domainId:
            for i in proxyIdList:
                for j in i:
                    sp_get_by_param('sp_deleteRecordsProxyDetails',[x,j[0]])
        
        dataObjlist = mappedProxies(vendorName)
        data = {
            'domainName': dataObjlist,
            'msg' : "Proxies are UnMapped"
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def delete_proxies_by_vendor(request):
    if request.method == 'POST' or request.is_ajax():

        dName = request.POST['requestUnMapped']
        domainId = json.loads(dName)
        vendorName = request.POST['vendorName']
        dataObjlist = mappedProxies(vendorName)        
        if len(dataObjlist) > 0:
            msg = "Can't Delete the Proxy because It's mapped with {} Domain".format(len(dataObjlist))
            flag = 0
        else :
            sp_get_by_param('sp_deleteRecordsProxyMaster',[vendorName])
            msg = 'Proxies Deleted Successfully'
            flag = 1
          
        data = {
            'msg' : msg,
            'flag' : flag
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)

@csrf_exempt
def mapped_proxies(request):
    if request.method == 'POST' or request.is_ajax():
        vendorName = request.POST['requestMapped']
        
        vendName = json.loads(vendorName)
        domainid = request.session['domainid']
       
                     
        for i in vendName:
            sp_get_by_param('sp_AddProxyToDomain',[domainid,i])
        
        dataObjlist = getAllValue(domainid)
        
        data = {
            'proxy': dataObjlist,
            'msg' : "Proxies are Mapped"
            

        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Not founded on server '}, safe=False)
