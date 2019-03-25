from django.conf.urls import url
from hotel import views
from hotel.master import urls as master_urls
from hotel.Notification import urls as Notification_urls
from hotel.Proxy import urls as Proxy_urls
from hotel.Domain import urls as Domain_urls
from hotel.user_login import urls as login_urls
from hotel.user_management import urls as user_management_urls
from hotel.req_management import urls as req_management_urls
from hotel.DashBoard import urls as db

urlpatterns = [
    url(r'^index/(?P<request_id>\w+)$', views.index, name='hotel_create_request'),
    url(r'^index/$', views.index, name='hotel_create_request'),
    url(r'^download/$', views.download, name='batchschedule_download'),
    url(r'^download/batch-input-upload-hotel', views.batch_upload_template_hotel, name='hotel_batch_input_upload_template_hotel'),
    url(r'^download/batch-input-upload-flight', views.batch_upload_template_flight, name='hotel_batch_input_upload_template_flight'),
    url(r'^ajax/batch-input-upload-hotel', views.batch_input_upload_hotel, name='hotel_batch_input_upload_hotel'),
    url(r'^ajax/batch-input-upload-flight', views.batch_input_upload_flight, name='hotel_batch_input_upload_flight'),

    url(r'^BindCities', views.BindCities, name='hotel_bind_cities'),
    url(r'^SaveRequest', views.HotelSaveRequest, name='hotel_save_request'),
    url(r'^BindHotels', views.BindHotels, name='hotel_bind_hotels'),
    url(r'^allHotels', views.allHotels, name='hotel_all_bind_hotels'),
    url(r'^FlightBindHotels', views.FlightBindHotels, name='flight_bind_hotels'),

    url(r'^Delete/$', views.HotelDeleteRequest, name='hotel_delete_request'),
    url(r'^Delete/all/$', views.HotelDeleteRequestAll, name='hotel_delete_request_all'),
    url(r'^Schedular/$', views.Schedular, name='add_request_scheduler'),
    url(r'^Schedular/email/$', views.emailSave, name='emailSave'),

    url(r'^Schedular/(?P<request_id>\d+)$', views.Schedular, name='add_request_scheduler'),

    url(r'^hotel/hoteltypedownload', views.hoteltype_download, name='hotel_typedownload'),
    url(r'^hotelPlus/save', views.FlightSaveRequest, name='Rflight_save_request'),
    url(r'^hotelPlus/$', views.hotel_plus_flight_index, name='hotel_plus_flight_request'),
    url(r'^hotelPlus/(?P<request_id>\w+)$', views.hotel_plus_flight_index, name='hotel_plus_flight_request'),
    url(r'^hotelPlus/flyCities/$', views.BindCities, name='flight_bind_cities'),
    url(r'^hotelPlus/flyAirports/$', views.BindAirports, name='flight_bind_airports'),
   
    url(r'^hotelPlus/delete', views.FlightDeleteRequest, name='Rflight_delete_request'),
    url(r'^Keyword_n_rule', views.keywordRule, name='Keyword_n_rule'),
    url(r'^download_hotel_splchar', views.downloadhotelSpecialChar, name='download_hotel_splchar'),
    url(r'^insertrule', views.insertRule, name='insertRule'),
    url(r'^export/csv/$', views.export_data_csv, name='export_data_csv'),
    url(r'^searchexport/csv/$', views.search_export_data_csv, name='search_export_data_csv'),
    url(r'^search_export_data_csv_standard/$', views.search_export_data_csv_standard, name='search_export_data_csv_standard'),

    url(r'^hotel_plus_hotels/hotelsupload', views.Hotels_Specific, name='hotels_specific_upload'),
    url(r'^hotel_plus_hotels/editreq', views.EditReq, name='editrequest'),
    url(r'^hotel_plus_hotels/stopreq', views.StopReq, name='stoprequest'),

    # vikash code

    # url(r'^Hotel/index$', views.index, name='hotel_create_request'),
    url(r'^match_n_unmatch_download$', views.match_n_unmatch_download, name='match_n_unmatch_download'),
    url(r'^match_n_unmatch', views.match_n_unmatch, name='match_n_unmatch'),
    url(r'^Bind_request_and_batch_name', views.Bind_request_and_batch_name, name='Bind_request_and_batch_name'),
    url(r'^group_creation/$', views.group_creation, name='group_creation'),
    url(r'^Bind_Country_name/$', views.Bind_Country_name, name='Bind_Country_name'),
    url(r'^Bind_city_name/$', views.Bind_city_name, name='Bind_city_name'),
    url(r'^lead_time_upload$', views.lead_time_upload, name='lead_time_upload'),
    url(r'^File_upload_excel_lead_time/$', views.File_upload_excel_lead_time, name='File_upload_excel_lead_time'),
    url(r'^File_download_excel_lead_time/$', views.File_download_excel_lead_time, name='File_download_excel_lead_time'),
    url(r'^Fgrid_bind_lead_time/$', views.Fgrid_bind_lead_time, name='Fgrid_bind_lead_time'),
    url(r'^Bind_hotel_name/$', views.Bind_hotel_name, name='Bind_hotel_name'),
    url(r'^push_to_staging/$', views.push_to_staging, name='push_to_staging'),
    url(r'^Db_push_stag_stopped/$', views.Db_push_stag_stopped, name='Db_push_stag_stopped'),
    url(r'^Push_tostg_db_save/$', views.Push_tostg_db_save, name='Push_tostg_db_save'),
    url(r'^Db_push_to_stag_prio_update/$', views.Db_push_to_stag_prio_update, name='Db_push_to_stag_prio_update'),
    url(r'^Match_unmatch_Bind_hotel_name/$', views.Match_unmatch_Bind_hotel_name, name='Match_unmatch_Bind_hotel_name'),
    url(r'^DBind_hotel_name_by_sup/$', views.DBind_hotel_name_by_sup, name='DBind_hotel_name_by_sup'),
    url(r'^Save_htls_details/$', views.Save_htls_details, name='Save_htls_details'),
    url(r'^Bind_grid_by_search/$', views.Bind_grid_by_search, name='Bind_grid_by_search'),
    url(r'^Bind_request_and_sup_name_by_request_id/$', views.Bind_request_and_sup_name_by_request_id, name='Bind_request_and_sup_name_by_request_id'),
    url(r'^delete_grp_details/$', views.delete_grp_details, name='delete_grp_details'),
    url(r'^File_upload_excel/$', views.File_upload_excel, name='File_upload_excel'),
    url(r'^chk_grp_name/$', views.chk_grp_name, name='chk_grp_name'),
    url(r'^Bind_hotel_name_for_update/$', views.Bind_hotel_name_for_update, name='Bind_hotel_name_for_update'),
    url(r'^Update_hotel_list/$', views.Update_hotel_list, name='Update_hotel_list'),
    url(r'^autoComplete_hotels/$', views.autoComplete_hotels, name='autoComplete_hotels'),
    url(r'^Bind_city_name_by_sup/$', views.Bind_city_name_by_sup, name='Bind_city_name_by_sup'),
    url(r'^download_excel_match_n_match/$', views.download_excel_match_n_match, name='download_excel_match_n_match'),
    url(r'^map_group_domain/$', views.map_group_domain, name='map_group_domain'),
    url(r'^f_delete_grp_mapp_detail/$', views.f_delete_grp_mapp_detail, name='f_delete_grp_mapp_detail'),
    url(r'^f_Bind_grp_mapp_detail/$', views.f_Bind_grp_mapp_detail, name='f_Bind_grp_mapp_detail'),
    url(r'^f_Save_grp_detail/$', views.f_Save_grp_detail, name='f_Save_grp_detail'),
    url(r'^f_get_email_by_req_id/$', views.f_get_email_by_req_id, name='f_get_email_by_req_id'),
    url(r'^f_get_grp_mapp_detail/$', views.f_get_grp_mapp_detail, name='f_get_grp_mapp_detail'),
    url(r'^Bind_grid_push_to_Stagging/$', views.Bind_grid_push_to_Stagging, name='Bind_grid_push_to_Stagging'),
    url(r'^matach_unmatch_upload_excel/$', views.matach_unmatch_upload_excel, name='matach_unmatch_upload_excel'),

    
] + master_urls.urlpatterns + Notification_urls.urlpatterns +Domain_urls.urlpatterns+  Proxy_urls.urlpatterns+  login_urls.urlpatterns + user_management_urls.urlpatterns + req_management_urls.urlpatterns + db.urlpatterns + [
    url(r'^', views.index, name='hotel_create_request_index')
]
