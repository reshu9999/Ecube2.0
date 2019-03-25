# Core Imports
from eCube_UI_2.core.resources.models import ModelHandler
from eCube_UI_2.core.UserManagement.db_connectors import UserManagementDB
#from eCube_UI_2.core.Add_Request.models import UserToken

# Package Imports
import json
import requests
import random
import string
import datetime
from pdb import set_trace as st

# Django Imports
from django.db.models import Q
# from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP  

class UserManagementModels(ModelHandler):
    REQUIRED_MODELS = [
        'UserMaster', 'RoleMaster', 'BliMaster', 'BliUserMap', 'AccessItemsMaster', 'RoleAccessItemDetails',
        'UserMenuAccessMappings', 'RoleAccessMapping', 'UserToken'
        # 'BliDetails', 'BliAttribute', 'BliAttributeMaster',
    ]


class AddRequestModels(ModelHandler):
    REQUIRED_MODELS = ['DomainMaster', 'CountryMaster']


class DomainManagementModels(ModelHandler):
    REQUIRED_MODELS = ['Competitor', 'CompetitorMarketMapping']


def Load_Data(role):
    if role == "admin":
        queryset = UserManagementModels.MODELS_MAP['UserMaster'].objects.all().order_by('UserName')
    else:
        queryset = UserManagementModels.MODELS_MAP['UserMaster'].objects.filter(~Q(Role="admin")).order_by('UserName')
    list1 = []
    dict1 = {}
    for users in queryset:
        dict1 = {"UserID":users.User_ID,"FirstName": users.FirstName, "LastName": users.LastName, "UserName": users.UserName.title(),
                 "rolename": users.Role, "Active": users.Active, "Email": users.EmailID,
                 "Bli": list(UserManagementModels.MODELS_MAP['BliUserMap'].objects.filter(
                     userid=users.User_ID, delflg='N').values_list("bliid", flat=True))}
        list1.append(dict1)
    return list1


def Load_Bli_Data():
    queryset = UserManagementModels.MODELS_MAP['BliMaster'].objects.all().order_by('BliName')
    list = []
    dict = {}
    for users in queryset:
        dict = {"BliName": users.BliName, "BliId": users.id, "Active": users.Active}
        list.append(dict)
    return list


def LoadPermissions():
    accessitems = UserManagementModels.MODELS_MAP['AccessItemsMaster'].objects.filter(
        active=True).values_list('id', 'accessitems')
    dic = {}
    for item in accessitems:
        dic[item[1]] = item[0]
    return dic


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

@csrf_exempt
def bind_grid(request):
    if request.method == 'GET' or request.is_ajax():
        role = request.user.Role
        username = request.user.UserName
        competitors = dict(UserManagementDB(request.user.User_ID).GetCompetitorsByDomains())
        # competitors = list(DomainManagementModels.MODELS_MAP['Competitor'].objects.values('id', 'name'))
        data = {
            'Grid': Load_Data(role),
            'Bli': Load_Bli_Data(),
            'Competitors': competitors,
            'Permissions': LoadPermissions()
        }
        return data
    else:
        return {'Data': 'Not founded'}


@csrf_exempt
def create_account(request):  # Add User
    usermodel = json.loads(request.POST['usermodel']) #Fetching User Details
    permissionmodel = request.POST['permissionmodel'] #Fetching User Permission Details

    permission = json.loads(permissionmodel)[0] #Fetching Role Type
    blimodel = json.loads(request.POST['blimodel'])
    userrole = permission.get('UserType')
    firstname = usermodel['F_Name']
    lastname = usermodel['L_Name']
    username = usermodel['U_Name']
    emailid = usermodel['E_Mail']
    role = userrole

    password = "eclerx#123"
    if UserManagementModels.MODELS_MAP['UserMaster'].objects.filter(UserName=username).exists():
        return {
            'Grid': Load_Data(request.user.Role), 'Message': 'User already created', 'MSG_TYPE': '2'
        }

    if UserManagementModels.MODELS_MAP['UserMaster'].objects.filter(EmailID=emailid).exists():
        return {
            'Grid': Load_Data(request.user.Role), 'Message': 'Email address already exists', 'MSG_TYPE': '2'
        }
    # password = UserManagementModels.MODELS_MAP['UserMaster'].objects.make_random_password()
    user = UserManagementModels.MODELS_MAP['UserMaster'].objects.create(UserName=username,
        FirstName=firstname, LastName=lastname, EmailID=emailid,
        Role=role, Active=True,
        CreatedDate=datetime.datetime.now()
    )
    user.set_password(password)
    user.save()

    result = json.loads(permissionmodel)
    listresult = []
    for rolesaccess in result:
        listresult.append(UserManagementModels.MODELS_MAP['UserMenuAccessMappings'](
            user_id_id = user.User_ID,
            accessitems = rolesaccess.get('accessitems'),
            limits = rolesaccess.get('limits'),
            permission_type = rolesaccess.get('permission_type')

        ))

    UserManagementModels.MODELS_MAP['UserMenuAccessMappings'].objects.bulk_create(listresult)

    #Creating Bli User Mapping
    for item in blimodel:
        UserManagementModels.MODELS_MAP['BliUserMap'].objects.create(userid=user.User_ID , bliid= int(item), delflg = 'N')
   
    # competitormodel = request.POST['competitormodel']
    # model = json.loads(competitormodel)

    # listkeys = []
    # for value in model.values():
    #     for val in value:
    #         marketid, countryid = val.split(',')
    #         DomainManagementModels.MODELS_MAP['CompetitorMarketMapping'].objects.create(
    #             competitor_id_id=marketid, country_id_id=countryid, user_id_id=user.User_ID, active=True)
    
    # Mail Sending Code
    # custombody(firstname,lastname, password)

    return {
        'Grid': Load_Data(request.user.Role),
        'Message': 'User Created Successfully', 'MSG_TYPE': '1'
    }


def custombody(firstname, lastname, password):
    body = """
            <html>
            <head> </head>
            <body>
            <p>Dear {0} {1},
                <br>
                    Your password has been created and password is {2}.
                <br />
                    Kindly click on link to change your password : <a href={3} > Reset Password </a>.
                    <br/>
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
            """.format(firstname, lastname, password,settings.DJANGO_BASEURL + reverse('hotel_user_management_confirm_reset_password'))
    list = []
    send_mail(to=emailid, subject='Password generated successfully', body=body)


@csrf_exempt
def edit_account(request):  # edit User
    usermodel = json.loads(request.POST['usermodel']) #Fetching User Details
    permissionmodel =  request.POST['permissionmodel'] #Fetching User Permission Details
    # competitormodel = request.POST['competitormodel']
    permission  = json.loads(permissionmodel)[0] #Fetching Role Type
    blimodel = json.loads(request.POST ['blimodel'])
    userrole =  permission.get('UserType')
    firstname = usermodel['F_Name']
    lastname = usermodel['L_Name']
    user_id = usermodel['U_Name']
    emailid = usermodel['E_Mail']
    #Updates User Records
    userobject=UserManagementModels.MODELS_MAP['UserMaster'].objects.get(User_ID=user_id)
    username = userobject.UserName
    userrecords = UserManagementModels.MODELS_MAP['UserMaster'].objects.filter(UserName=username).update(
        FirstName=firstname, LastName=lastname, Role=userrole, EmailID=emailid)

    UserManagementModels.MODELS_MAP['UserMenuAccessMappings'].objects.filter(user_id=user_id).delete()#User deletes old permissions
    #Inserts new user permission models
    result = json.loads(permissionmodel)
    listresult = []
  
    for rolesaccess in result:
        listresult.append(UserManagementModels.MODELS_MAP['UserMenuAccessMappings'](
            user_id_id = user_id,
            accessitems = rolesaccess.get('accessitems'),
            limits = rolesaccess.get('limits'),
            permission_type = rolesaccess.get('permission_type')
        ))

    UserManagementModels.MODELS_MAP['BliUserMap'].objects.filter(userid=user_id).delete()
     #Creating Bli User Mapping
    for item in blimodel:
        UserManagementModels.MODELS_MAP['BliUserMap'].objects.create(userid=user_id, bliid= int(item), delflg = 'N')
    UserManagementModels.MODELS_MAP['UserMenuAccessMappings'].objects.bulk_create(listresult)
    DomainManagementModels.MODELS_MAP['CompetitorMarketMapping'].objects.filter(user_id=user_id).delete()
    
    # model = json.loads(competitormodel)
    # listkeys = []
    # for value in model.values():
    #     for val in value:
    #         marketid, countryid = val.split(',')
    #         DomainManagementModels.MODELS_MAP['CompetitorMarketMapping'].objects.create(
    #             competitor_id_id=marketid, country_id_id=countryid, user_id_id=user_id, active=True)

    if (userrecords > 0):
        queryset = UserManagementModels.MODELS_MAP['UserMaster'].objects.filter(UserName=username)
        list1 = []
        dict1 = {}

        if request.user.Role == "admin":
            queryset = UserManagementModels.MODELS_MAP['UserMaster'].objects.all().order_by('UserName')
        else:
            queryset = UserManagementModels.MODELS_MAP['UserMaster'].objects.filter(~Q(Role="admin")).order_by('UserName')
        for users in queryset:
            dict1 = {"UserId":users.User_ID, "Role":users.Role,"FirstName": users.FirstName, "LastName": users.LastName, "UserName": users.UserName,
                    "rolename": users.Role, "Active": users.Active, "Email": users.EmailID}
            list1.append(dict1)
        data = {
            'Grid': list1, 'Message': 'User Updated Sucessfully', 'MSG_TYPE': '1'
        }
    else:
        data = {
            'Message': 'Updation failed', 'MSG_TYPE': '2'
        }
    return data


@csrf_exempt
def delete_account(request):  # delete User
    userid = json.loads(request.POST.get('userid'))

    if request.user.User_ID == userid:
        data = {'Grid': Load_Data(request.user.Role),
                "Message": "Cannot delete own user", 'MSG_TYPE': '2'}
        return data

    # userobject = UserManagementModels.MODELS_MAP['UserMaster'].objects.get(UserName=username)
    # user_id = userobject.User_ID
    UserManagementModels.MODELS_MAP['UserMenuAccessMappings'].objects.filter(user_id=userid).delete() #Delete User Permission Settings
    DomainManagementModels.MODELS_MAP['CompetitorMarketMapping'].objects.filter(user_id=userid).delete()
    UserManagementModels.MODELS_MAP['BliUserMap'].objects.filter(userid=userid).delete()
    UserManagementModels.MODELS_MAP['UserMaster'].objects.filter(User_ID=userid).delete()
    data = {
        'Grid': Load_Data(request.user.Role), 'Message': 'User Deleted Sucessfully', 'MSG_TYPE': '1'
    }
    return data


@csrf_exempt
def account_ops(request):  # delete User
    # Act_staus = request.POST.get('Act_val')
    userid = json.loads(request.POST.get('userid'))
    userrecords = UserManagementModels.MODELS_MAP['UserMaster'].objects.filter(
        User_ID=userid).update(Active=True if json.loads(request.POST.get('Act_val')) == 1 else False)
    if userrecords > 0:
        data = {
            'Grid': Load_Data(request.user.Role),
            'Message': 'User Updated Sucessfully', 'MSG_TYPE': '1'
        }
    else:
        data = {
            'Grid': Load_Data(request.user.Role),
            'Message': 'Updation failed', 'MSG_TYPE': '2'
        }

    return data


@csrf_exempt
def api_consumption_add(request, bli_name, attr_name):
    if not request.method in ['POST', 'OPTIONS']:
        raise Exception('Incorrect Request Method\nShould be POST or OPTIONS')

    if request.method == 'OPTIONS':
        return JsonResponse({
            'bli_map': {obj.name: list(obj.attributes.values_list('attribute__title', flat=True))
                        for obj in UserManagementModels.MODELS_MAP['BliDetails'].objects.all()}
        })

    bli_attr = get_object_or_404(UserManagementModels.MODELS_MAP['BliDetails'], name=bli_name).attributes.get(attribute__title=attr_name)
    consumption = request.POST['consumption']
    bli_attr.add_consumption(consumption)

    return JsonResponse({
        'consumption': {
            'added_consumption': consumption,
            'daily_consumption': bli_attr.daily_consumption,
            'monthly_consumption': bli_attr.monthly_consumption,
            'daily_percentage': bli_attr.daily_percentage,
            'monthly_percentage': bli_attr.monthly_percentage,
        },
        'limits': {
            'daily_left': bli_attr.daily - bli_attr.daily_consumption,
            'monthly_left': bli_attr.monthly - bli_attr.monthly_consumption,
        },
    })


@csrf_exempt
def bli_index(request):
    if not request.method == 'GET':
        raise Exception('Incorrect Request Method\nShould be GET')

    all_attrs = UserManagementModels.MODELS_MAP['BliAttributeMaster'].objects.all()
    attr_master = list(all_attrs.values('class_name', 'input_name', 'title'))
    context = {
        'all_blis': UserManagementModels.MODELS_MAP['BliDetails'].objects.all(),
        'attr_master': attr_master,
    }
    return render(request, 'UserManagement/blis.html', context)


@csrf_exempt
def bli_view(request, bli_id):
    if not request.method == 'GET':
        raise Exception('Incorrect Request Method\nShould be GET')

    all_attrs = UserManagementModels.MODELS_MAP['BliAttributeMaster'].objects.all()
    attr_master = list(all_attrs.values('class_name', 'input_name', 'title'))
    context = {
        'all_blis': UserManagementModels.MODELS_MAP['BliDetails'].objects.all(),
        'attr_master': attr_master,
    }

    bli_detail_object = get_object_or_404(UserManagementModels.MODELS_MAP['BliDetails'], pk=bli_id)

    for attr in attr_master:
        obj = UserManagementModels.MODELS_MAP['BliAttribute'].objects.filter(bli_details=bli_detail_object, attribute__title=attr['title'])
        if obj:
            attr.update({'obj': obj.first()})

    context.update({
        'selected_bli_details': bli_detail_object,
    })
    return render(request, 'UserManagement/blis.html', context)


@csrf_exempt
def bli_add(request):
    if not request.method == 'POST':
        raise Exception('Incorrect Request Method\nShould be POST')

    all_attrs = UserManagementModels.MODELS_MAP['BliAttributeMaster'].objects.all()
    attr_master = list(all_attrs.values('class_name', 'input_name', 'title'))
    context = {
        'all_blis': UserManagementModels.MODELS_MAP['BliDetails'].objects.all(),
        'attr_master': attr_master,
    }

    request_post = request.POST
    selected_attrs = request_post.getlist('selected_attrs')
    bli_detail_object = UserManagementModels.MODELS_MAP['BliDetails'](
        bli_master=UserManagementModels.MODELS_MAP['BliMaster'].objects.all().first(),
        name=request_post['bli_name'],
        revenue=request_post['bli_revenue'],
    )
    bli_detail_object.save()

    for attr_obj in all_attrs:
        if attr_obj.input_name in selected_attrs:
            daily = request_post[attr_obj.input_name + '_daily']
            monthly = request_post[attr_obj.input_name + '_monthly']
            date = request_post[attr_obj.input_name + '_date']
            split_date = date.split('/')
            start_date = "%s-%s-%s" % (split_date[2], split_date[0], split_date[1]) if date else None
            if daily and monthly and date:
                bli_attr = UserManagementModels.MODELS_MAP['BliAttribute'](
                    bli_details=bli_detail_object,
                    attribute=attr_obj,
                    daily=daily,
                    monthly=monthly,
                    start_date=start_date,
                )
                bli_attr.save()

    for attr in attr_master:
        obj = UserManagementModels.MODELS_MAP['BliAttribute'].objects.filter(bli_details=bli_detail_object, attribute__title=attr['title'])
        if obj:
            attr.update({'obj': obj.first()})

    context.update({
        'selected_bli_details': bli_detail_object,
    })
    return render(request, 'UserManagement/blis.html', context)


@csrf_exempt
def bli_update(request, bli_id):
    if not request.method == 'POST':
        raise Exception('Incorrect Request Method\nShould be POST')

    all_attrs = UserManagementModels.MODELS_MAP['BliAttributeMaster'].objects.all()
    attr_master = list(all_attrs.values('class_name', 'input_name', 'title'))
    context = {
        'all_blis': UserManagementModels.MODELS_MAP['BliDetails'].objects.all(),
        'attr_master': attr_master,
    }

    request_post = request.POST
    selected_attrs = request_post.getlist('selected_attrs')
    bli_detail_object = get_object_or_404(UserManagementModels.MODELS_MAP['BliDetails'], pk=bli_id)
    bli_detail_object.name = request_post['bli_name']
    bli_detail_object.revenue = request_post['bli_revenue']
    bli_detail_object.save()

    for attr_obj in all_attrs:
        if attr_obj.input_name in selected_attrs:
            daily = request_post[attr_obj.input_name + '_daily']
            monthly = request_post[attr_obj.input_name + '_monthly']
            date = request_post[attr_obj.input_name + '_date']
            split_date = date.split('/')
            start_date = "%s-%s-%s" % (split_date[2], split_date[0], split_date[1]) if date else None
            if daily and monthly and date:
                old_bli_attrs = bli_detail_object.attributes.filter(attribute=attr_obj)
                if old_bli_attrs:
                    bli_attr = old_bli_attrs.first()
                    bli_attr.daily = daily
                    bli_attr.monthly = monthly
                    bli_attr.start_date = start_date
                else:
                    bli_attr = UserManagementModels.MODELS_MAP['BliAttribute'](
                        bli_details=bli_detail_object,
                        attribute=attr_obj,
                        daily=daily,
                        monthly=monthly,
                        start_date=start_date,
                    )
                bli_attr.save()
        else:
            old_bli_attrs = bli_detail_object.attributes.filter(attribute=attr_obj)
            old_bli_attrs.delete()

    for attr in attr_master:
        obj = UserManagementModels.MODELS_MAP['BliAttribute'].objects.filter(bli_details=bli_detail_object, attribute__title=attr['title'])
        if obj:
            attr.update({'obj': obj.first()})

    context.update({
        'selected_bli_details': bli_detail_object,
    })
    return render(request, 'UserManagement/blis.html', context)

def messagebody(username,password):
    body = """\
                            <html>
                            <head> </head>
                            <body>
                            <p>Dear {0},
                                <br>
                                    Your new paswword is {1}.
                                <br />
                                Kindly click on link to change your password : <a href = {2}> Reset Password</a>
                                <br/>
                                    For any queries, please contact eCube2_TechTeam@eclerx.com
                                <br/>
                                    <br/>
                                Regards,
                                <br/>
                                eCube Admin Team
                                </p>
                            </p>
                            </body>
                            </html>
                            """.format(username,password,settings.DJANGO_BASEURL + reverse('hotel_user_management_reset_password'))
    return body


@csrf_exempt
def Reset_Password(request):  # Reset Password
    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST.get('userid')
        email = request.POST.get('email')
        user = request.user
        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))            
        UserManagementModels.MODELS_MAP['UserToken'].objects.create(user_id=user_id,token=token)
        body = reset_custombody(user.UserName,token)            
        dict1 = {"to": email, "bcc": email, "body": body,
                "subject": "eCube 2.0 - Reset Password   ", "has_attachments": False}
        mail_args = json.dumps(dict1)      
        requests.post('http://localhost:8004/api/v1/send_email/', data=mail_args)
        return {"Message": 'Password reset successfully for ' + user.UserName +'. Mail has been sent.', "MSG_TYPE": 1}
            

def reset_custombody(username,token):
    body = """\
                <html>
                <head> </head>
                <body>
                <p>Dear {0},
                    <br>
                    <br>
                        You have requested to change the password.
                    <br />
                    Kindly click on link to change your password : <a href={1} > Reset Password</a>.
                    <br/>
                    <br/>
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
                """.format(username, settings.DJANGO_BASEURL + reverse('hotel_user_management_confirm_reset_password', kwargs={'token':token}))
    return body

@csrf_exempt
def bind_user_permissions(request):
    userid = json.loads(request.POST['model'])
    item = UserManagementModels.MODELS_MAP['UserMaster'].objects.get(User_ID=userid)
    # logic for binding competitor and market
    resultset = list(DomainManagementModels.MODELS_MAP['CompetitorMarketMapping'].objects.filter(
        user_id=item.User_ID, active=True).values('country_id', 'competitor_id'))

    list_competitors = []
    list_unique_competitor = []
    competitors = {}

    if resultset is not None:
        for result in resultset:
            list_competitors.append(result.get('competitor_id'))
    uniquecompetitors = set(list_competitors)

    for id in uniquecompetitors:
        competitors['compid'] = id
        competitors['name'] = list(DomainManagementModels.MODELS_MAP['Competitor'].objects.filter(
            id=id).values('name'))[0].get('name')
        countryidslist = list(DomainManagementModels.MODELS_MAP['CompetitorMarketMapping'].objects.filter(
            competitor_id=id, user_id=item.User_ID, active=True).values_list('country_id', flat=True))
        list_countries = []
        for cid in countryidslist:
            country = {}
            country['countryid'] = cid
            country['countryname'] = list(AddRequestModels.MODELS_MAP['CountryMaster'].objects.filter(
                id=cid, _active=True).values('name'))[0].get('countryname')
            list_countries.append(country)

        competitors['countries'] = list_countries
        list_unique_competitor.append(competitors)
        competitors = {}

    # logic for user binding permissions

    userpermissions = list(UserManagementModels.MODELS_MAP['UserMenuAccessMappings'].objects.filter(
        user_id=item.User_ID).values('accessitems', 'limits', 'permission_type'))

    return {"permissions": userpermissions, "role": item.Role, "Competitors": list_unique_competitor}


@csrf_exempt
def bind_competitor_market(request):
    competitorid = json.loads(request.POST['model'])
    country_ids = list(AddRequestModels.MODELS_MAP['DomainMaster'].objects.filter(competitorid__in=competitorid).values_list('country_id', flat=True))
    countries = list(AddRequestModels.MODELS_MAP['CountryMaster'].objects.filter(id__in=country_ids).values('id', 'name'))
    return countries


@csrf_exempt
def user_exists_check(request):
    usermodel = json.loads(request.POST['usermodel']) #Fetching User Details
    if UserManagementModels.MODELS_MAP['UserMaster'].objects.filter(UserName=usermodel['U_Name']).count() > 0:
        data = {"Message": 'User Already created', 'MSG_TYPE': '2'}
    else:
        data = {"Message": 'New User', 'MSG_TYPE': '1'}
    return data


@csrf_exempt
def email_exists_check(request):
    usermodel = json.loads(request.POST['usermodel']) #Fetching User Details
    if UserManagementModels.MODELS_MAP['UserMaster'].objects.filter(EmailID=usermodel['U_Mail']).count() > 0:
        data = {"Message": 'Email address already exists', 'MSG_TYPE': '2'}
    else:
        data = {"Message": 'New User', 'MSG_TYPE': '1'}
    return data


@csrf_exempt
def update_user_info(request):
    usermodel = json.loads(request.POST["usermodel"])
    firstname = usermodel['firstname']
    lastname = usermodel['lastname']
    user_id = usermodel['username']
    emailid = usermodel['emailid']
    blimodel = usermodel['blid']

    userobject = UserManagementModels.MODELS_MAP['UserMaster'].objects.get(
        User_ID=user_id)  # get the user object
    username = userobject.UserName
    flag = False
    if firstname == userobject.FirstName and lastname == userobject.LastName and emailid == userobject.EmailID:
        flag = True

    list_blis = list(UserManagementModels.MODELS_MAP['BliUserMap'].objects.filter(
        userid=user_id).values_list("bliid", flat=True))
    blimodel = list(map(int, blimodel))

    flag1 = False
    if set(blimodel) == set(list_blis):
        flag1 = True

    if flag == True and flag1 == True:
        return {"status": "1"}

    elif flag1 == False:
        Load_Data(request.user.Role)
        UserManagementModels.MODELS_MAP['BliUserMap'].objects.filter(userid=user_id).delete()
        for item in blimodel:
            UserManagementModels.MODELS_MAP['BliUserMap'].objects.create(
                userid=user_id, bliid=int(item), delflg='N')
        return {"status": "0"}

    else:
        Load_Data(request.user.Role)
        UserManagementModels.MODELS_MAP['UserMaster'].objects.filter(User_ID=user_id).update(FirstName=firstname,
                                                          LastName=lastname,
                                                          EmailID=emailid
                                                          )
        return {"status": "0"}

@csrf_exempt
def api_user_consumption_add(request, user_id):
    if request.method not in ['POST', 'OPTIONS']:
        raise Exception('Incorrect Request Method\nShould be POST or OPTIONS')

    if request.method == 'OPTIONS':
        return JsonResponse({
            'users': list(UserManagementModels.MODELS_MAP['UserMenuAccessMappings'].objects.filter(accessitem_id=18).values_list('user_id', 'content'))
        })

    user_mapping = get_object_or_404(UserManagementModels.MODELS_MAP['UserMenuAccessMappings'], name=user_id, accessitem_id=18)
    consumption = request.POST['consumption']
    user_mapping.add_consumption(consumption)

    return JsonResponse({
        'consumption': {
            'added_consumption': consumption,
            'total_consumption': user_mapping.total_consumption,
            'total_percentage': user_mapping.total_percentage,
        },
        'limits': {
            'count': int(user_mapping.count_left),
            'percentage': float(user_mapping.percentage_left),
        },
    })


@csrf_exempt
def api_user_consumption_reset(request, user_id):
    if request.method not in ['POST', 'OPTIONS']:
        raise Exception('Incorrect Request Method\nShould be POST or OPTIONS')

    if request.method == 'OPTIONS':
        return JsonResponse({
            'users': list(UserManagementModels.MODELS_MAP['UserMenuAccessMappings'].objects.filter(accessitem_id=18).values_list('user_id', 'content'))
        })

    user_mapping = get_object_or_404(UserManagementModels.MODELS_MAP['UserMenuAccessMappings'], name=user_id, accessitem_id=18)
    user_mapping.reset_consumption()

    return JsonResponse({
        'limits': {
            'count': int(user_mapping.count_remaining),
            'percentage': float(user_mapping.percentage_remaining),
        },
    })


@csrf_exempt
def Confirm_Reset_Password(request, token):
    if request.method == 'POST' and request.is_ajax():
        conf_password =  request.POST['con_pass']
        #token = kwargs.get('token')
        if not token:
            return {"MSG_TYPE":"2", "msg": "Invalid token."}
        if not UserManagementModels.MODELS_MAP['UserToken'].objects.filter(token=token).exists():
            return {"MSG_TYPE":"2", "msg": "Invalid token."}
        
        user_token = UserManagementModels.MODELS_MAP['UserToken'].objects.get(token=token)                
        user = UserManagementModels.MODELS_MAP["UserMaster"].objects.get(User_ID=user_token.user_id)
        user.set_password(conf_password)
        user.save()
        user_token.delete()
        data = {"MSG_TYPE":"1"}
        return data
