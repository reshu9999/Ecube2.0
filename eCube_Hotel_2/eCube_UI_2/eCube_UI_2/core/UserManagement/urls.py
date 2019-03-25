"""DjangoMongoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from UserManagement import views

urlpatterns = [
      url(r'^UserManagement/Create_Account', view=views.Create_Account, name='Create_User'),
      url(r'^UserManagement/Reset_Password', view=views.Reset_Password, name='Reset_Password'),
      url(r'^UserManagement/Bind_Grid', view=views.Bind_Grid, name='Bind_Grid'),
      url(r'^UserManagement/edit_account', view=views.edit_account, name='edit_account'),
      url(r'^UserManagement/delete_account', view=views.delete_account, name='delete_account'),
      url(r'^UserManagement/Actiave_Deactivate_account', view=views.Actiave_Deactivate_account, name='Activate_Deactivate_account'),

      url(r'^UserManagement/bli/add/$', view=views.bli_add, name='user_management_add_bli'),
      url(r'^UserManagement/bli/view/(?P<bli_id>\d+)/$', view=views.bli_view, name='user_management_view_bli'),
      url(r'^UserManagement/bli/update/(?P<bli_id>\d+)/$', view=views.bli_update, name='user_management_update_bli'),
      url(r'^UserManagement/bli/$', view=views.bli_index, name='user_management_bli'),
      url(r'^UserManagement/bli/consumption/add/(?P<bli_name>\d+)/(?P<attr_name>\d+)$', view=views.api_consumption_add, name='user_management_api_add_consumption'),

      url(r'^UserManagement/UserRoleData$', view=views.LoadUserModuleData, name='user_management_userroledata'),
    #   url(r'^UserManagement/EditPermissionSettings$', view=views.EditPermissionSettings, name='user_management_editpermissionsettings'),
      url(r'^UserManagement/BindUserPermissions$', view=views.BindUserPermissions, name='user_management_userbindpermissions'),
      url(r'^UserManagement/BindMarket_Competitor$', view=views.BindCompetitor_Martket, name='usermanagement_bindcompetitor_market'),
      url(r'^UserManagement/UserCheck$', view=views.User_Check, name='usermanagement_user_check'),
      url(r'^UserManagement/UserMailCheck$', view=views.User_Mail_Check, name='usermanagement_mail_check'),

      url(r'^UserManagement/user/consumption/add/(?P<user_id>\d+)/$', view=views.api_user_consumption_add,
          name='user_management_api_add_user_consumption'),
      url(r'^UserManagement/user/consumption/reset/(?P<user_id>\d+)/$', view=views.api_user_consumption_reset,
          name='user_management_api_reset_user_consumption'),

]
