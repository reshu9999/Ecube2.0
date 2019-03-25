from django.conf.urls import url

from hotel.req_management import views as hotel_req_management_views

urlpatterns = [
    url(r'^request-management/index/$', view=hotel_req_management_views.request_management,
        name='hotel_request_management_index'),
    url(r'^request-management/popup/$', view=hotel_req_management_views.request_management_popup,
        name='request_management_popup'),
    url(r'^request-management/edit-req/$', view=hotel_req_management_views.edit_request_router,
        name='hotel_request_management_edit_request_router'),
    url(r'^File_download_excel_req_man$', view=hotel_req_management_views.File_download_excel_req_man,
        name='File_download_excel_req_man'),
    url(r'^download_pnf_excel/$', view=hotel_req_management_views.download_pnf_excel,
        name='download_pnf_excel'),
    url(r'^download_psfail_excel/$', view=hotel_req_management_views.download_psfail_excel,
        name='download_psfail_excel'),
    url(r'^Pnf_Recrwal$', view=hotel_req_management_views.Pnf_Recrwal,
        name='Pnf_Recrwal'),
    url(r'^Bind_modal$', view=hotel_req_management_views.Bind_modal,
        name='Bind_modal'),
    url(r'^Bind_Second_modal$', view=hotel_req_management_views.Bind_Second_modal,
        name='Bind_Second_modal'),

    url(r'^Recrwal$', view=hotel_req_management_views.Recrwal,
        name='Recrwal'),

    url(r'^Sub_Recrwal$', view=hotel_req_management_views.Sub_Recrwal,
        name='Sub_Recrwal'),

    url(r'^File_download_excel_req_man_mongo$', view=hotel_req_management_views.File_download_excel_req_man_mongo,
        name='File_download_excel_req_man_mongo'),

    url(r'^api/v1/request-management/reparse-request-run/(?P<request_run_id>\w+)$',
        view=hotel_req_management_views.reparse_request_run,
        name='hotel_request_management_reparse_request_run'),

    url(r'^api/v1/request-management/reparse-sub-request/(?P<request_run_id>\w+)/(?P<sub_request_id>\w+)$',
        view=hotel_req_management_views.reparse_sub_request,
        name='hotel_request_management_reparse_sub_request'),

    url(r'^api/v1/request-management/pause-request-run/(?P<request_run_id>\w+)$',
        view=hotel_req_management_views.pause_request_run,
        name='hotel_request_management_pause_request_run'),

    url(r'^api/v1/request-management/resume-request-run/(?P<request_run_id>\w+)$',
        view=hotel_req_management_views.resume_request_run,
        name='hotel_request_management_resume_request_run'),

    url(r'^api/v1/request-management/stop-request-run/(?P<request_run_id>\w+)$',
        view=hotel_req_management_views.stop_request_run,
        name='hotel_request_management_stop_request_run'),

    url(r'^api/v1/request-management/delete-request-schedule/(?P<request_id>\w+)$',
        view=hotel_req_management_views.delete_request_schedule,
        name='hotel_request_management_stop_request_run'),

    url(r'^fetch_request$', view=hotel_req_management_views.fetch_request,
        name='fetch_request'),
]
