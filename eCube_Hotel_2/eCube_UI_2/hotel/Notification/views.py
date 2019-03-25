from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.http import HttpResponse, JsonResponse
from hotel.Notification import models

def index(request):
    if request.method == 'GET':
        return render(request, 'hotel/Notification/index.html')
    else:
        return JsonResponse({"data": "success"})

def Load_Notifications():
    queryset = models.Notifications.objects.filter(delete=False).order_by('-id')
    list = []
    dict = {}
    for notification in queryset:
        dict = {"id": notification.id, "title": notification.title, "description": notification.descriptions,
                "active": notification.active, "CreatedDate":notification.created_date, "CurrentDate":datetime.datetime.now().date()}
        list.append(dict)
    return list



@csrf_exempt
def getNotifications(request):
    if request.method == 'GET' or request.is_ajax():
        data = {'Grid': Load_Notifications()}
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Notfound'}, safe=False)


@csrf_exempt
def save_update(request):
    if request.is_ajax() and request.method == "POST":
        Updated_id =request.POST["Updated_id"]
        if not (Updated_id == ""):
            note_title = request.POST["Title"]
            note_descriptions = request.POST['Description']
            notificationRecords = models.Notifications.objects.filter(id=int(Updated_id)).update(title=note_title or None,
                                                                                          descriptions=note_descriptions or None,
                                                                                          )
            if (notificationRecords > 0):
                data = {'Grid': Load_Notifications(), 'Message': 'Notification updated sucessfully', 'MSG_TYPE': '1'}
            else:
                data = {'Message': 'Updation failed', 'MSG_TYPE': '2'}
            return JsonResponse(data)
        else:
            note_title = request.POST["Title"]
            note_descriptions = request.POST['Description']
            notification = models.Notifications(
                title=note_title,
                descriptions=note_descriptions,
                active=True,
                created_by=request.session['UserID'],
                deleted_by=request.session['UserID'],
                delete_date=datetime.datetime.now(),
                created_date=datetime.datetime.now())
            notification.save()
            data = {'Grid': Load_Notifications(), 'Message': 'Notification created sucessfully', 'MSG_TYPE': '1'}
            return JsonResponse(data)
    else:
        if request.method == 'GET':
            return render(request, 'Notifications/create_notification.html')

def Load_NotificationsById(noteId):
    queryset = models.Notifications.objects.filter(delete=False, id=int(noteId))
    list = []
    dict = {}
    for notification in queryset:
        dict = {"id": notification.id, "title": notification.title, "description": notification.descriptions,
                "active": notification.active}
        list.append(dict)
    return list



@csrf_exempt
def getNotificationsById(request):
    if request.method == 'GET' or request.is_ajax():
        note_id =request.GET['note_id']
        data = {'Grid': Load_NotificationsById(note_id)}
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Data': 'Notfound'}, safe=False)


@csrf_exempt
def removeNotifications(request):
    if request.method == 'POST' or request.is_ajax():
        notification_id = request.POST.get('id')
        notification_records = models.Notifications.objects.get(id=notification_id)
        notification_records.delete = True
        notification_records.save()
        data = {'Grid': Load_Notifications(), 'Message': 'Notifications Deleted Sucessfully', 'MSG_TYPE': '1'}
        return JsonResponse(data)
    else:
        if request.method == 'GET':
            return render(request, 'Notifications/create_notification.html')


@csrf_exempt
def updateStatus(request):
    if request.is_ajax() and request.method == "POST":
        note_id = request.POST["id"]
        note_status = request.POST['active']
        notificationRecords = models.Notifications.objects.filter(id=int(note_id)).update(active=note_status or None)
        data = {'Grid': Load_Notifications(), 'Message': 'Notification created sucessfully', 'MSG_TYPE': '1'}
        return JsonResponse(data)
    else:
        if request.method == 'GET':
            return render(request, 'Notifications/create_notification.html')
