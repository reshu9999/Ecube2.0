from django.conf.urls import url

from Add_Request import views



urlpatterns = [


    url(r'^Add_Request/download', views.download, name='add_request_download'),

    url(r'^Add_Request/index/(?P<request_id>\d+)/$', views.index, name='add_request_index'),
    url(r'^Add_Request/index/$', views.index, name='add_request_index'),
    url(r'^Add_Request/Upload/(?P<upload_type>\w+)/(?P<request_id>\d+)/$', views.upload, name="add_request_upload"),
    url(r'^Add_Request/Upload/(?P<upload_type>\w+)/$', views.upload, name="add_request_upload"),
    url(r'^Add_Request/validate/upload-files/$', views.validate_files, name="add_request_validate_files"),
    # url(r'^Add_Request/Upload/', views.upload, name="add_request_upload"),
   
    url(r'^Add_Request/GroupMapping', views.group_mapping, name="add_request_group_mapping"),
    url(r'^Add_Request/Schedular', views.Schedular, name="add_request_scheduler"),
    url(r'^Add_Request/Preview', views.Preview, name="add_request_preview"),
    url(r'^Add_Request/RequestManagement', views.requestmanagement, name="add_request_request_management"),
    url(r'^Add_Request/child', views.child, name="add_request_child"),
    url(r'^Add_Request/getUrlRequest', views.aetosGetUrlRequest, name="getUrlRequest"),
    # url(r'^Add_Request/getUrlRequest', views.getUrlRequest, name="getUrlRequest"),
    url(r'^Add_Request/AllGroupMappingDetails', views.AllGroupMappingDetails, name="AllGroupMappingDetails"), #For Pop Up Modal
    url(r'^Add_Request/ServiceRequest', views.service_request_preview, name="add_request_service_request_preview"), #For Pop Up Modal
    url(r'^Add_Request/selectMarket', views.selectMarket, name="selectMarket"),
    url(r'^Add_Request/updatePNFRecrawl', views.updatePNFRecrawl, name="updatePNFRecrawl"),
    url(r'^Add_Request/selectCategoryL1', views.selectCategoryL1, name="selectCategoryL1"),
    url(r'^Add_Request/selectCategoryL2', views.selectCategoryL2, name="selectCategoryL2"),

]

