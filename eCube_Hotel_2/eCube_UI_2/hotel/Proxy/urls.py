from django.conf.urls import url
from hotel.Proxy import views

urlpatterns = [
   url(r'^proxy_mapping/$', views.index, name='proxy_mapping'),
   url(r'^upload/$', views.upload, name='upload_proxies'),
   url(r'^proxy/$', views.get_proxy, name='get_proxies'),
   url(r'^proxy/download/$', views.download_proxy, name='proxy-download'),
   url(r'^delete_proxies_by_vendor/$', views.delete_proxies_by_vendor, name='delete_proxies_by_vendor'),
   url(r'^unmapped_proxies/$', views.unmapped_proxies, name='unmapped_proxies'),
   url(r'^mapped_proxies/$', views.mapped_proxies, name='mapped_proxies'),
   url(r'^allMappedProxy/$', views.allMappedProxy, name='allMappedProxy'),
   url(r'^unmapped_proxies_by_vendor/$', views.unmapped_proxies_by_vendor, name='unmapped_proxies_by_vendor'),
]