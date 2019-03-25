from django.conf.urls import url

from hotel.user_management import views as hotel_user_management_views

urlpatterns = [
    url(r'^user-management/index/$', view=hotel_user_management_views.create_account,
        name='hotel_user_management_index'),

    url(r'^user-management/bind-grid/$', view=hotel_user_management_views.bind_grid,
        name='hotel_user_management_bind_grid'),

    url(r'^user-management/account-ops/$', view=hotel_user_management_views.account_ops,
        name='hotel_user_management_account_ops'),

    url(r'^user-management/account-delete/$', view=hotel_user_management_views.delete_account,
        name='hotel_user_management_delete_account'),

    url(r'^user-management/account-edit/$', view=hotel_user_management_views.edit_account,
        name='hotel_user_management_edit_account'),

    url(r'^user-management/user-edit/$', view=hotel_user_management_views.update_account,
        name='hotel_user_management_update_account'),

    url(r'^user-management/user-role-data/$', view=hotel_user_management_views.load_role_data,
        name='hotel_user_management_load_role_data'),

    url(r'^user-management/user-bind-permissions/$', view=hotel_user_management_views.bind_user_permissions,
        name='hotel_user_management_bind_user_permissions'),

    url(r'^user-management/user-exists/$', view=hotel_user_management_views.user_exists_check,
        name='hotel_user_management_user_exists_check'),

    url(r'^user-management/reset-password/$', view=hotel_user_management_views.Reset_Password,
        name='hotel_user_management_reset_password'),

    url(r'^email-management/email-exists/$', view=hotel_user_management_views.email_exists_check,
        name='hotel_user_management_email_exists_check'),

    url(r'^email-management/competitor-bind-market/$', view=hotel_user_management_views.bind_competitor_market,
        name='hotel_user_management_bind_competitor_market'),

    url(r'^user-management/confirm-reset-password/(?P<token>[\w-]+)/$', view=hotel_user_management_views.Confirm_Reset_Password,
        name='hotel_user_management_confirm_reset_password')
        
]
