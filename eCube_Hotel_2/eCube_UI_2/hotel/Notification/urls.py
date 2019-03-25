from django.conf.urls import url
from hotel.Notification import views

urlpatterns = [
   url(r'^notifications/$', views.index, name='notification'),
   url(r'^getNotifications/$', views.getNotifications, name='getNotifications'),
   url(r'^save_update/$', views.save_update, name='save_update'),
   url(r'^save_update/(?P<val>[0-9]+)/$', views.save_update, name='save_update_main'),
   url(r'^getNotificationsById/$', views.getNotificationsById, name='getNotificationsById'),
   url(r'^removeNotifications/$', views.removeNotifications, name='removeNotifications'),
   url(r'^updateStatus/$', views.updateStatus, name='updateStatus'),
]