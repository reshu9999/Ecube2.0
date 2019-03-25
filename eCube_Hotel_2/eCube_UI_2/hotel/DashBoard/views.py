from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from datetime import datetime,timedelta

# Create your views here.

@csrf_exempt
def Index(request):

    daysCount = 0
    if request.method == "POST":
        daysCount = request.POST.get('request_data')
    fromDate = datetime.now().strftime("%Y-%m-%d")
    result = getCount(request, fromDate,int(daysCount))
    return  render(request, 'hotel/Dashboard/index.html',{"Running" : result[0],"Queue" : result[1],"Complete" : result[2],"Stop" : result[3],"Pause" : result[4],"Scheduled": result[5]})


def getCount(request, fromDate,daysCount=0):

    if daysCount > 0:
        fromDate = datetime.now()-timedelta(days=daysCount)
        fromDate = fromDate.strftime("%Y-%m-%d")
    toDate = datetime.now().strftime("%Y-%m-%d")

    cur = connection.cursor()
    runningCount =''
    completeCount = ''
    stopCount=''
    queueCount=''
    pauseCount=''
    scheduledCount = ''
    user_id = request.user.User_ID
    cur.callproc('GetRequestStatusCount',[fromDate,toDate,runningCount,completeCount,stopCount,queueCount,pauseCount,scheduledCount,user_id,request.session['bli_id']])
    cur.execute('select @_GetRequestStatusCount_2,@_GetRequestStatusCount_3,@_GetRequestStatusCount_4,@_GetRequestStatusCount_5,@_GetRequestStatusCount_6,@_GetRequestStatusCount_7')
    t  = cur.fetchone()
    p = []
    for r in t:
        p.append(r.decode())

    return  p

@csrf_exempt
def GetCountData(request):

    if request.method == "POST":
        daysCount = request.POST.get('daysCount')
    fromDate = datetime.now()-timedelta(days=int(daysCount))
    fromDate = fromDate.strftime("%Y-%m-%d")
    toDate = datetime.now().strftime("%Y-%m-%d")

    cur = connection.cursor()
    runningCount =''
    completeCount = ''
    stopCount=''
    queueCount=''
    pauseCount=''
    scheduledCount = ''
    user_id = request.user.User_ID

    cur.callproc('GetRequestStatusCount',[fromDate,toDate,runningCount,completeCount,stopCount,queueCount,pauseCount,scheduledCount,user_id,request.session['bli_id'] ])
    cur.execute('select @_GetRequestStatusCount_2,@_GetRequestStatusCount_3,@_GetRequestStatusCount_4,@_GetRequestStatusCount_5,@_GetRequestStatusCount_6,@_GetRequestStatusCount_7')

    t = cur.fetchone()
    p = []
    for r in t:
        p.append(r.decode())
    return JsonResponse({"data": p})

@csrf_exempt
def GetBatchData(request):
    if request.method == "POST":
        Id = int(request.POST.get('Id'))
        user_id = request.user.User_ID
        bli_id = request.session['bli_id']

    cur = connection.cursor()
    cur.callproc('GetBatchData',[bli_id,user_id])

    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.close()
    connection.close()
    return JsonResponse({"data": r})
