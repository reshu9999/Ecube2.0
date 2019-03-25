from django.conf.urls import url

from hotel.user_login import views as hotel_login_views

urlpatterns = [
    url(r'^login/$', view=hotel_login_views.login_handler, name='login_index'),
    url(r'^login/do-login/$', view=hotel_login_views.login_handler, name='do_login'),
    url(r'^login/check-bli/$', view=hotel_login_views.check_login_and_get_bli, name='check_login_and_get_bli'),
    url(r'^logout/$', view=hotel_login_views.logout, name='do_logout'),
    url(r'^login/forgot-password/$', view=hotel_login_views.forgotpassword, name='login_forgot_password')
]
