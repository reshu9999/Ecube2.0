# App Imports
from hotel.models import UserMaster
from hotel.master.models import DomainMaster, CountryMaster
from hotel.user_management.models import (RoleMaster, BliMaster, BliUserMap, MenuMaster, AccessItemMaster,
                                          RoleAccessItemDetails, UserMenuAccessMapping, RoleAccessMapping, Competitor,
                                          CompetitorMarketMapping, UserToken)

# TODO: NOT IN USE CURRENTLY
# BliDetails, BliAttribute, BliAttributeMaster

# Core Imports
# from eCube_UI_2.core.LogIn.views import *
from eCube_UI_2.core.UserManagement import views as core_views

# Django Imports
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect

core_views.UserManagementModels.MODELS_MAP = {
    'UserMaster': UserMaster,
    'RoleMaster': RoleMaster,
    'BliMaster': BliMaster,
    'BliUserMap': BliUserMap,
    # 'BliDetails': BliDetails,
    # 'BliAttribute': BliAttribute,
    # 'BliAttributeMaster': BliAttributeMaster,
    'AccessItemsMaster': AccessItemMaster,
    'RoleAccessItemDetails': RoleAccessItemDetails,
    'UserMenuAccessMappings': UserMenuAccessMapping,
    'RoleAccessMapping': RoleAccessMapping,
    'UserToken': UserToken,
}
core_views.DomainManagementModels.MODELS_MAP = {
    'Competitor': Competitor,
    'CompetitorMarketMapping': CompetitorMarketMapping,
}
core_views.AddRequestModels.MODELS_MAP = {
    'DomainMaster': DomainMaster,
    'CountryMaster': CountryMaster,
}
core_views.UserManagementModels.check_required_models()
core_views.DomainManagementModels.check_required_models()
core_views.AddRequestModels.check_required_models()


@csrf_exempt
def create_account(request):
    if request.method == 'POST' and request.is_ajax():
        return JsonResponse(core_views.create_account(request))

    return render(request, 'hotel/user_management/index.html')


@csrf_exempt
def bind_grid(request):
    return JsonResponse(core_views.bind_grid(request))


@csrf_exempt
def account_ops(request):
    if request.method == 'POST' or request.is_ajax():
        return JsonResponse(core_views.account_ops(request))

    return render(request, 'hotel/user_management/index.html')


@csrf_exempt
def delete_account(request):
    if request.method == 'POST' or request.is_ajax():
        return JsonResponse(core_views.delete_account(request))

    return render(request, 'hotel/user_management/index.html')


@csrf_exempt
def edit_account(request):
    if request.method == 'POST' or request.is_ajax():
        return JsonResponse(core_views.edit_account(request))

    return render(request, 'hotel/user_management/index.html')


@csrf_exempt
def update_account(request):
    if request.method == 'POST' or request.is_ajax():
        return JsonResponse(core_views.update_user_info(request))


@csrf_exempt
def load_role_data(request):
    if request.method == 'POST' or request.is_ajax():
        return JsonResponse(core_views.load_user_module_data(request), safe=False)


@csrf_exempt
def bind_user_permissions(request):
    if request.method == 'POST' or request.is_ajax():
        return JsonResponse(core_views.bind_user_permissions(request))


@csrf_exempt
def user_exists_check(request):
    return JsonResponse(core_views.user_exists_check(request))


@csrf_exempt
def email_exists_check(request):
    return JsonResponse(core_views.email_exists_check(request))


@csrf_exempt
def bind_competitor_market(request):
    return JsonResponse(core_views.bind_competitor_market(request), safe=False)


@csrf_exempt
def Reset_Password(request):  # Reset Password
    if request.method == 'GET':
        return render(request,'hotel/user_management/reset_password.html')
    return JsonResponse(core_views.Reset_Password(request), safe=False)


@csrf_exempt
def Confirm_Reset_Password(request,token):  # Confirm Reset Password
    if request.method == 'GET':
        return render(request,'hotel/user_management/confirm_reset_password.html', context={'token':token})
    return JsonResponse(core_views.Confirm_Reset_Password(request,token))
