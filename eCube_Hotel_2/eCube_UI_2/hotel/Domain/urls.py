from django.conf.urls import url
from hotel.Domain import views

urlpatterns = [
   url(r'^Domain_mapping/$', views.index.as_view(), name='domain_mapping'),
   url(r'^GetDomainName/$', views.GetDomainName, name='GetDomainName'),
   url(r'^domain_uploader_post/$', views.domain_uploader_post, name='domain_uploader_post'),
   url(r'^domain_uploader_file_download/$', views.domain_uploader_file_download, name='domain_uploader_file_download'),
]