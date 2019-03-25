# Core Imports
from eCube_UI_2.core.resources.models import ModelHandler
from eCube_UI_2.core.resources.db_connectors import MongoDBBaseHandler

# Package Imports
import pymysql
import datetime

# Django Imports
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import get_template


class RequestManagementModels(ModelHandler):
    REQUIRED_MODELS = [
        'CrawlRequestDetail', 'RequestMaster',
        # 'FieldGroupMapping'
    ]


def request_management(request, db):
    cur = db.cursor()
    fromdate = None
    todate = None
    fromnextdate = None
    tonextdate = None
    fromcompletedate = None
    tocompletedate = None
    
    user_Id = request.session["UserID"]
    bli_id = request.session.get('bli_id')
    if request.method == 'POST':
        fetchall = 0

        requestno = request.POST.get('reqnumber') or 0
        RequestDesc = request.POST.get('RequestDesc') or None
        RequestFromDate = request.POST.get('fromCreateDate') or None
        RequestToDate = request.POST.get('toCreateDate') or None
        FromNextScheduleDate = request.POST.get('FromNextScheduleDate') or None
        TONextScheduleDate = request.POST.get('TONextScheduleDate') or None
        FromCompletionDate = request.POST.get('FromCompletionDate') or None
        ToCompletionDate = request.POST.get('ToCompletionDate') or None
        ReqStatus = request.POST.get('ReqStatus') or None
        fn_chk = request.POST.get('fn_chk') or None
       
        if RequestFromDate and RequestToDate:
            fromdate = datetime.datetime.strptime(
                RequestFromDate, '%m/%d/%Y').strftime("%Y-%m-%d")
            todate = datetime.datetime.strptime(
                RequestToDate, '%m/%d/%Y').strftime("%Y-%m-%d")
        if FromNextScheduleDate and TONextScheduleDate:
            fromnextdate = datetime.datetime.strptime(
                FromNextScheduleDate, '%m/%d/%Y').strftime("%Y-%m-%d")
            tonextdate = datetime.datetime.strptime(
                TONextScheduleDate, '%m/%d/%Y').strftime("%Y-%m-%d")

        if FromCompletionDate and ToCompletionDate:
            fromcompletedate = datetime.datetime.strptime(
                FromCompletionDate, '%m/%d/%Y').strftime("%Y-%m-%d")
            tocompletedate = datetime.datetime.strptime(
                ToCompletionDate, '%m/%d/%Y').strftime("%Y-%m-%d")

        args = [requestno, RequestDesc, fromdate, todate, fromnextdate, tonextdate,
                fromcompletedate, tocompletedate, ReqStatus, fetchall,user_Id,bli_id]
        if not fn_chk:
            # args = [ReqStatus,user_Id,bli_id]
            if ReqStatus.lower() == 'today':
                args = [None, None, str(datetime.datetime.now().date()), str(datetime.datetime.now().date()), None,
                        None, None, None, None, fetchall, user_Id, bli_id]
            else:
                args = [None, None, None, None, None, None, None, None, ReqStatus, fetchall, user_Id, bli_id]
            # cur.callproc(procname="sp_FilterReqManagementbystatus", args=args)

            # print("args1")
            # print(args)
            cur.callproc(procname="aetos_RequestSearchSP", args=args)
        else:
          
            # [0, 'NULL', '2018-10-16', '2018-10-16',
            #  None, None, None, None, 'NULL', 1, 40,
            # '1']
            # cur.callproc(procname="sp_SearchRequestManagement", args=args)
            # print("args2")
            # print(args)
            cur.callproc(procname="aetos_RequestSearchSP", args=args)
            
        result = cur.fetchall()
        cur.close()

        columns = ["RequestRunId", "RequestId", "RequestTitle", "RequestDescription", "ScheduleType", "UserName",
                   "StartedDatetime",
                   "EndDateTime", "OR", "TR", "Completed", "PNF", "PSFailcount", "Status", "Percent", "ReportDownloadLink","sch_date","CreatedDatetime"]
        datalist = []
        for x in result:
            datalist.append(dict(tuple(zip(columns, x))))
    else:
        fetchall = 1
        ReqStatus = 'All'
        Dashboardstatus = request.GET.get('status')
        DashboardfromDate = request.GET.get('fromDate')
        Dashboardtodate = request.GET.get('toDate')

        if DashboardfromDate != None and Dashboardtodate != None and Dashboardstatus != None:
            fromdate = datetime.datetime.strptime(
                DashboardfromDate, '%d-%m-%Y').strftime("%Y-%m-%d")
            todate = datetime.datetime.strptime(
                Dashboardtodate, '%d-%m-%Y').strftime("%Y-%m-%d")
            args = [None, None, fromdate, todate, None, None, None, None, Dashboardstatus, 2, user_Id, bli_id]
        else:
            # args = [None, None, str(datetime.datetime.now().date()), str(datetime.datetime.now().date()), None, None,
            #         None, None, None, fetchall, user_Id, bli_id]
            args = [None, None, None, None, None, None, None, None, None, fetchall, user_Id, bli_id]
        
        # cur.callproc(procname="sp_SearchRequestManagement", args=args)
        # print("args3")
        # print(args)
        cur.callproc(procname="aetos_RequestSearchSP", args=args)
        result = cur.fetchall()
        cur.close()
        columns = ["RequestRunId", "RequestId", "RequestTitle", "RequestDescription", "ScheduleType", "UserName", "StartedDatetime",
                   "EndDateTime", "OR", "TR", "Completed", "PNF", "PSFailcount", "Status", "Percent", "ReportDownloadLink","sch_date","CreatedDatetime"]
        datalist = []
        for x in result:
            datalist.append(dict(tuple(zip(columns, x))))

    db.close()
    return {'datalist': datalist, 'ReqStatus': ReqStatus}


def getUrlRequest(request):
    client = MongoDBBaseHandler('url').client

    field_value_template = get_template('Add_Request/field_value.html')
    req_id = int(request.GET['req_id'])
    req = RequestManagementModels.MODELS_MAP['RequestMaster'].objects.get(id=req_id)
    if not req.field_group:
        mappings = RequestManagementModels.MODELS_MAP['FieldGroupMapping'].objects.filter(pk=42)
    else:
        mappings = RequestManagementModels.MODELS_MAP['FieldGroupMapping'].objects.filter(
            field_group=req.field_group)

    def make_field_value_html(x): return field_value_template.render({'data': {map.field.name: x.get(map.field.name, 'None')
                                                                               for map in mappings}})

    def mongo_crawl_data(y): return client.HTMLDumps.CrawlResponse.find_one(
        {'subRequestId': str(y.id)}) or dict()

    return JsonResponse({
        'dataObjlist': [{
            'RequestUrl': obj.request_url,
            'StartDatetime': obj.start_date,
            'EndDatetime': obj.end_date,
            'Data': make_field_value_html(mongo_crawl_data(obj)),
        } for obj in RequestManagementModels.MODELS_MAP['CrawlRequestDetail'].objects.filter(request_id=req_id)]
    })
