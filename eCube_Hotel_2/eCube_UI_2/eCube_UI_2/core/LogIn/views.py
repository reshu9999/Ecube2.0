import json
import requests
import datetime
import string
import random
from eCube_UI_2.core.resources.models import ModelHandler
#from eCube_UI_2.core.Add_Request.models import UserToken
from django.core.mail import EmailMessage
# from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

# from Notifications.models import Notifications
# from UserManagement.models import UserMaster, BliMaster, BliUserMap, AccessItemsMaster, UserMenuAccessMappings
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP


class UserManagementModels(ModelHandler):
    REQUIRED_MODELS = ['UserMaster', 'BliMaster', 'BliUserMap', 'AccessItemsMaster', 'UserMenuAccessMappings', 'UserToken']


class NotificationModels(ModelHandler):
    REQUIRED_MODELS = ['Notifications']


@csrf_exempt
def UserLogin(request):

    username = request.POST.get('UserName')
    password = request.POST.get('Password')
    bli_id = request.POST.get('BLI_ID')

    if not username:
        return {'Message': 'Username is required.', 'status':  'Error'}

    if not password:
        return {'Message': 'Password is required.', 'status': 'Error'}

    if not bli_id:
        return {'Message': 'Bli ID is required.', 'status': 'Error'}

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        bli_object = UserManagementModels.MODELS_MAP['BliMaster'].objects.get(id=bli_id)
        request.session['bli_id'] = bli_id
        request.session['BliID'] = bli_id
        request.session['UserID'] = user.User_ID
        request.session['business'] = bli_object.business
        request.session['BliName'] = bli_object.BliName
        # usermanager = UserManagementDB()
        # queryset = usermanager.GetUserMenus(request.user.User_ID)
        # result_set = flatten_arr(queryset)
        # print(result_set)
        # result_menu= list(result_set)

        # TODO: commenting for now
        accessitems = list(UserManagementModels.MODELS_MAP['UserMenuAccessMappings'].objects.filter(
            user_id=user.User_ID).values('accessitems', 'limits', 'permission_type'))
        # usermenus = list(UserManagementModels.MODELS_MAP['AccessItemsMaster'].objects.filter(id__in=accessitems).values_list('accessitems',flat=True))
        # countNotification = NotificationModels.MODELS_MAP['Notifications'].objects.filter(delete=False, active=True, created_date__gte=datetime.date.today()).count()
        # request.session["notificationCount"] = countNotification
        request.session["UserMenuAccess"] = {uma['accessitems']: uma for uma in accessitems}

        # TODO: end

        return {'Message': 'User logged in successfully.', 'status': 'Success'}
    return {'Message': 'Invalid username/password.', 'status': 'Error'}


@csrf_exempt
def UserLoginCheck(request):

    username = request.POST.get('UserName')
    password = request.POST.get('Password')

    if not username:
        return {'Message': 'Username is required.', 'status': 'Error'}
    
    if not password:
        return {'Message': 'Password is required.', 'status': 'Error'}

    user = authenticate(request, username=username, password=password)
    if user is not None:
        # TODO: use bli_table in hotel
        bli_ids = list(UserManagementModels.MODELS_MAP['BliUserMap'].objects.filter(userid=user.User_ID).values_list('bliid', flat=True))
        bli_list = list(UserManagementModels.MODELS_MAP['BliMaster'].objects.filter(id__in=bli_ids).values('id', 'BliName').distinct())
        if (len(bli_list)>1):
                html = '''<label for="username_input">
                <svg version="1.1" class="user-icon" x="0px" y="0px" viewBox="-255 347 100 100" xml:space="preserve" height="36px" width="30px">
                    <path class="user-path" d="
                        M-203.7,350.3c-6.8,0-12.4,6.2-12.4,13.8c0,4.5,2.4,8.6,5.4,11.1c0,0,2.2,1.6,1.9,3.7c-0.2,1.3-1.7,2.8-2.4,2.8c-0.7,0-6.2,0-6.2,0
                        c-6.8,0-12.3,5.6-12.3,12.3v2.9v14.6c0,0.8,0.7,1.5,1.5,1.5h10.5h1h13.1h13.1h1h10.6c0.8,0,1.5-0.7,1.5-1.5v-14.6v-2.9
                        c0-6.8-5.6-12.3-12.3-12.3c0,0-5.5,0-6.2,0c-0.8,0-2.3-1.6-2.4-2.8c-0.4-2.1,1.9-3.7,1.9-3.7c2.9-2.5,5.4-6.5,5.4-11.1
                        C-191.3,356.5-196.9,350.3-203.7,350.3L-203.7,350.3z
                    "/>
                </svg></label><select id="bli_id">'''
                for bli in bli_list:
                    html += '<option value=' + str(bli['id']) + '>' + bli['BliName'] + '</option>'
                html += '</select>'
                mul_bli=True
        else :
              html=str(bli_list[0]['id'])
              mul_bli=False
        return {'Message': html, 'status': 'Success' ,'mul_bli':mul_bli}
    
    return {'Message': 'Invalid username/password.', 'status': 'Error'}
    

def Forgot_Password(request):
    if request.method == 'POST' or request.is_ajax():        
        username = request.POST.get('UserID')
        EmailId =  request.POST.get('EmailID')        
        user = UserManagementModels.MODELS_MAP['UserMaster'].objects.filter(UserName=username,EmailID=EmailId).first()        
        if not user is None:
            # password = UserManagementModels.MODELS_MAP['UserMaster'].objects.make_random_password()
            password = 'eclerx#123'
            user.set_password(password)
            user.save()
            token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            #UserToken.objects.create(user_id=user.User_ID,token=token)
            UserManagementModels.MODELS_MAP['UserToken'].objects.create(user_id=user.User_ID,token=token)
            body = custombody(username,password,token)            
            dict1 = {"to": EmailId, "bcc": EmailId, "body": body,
                "subject": "eCube 2.0 - Forgot Password   ", "has_attachments": False}
            mail_args = json.dumps(dict1)      
            requests.post('http://localhost:8004/api/v1/send_email/', data=mail_args)
            # send_mail(to=EmailId, subject='Password Reset', body=body)
            return {"Message": "Password sent to registered email", "MSG_TYPE": 2}
            
        return {"Message": "Invalid user Id/user email Id", "MSG_TYPE": 3}
            

def custombody(username,password,token):
    body = """\
                <html>
                <head> </head>
                <body>
                <p>Dear {0},
                    <br><br>
                        Your new password is {1}.
                    <br />
                    Kindly click on link to change your password : <a href={2} > Reset Password</a>.
                    <br/><br/>
                        For any queries, please contact eCube2_TechTeam@eclerx.com
                    <br/>
                        <br/>
                    Regards,
                    <br/>
                    eCube Admin Team
                    </p>
                </p>
                <p>This message including attachment(s) is intended only for the personal and confidential use of the recipient(s) named above.This communication is for informational purposes only.Email transmission cannot be guaranteed to be secure or error-free.
                    All information is subject to change without notice. If you are not the intended recipient of this message you are hereby notified that any review, dissemination, distribution or copying of this message is strictly prohibited. If you are not the
                    intended recipient, please contact:<a href="mailto:helpdesk@eclerx.com">helpdesk@eclerx.com</a><br><br>
                </p>
                <p>
                    <font size="3pt" color="black" family="Tahoma"><strong>© 2016.eClerx Services Ltd. An ISO/IEC 27001:2013 Company</strong></font>
                </p>
                </body>
                </html>
                """.format(username,password, settings.DJANGO_BASEURL + reverse('hotel_user_management_confirm_reset_password', kwargs={'token':token}))
    return body


def send_mail(to, subject, body):
    msg = MIMEMultipart('alternative')
    sender = settings.EMAIL_HOST_ID
    msg['Subject'] = subject
    msg['From'] = settings.EMAIL_HOST_ID
    msg['To'] = to
    part = MIMEText(body, 'html')
    msg.attach(part)
    mail_obj = SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    mail_obj.starttls()
    username = settings.EMAIL_HOST_USERNAME
    password = settings.EMAIL_HOST_PASSWORD
    mail_obj.login(username, password)
    resp = mail_obj.sendmail(sender, to, msg.as_string())
    return resp


def UserLogout(request):
    logout(request)

@csrf_exempt
def ResetPassword(request):
    if "UserID" in request.session:
        if request.method == 'POST' and request.is_ajax():
            conf_password =  json.loads(request.POST['con_pass'])
            user = UserMaster.objects.get(UserName=request.user.UserName)
            user.set_password(conf_password)
            user.save()
            return JsonResponse({"MSG_TYPE":"1"})
        else:
            return render(request,'user_login/Reset_Password.html')
    else:
        return redirect(reverse('UserLogin'))
