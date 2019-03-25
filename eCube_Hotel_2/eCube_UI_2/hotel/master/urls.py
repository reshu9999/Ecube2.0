from django.conf.urls import url
from hotel.master import views

urlpatterns = [
    # # MASTER URLS
    url(r'^master/$', views.master_index, name='master_index'),
    url(r'^master/country/$',views.master_country,name='master_country'),
    url(r'^master/cities/$',views.master_cities,name='master_cities'),
    url(r'^master/airport/$',views.master_airport,name='master_airport'),
    url(r'^master/board/$',views.master_board,name='master_board'),
    url(r'^master/hotelgrp/$',views.master_hotelgrp,name='master_hotelgrp'),
    url(r'^master/pos/$',views.master_pos,name='master_pos'),
    url(r'^master/hotel/$',views.master_hotel,name='master_hotel'),
    url(r'^master/Hotel_master_upload_excel/$',views.Hotel_master_upload_excel,name='Hotel_master_upload_excel'),
    url(r'^master/Bind_Hotel_master_name/$',views.Bind_Hotel_master_name,name='Bind_Hotel_master_name'),
    url(r'^master/Bind_city_master_name/$',views.Bind_city_master_name,name='Bind_city_master_name'),
    url(r'^master/Delete_City_master_name/$',views.Delete_City_master_name,name='Delete_City_master_name'),
    url(r'^master/Delete_Country_master_name/$',views.Delete_Country_master_name,name='Delete_Country_master_name'),
    url(r'^master/Bind_Country_master_name/$',views.Bind_Country_master_name,name='Bind_Country_master_name'),
    url(r'^master/Bind_POS_master_name/$',views.Bind_POS_master_name,name='Bind_POS_master_name'),
    url(r'^master/Bind_board_master_name/$',views.Bind_board_master_name,name='Bind_board_master_name'),
    url(r'^master/Bind_airport_master_name/$',views.Bind_airport_master_name,name='Bind_airport_master_name'),
    url(r'^master/Delete_Airport_master_name/$',views.Delete_Airport_master_name,name='Delete_Airport_master_name'),
    url(r'^master/Delete_Board_master_name/$',views.Delete_Board_master_name,name='Delete_Board_master_name'),
    url(r'^master/Delete_POS_master_name/$',views.Delete_POS_master_name,name='Delete_POS_master_name'),


    url(r'^master/Bind_Hotel_master_country_name/$',views.Bind_Hotel_master_country_name,name='Bind_Hotel_master_country_name'),
    url(r'^master/Bind_Hotel_master_city_name/$',views.Bind_Hotel_master_city_name,name='Bind_Hotel_master_city_name'),
    url(r'^master/update_Hotel_master/$',views.update_Hotel_master,name='update_Hotel_master'),
    url(r'^master/Add_New_Hotel_master/$',views.Add_New_Hotel_master,name='Add_New_Hotel_master'),
    url(r'^master/Delete_Hotel_master_name/$',views.Delete_Hotel_master_name,name='Delete_Hotel_master_name'),
    url(r'^master/Pos_master_upload_excel/$',views.Pos_master_upload_excel,name='Pos_master_upload_excel'),
    url(r'^master/City_master_upload_excel/$',views.City_master_upload_excel,name='City_master_upload_excel'),
    url(r'^master/Country_master_upload_excel/$',views.Country_master_upload_excel,name='Country_master_upload_excel'),

    url(r'^master/Download_hotel/$', views.Download_hotel_master, name='Download_Hotel_master'),
    url(r'^master/Bind_sup_name_by_city/$', views.Bind_sup_name_by_city, name='Bind_sup_name_by_city'),
    ]


