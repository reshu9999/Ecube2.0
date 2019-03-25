from django.conf.urls import url

from eCube_UI_2.core.LogIn import views as login_views

urlpatterns = [

    url(r'^$', view=login_views.UserLogin, name='UserLogin'),
    url(r'^LogIn/Login/$', view=login_views.UserLogin, name='login'),
    url(r'^LogIn/check/$', view=login_views.UserLoginCheck, name='login-check'),
    url(r'^LogIn/Forgot_Password/', view=login_views.Forgot_Password, name='Forgot_Password'),
    url(r'^LogOut/Logout$', view=login_views.UserLogout, name='UserLogout'),
    url(r'^UserAccount/ResetPassword/$', view=views.ResetPassword, name='login_resetpassword')
]
