# App Imports
from hotel.models import UserMaster
from hotel.user_management.models import BliMaster, BliUserMap, AccessItemMaster, UserMenuAccessMapping, UserToken

# Core Imports
from eCube_UI_2.core.LogIn import views as core_views

# Django Imports
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect

core_views.UserManagementModels.MODELS_MAP = {
    'BliMaster': BliMaster,
    'BliUserMap': BliUserMap,
    'UserMaster': UserMaster,
    'AccessItemsMaster': AccessItemMaster,
    'UserMenuAccessMappings': UserMenuAccessMapping,
    'UserToken': UserToken,
}
core_views.NotificationModels.MODELS_MAP = {
    'Notifications': None,
}

core_views.UserManagementModels.check_required_models()
core_views.NotificationModels.check_required_models()


@csrf_exempt
def login_handler(request):
    if request.method == 'GET':
        return render(request, 'hotel/user_login/index.html')

    return JsonResponse(core_views.UserLogin(request))


@csrf_exempt
def check_login_and_get_bli(request):
    if request.method == 'GET':
        return render(request, 'hotel/user_login/index.html')

    return JsonResponse(core_views.UserLoginCheck(request))


@csrf_exempt
def logout(request):
    core_views.UserLogout(request)
    return redirect('login_index')


@csrf_exempt
def forgotpassword(request):    
    return JsonResponse(core_views.Forgot_Password(request))
