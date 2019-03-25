from ops import CrawlOpsHandler, SPHandler
from resources.responses import AetosBaseResponse
import pandas as pd
import os
import pymysql
from datetime import datetime

from flask import Flask, request, Response, json, make_response, request, current_app,send_from_directory


class AetosResponse(AetosBaseResponse):
    RESPONSE = Response


app = Flask(__name__)


@app.route('/api/v1/sample/request', methods=['GET'])
def sample_request():
    return AetosResponse.success_api_response({'message': 'great success!!!'})


@app.route('/api/v1/sample/test', methods=['GET'])
def api_test():
    return AetosResponse.success_api_response({'message': 'Api working properly', 'new_data': 'done'})


@app.route('/api/v1/sample/sp_Bind_grid_for_UI', methods=['POST'])
def sp_Bind_grid_for_UI():
    request_body = request.form
    primry_sup__id = request_body['primry_sup__id']
    city_id = request_body['city_id']
    selected_all = request_body['selected_all']
    primary_hotel_id = request_body['primary_hotel_id']
    secondry_sup_id = request_body['secondry_sup_id']
    hotel_status_id = request_body['hotel_status_id']
    matching_status_id = request_body['matching_status_id']
    # print (matching_status_id)
    # print (primry_sup__id, city_id,primary_hotel_id,secondry_sup_id,hotel_status_id,matching_status_id)
    data = SPHandler.sp_Bind_grid_for_UI(primry_sup__id, city_id,selected_all,primary_hotel_id,secondry_sup_id,hotel_status_id,matching_status_id)
    return AetosResponse.success_api_response({'data': data})


@app.route('/api/v1/sample/Get_data_for_match_json', methods=['GET'])
def Get_data_for_match_json():
    request_body = request.args
    primry_sup__id = request_body['secondary_sup_name']
    city_id = request_body['city_name']
    Country_id = request_body['Country_name']
    data = SPHandler.Get_data_for_match_json(Country_id,city_id,primry_sup__id)
    list1 = []
    dict1 = {}
    for Sp_res in data:
        dict1 = {"Hotel_relation_Id": Sp_res[0], "Hotel_Id": Sp_res[1], "ID": Sp_res[2], "Name": Sp_res[3],
                 "Hotel_Name": Sp_res[4], "WebSite_Hotel_ID": Sp_res[5], "Hotel_Addres_1": Sp_res[6],
                 "Hotel_Addres_2": Sp_res[7], "CompHotel": Sp_res[8], "CompHotel_Address_1": Sp_res[9],
                 "CompHotel_Address_2": Sp_res[10],"Hotel_Relation_comp_Hotel_ID": Sp_res[11],"Comp_supplier_Id": Sp_res[12],
                  "Comp_Supplier_Name": Sp_res[13],"Is_Hotel_Relation_Manual_Match": Sp_res[14],"Created_By": Sp_res[15],
                  "Admin_User_Id": Sp_res[16],"City_ID": Sp_res[17],"City_Name": Sp_res[18], 
                  "Country_Id": Sp_res[19],"Country_Name": Sp_res[20],"Comp_city_Id": Sp_res[21], 
                  "Comp_city_Name": Sp_res[22],"Comp_Country_ID": Sp_res[23],"Comp_Country_Name": Sp_res[24],"Last_appreance_Date": Sp_res[25]
                 }
        list1.append(dict1)
    if len(list1) > 0:
        return AetosResponse.success_api_response({'data': list1, 'count': len(data)})
    else:
        return AetosResponse.success_api_response({'data': list1, 'count': 0})
    



@app.route('/api/v1/sample/sp_update_match_unmatch_frm_UI', methods=['GET'])
def sp_update_match_unmatch_frm_UI():
    request_body = request.args
    # for match
    Sec_sup__id_match = request_body['Sec_sup__id_match'].split(',')
    prim_htls_id = request_body['primary_htls_id'].split(',')
   
    # for unmatch 
    primary_sup__id_unmatch = request_body['primary_sup__id_unmatch'].split(',')
   
    Session_id =request_body['Session_id']
    # for unmatch
    if len(primary_sup__id_unmatch) > 0  and   not primary_sup__id_unmatch == ['']:
        # print('first call')
        # print(primary_sup__id_unmatch)
        for i in primary_sup__id_unmatch:
            SPHandler.sp_update_unmatch(i, Session_id)
            
    # for match
    if len(prim_htls_id) > 0   and   not prim_htls_id == ['']:
        # print('second call')
        # print (prim_htls_id)
        # print (Sec_sup__id_match)
        for i, x in enumerate(prim_htls_id):
            SPHandler.sp_update_match(x, Sec_sup__id_match[i], Session_id)
           


    # data = SPHandler.sp_Bind_grid_for_UI(primry_sup__id, city_id,primary_hotel_id,secondry_sup_id,hotel_status_id,matching_status_id)
    data = "done"
    # from django.http import JsonResponse
    # return JsonResponse(data, safe=False)
    return AetosResponse.success_api_response({'data': data})



@app.route('/api/v1/sample/sp_Bind_grid_for_Sec_popup', methods=['GET'])
def sp_Bind_grid_for_Sec_popup():
    request_body = request.args
    city_id = request_body['city_id']
    secondry_sup_id = request_body['secondry_sup_id']
    data = SPHandler.sp_Bind_grid_for_sec_popup(city_id, secondry_sup_id)
    return AetosResponse.success_api_response({'data': data})


@app.route('/api/v1/sample/unmatched_sp_Bind_grid_for_match_unmatch_download_excel', methods=['POST'])
def unmatched_sp_Bind_grid_for_match_unmatch_download_excel():
    request_body = request.form
    city_id = request_body['city_id']
    secondry_sup_id = request_body['secondry_sup_id']
    radio_id= request_body['radio_id']
    if (radio_id == 'exact_match') :
        data = SPHandler.sp_get_data_excel_dowwnload(city_id, secondry_sup_id,1)
    elif (radio_id =='probable_match') :
        data = SPHandler.sp_get_data_excel_dowwnload(city_id, secondry_sup_id,2)
    elif (radio_id =='unmatch_data') :
        data = SPHandler.sp_get_data_excel_dowwnload(city_id, secondry_sup_id ,3)
    # list1 = []
    # dict1 = {}
    # for Sp_res in data:
    #     dict1 = {"ID": Sp_res[0], "code": Sp_res[1], "Primary_hotel_id": Sp_res[2], "Primary_hotel_name": Sp_res[3],
    #              "Primary_hotel_Address": Sp_res[4], "sup_id": Sp_res[5], "sup_name": Sp_res[6],
    #              "Date": Sp_res[7], "long": Sp_res[8], "lat": Sp_res[9]}
    #     list1.append(dict1)
        # print (list1)
    if len(data) > 0:
        return AetosResponse.success_api_response({'data': data, 'count': len(data)})
    else:
        return AetosResponse.success_api_response({'data': data, 'count': 0})


@app.route('/api/v1/sample/sp_Bind_grid_for_Sec_popup_for_excel', methods=['GET'])
def sp_Bind_grid_for_Sec_popup_for_excel():
    request_body = request.args
    city_id = request_body['city_id']
    secondry_sup_id = request_body['secondry_sup_id']
    radio_id= request_body['radio_id']
    list1 = []
    dict1 = {}
    path ='0'
    if (radio_id == 'exact_match') :
        data = SPHandler.sp_get_data_excel_dowwnload(city_id, secondry_sup_id,1)
        file_name ='output_excel_Exact_%s' % datetime.now() + ''

        for Sp_res in data:
            dict1 = {"Secondary Supplier Company": Sp_res[0], 
                     "Primary Supplier Hotel Id": Sp_res[1], 
                     "Primary Supplier Hotel code": Sp_res[2], 
                     "Primary Supplier Hotel Name": Sp_res[3], 
                     "Primary supplier Hotel Status": Sp_res[4], 
                     "Primary Supplier Hotel Address": Sp_res[5], 
                     "Primary Supplier Hotel Star": Sp_res[6], 
                     "Primary Supplier Longitude": Sp_res[7], 
                     "Primary Supplier Latitude": Sp_res[8], 
                     "Secondary Supplier Hotel Id": Sp_res[9], 
                     "Secondary Website Hotel Id": Sp_res[10],  

                     "Secondary Supplier Hotel Name": Sp_res[11], 
                     "Secondary Supplier Hotel Address": Sp_res[12], 
                     "Secondary Supplier Hotel Star": Sp_res[13],  
                     "Secondary Supplier Longitude": Sp_res[14],
                     "Secondary Supplier Latitude": Sp_res[15], 
                     "Destination Code": Sp_res[16], 
                     "City": Sp_res[17],
                     "Country": Sp_res[18],  
                     "Matching Type": Sp_res[19],  
                     "Added On (Secondary Supplier)": Sp_res[20],  
                     "Matched On": Sp_res[21], 
                     "Secondary Hotel Last Appearance": Sp_res[22], 
                     "Primary Hotel Last Appearance": Sp_res[23], 
                     "Secondary Supplier Zone Name": Sp_res[24] }
            list1.append(dict1)
        
   

        if len(list1) > 0:
            df = pd.DataFrame(list1)
            time = file_name
            path = '/var/www/eCube_Hotel_2/Services/media/Download_excel/%s' % time + '.xlsx'
            writer = pd.ExcelWriter(path)
            df.to_excel(writer, 'Sheet1', columns=["Secondary Supplier Company", "Primary Supplier Hotel Id", "Primary Supplier Hotel code", "Primary Supplier Hotel Name", "Primary Hotel Status", "Primary Supplier Hotel Address", "Primary Supplier Hotel Star", "Primary Supplier Longitude", "Primary Supplier Latitude", "Secondary Supplier Hotel Id", "Secondary Website Hotel Id", "Secondary Supplier Hotel Name", "Secondary Supplier Hotel Address", "Secondary Supplier Hotel Star", "Secondary Supplier Longitude", "Secondary Supplier Latitude", "Destination Code", "City", "Country", "Matching Type", "Added On (Secondary Supplier)", "Matched On", "Secondary Hotel Last Appearance", "Primary Hotel Last Appearance", "Secondary Supplier Zone Name"], index=False)
            writer.save()
            path = '/media/%s' % time + '.xlsx'
        return AetosResponse.success_api_response({'data': list1, 'path': path})


    elif (radio_id =='probable_match') :
        data = SPHandler.sp_get_data_excel_dowwnload(city_id, secondry_sup_id,2)
        file_name ='output_excel_Prob_%s' % datetime.now() + ''




        for Sp_res in data:
            dict1 = {"Secondary Supplier Company": Sp_res[0],
                     "Primary Supplier Hotel Id": Sp_res[1], 
                     "Primary Supplier Hotel code": Sp_res[2], 
                     "Primary Supplier Hotel Name": Sp_res[3], 
                     "Primary Supplier Hotel Status": Sp_res[4],
                     "Primary Supplier Hotel Address": Sp_res[5], 
                     "Primary Supplier Hotel Star": Sp_res[6],
                     "Primary Supplier Longitude": Sp_res[7], 
                     "Primary Supplier Latitude": Sp_res[8], 
                     "Secondary Supplier Hotel Id": Sp_res[9], 
                     "Secondary Website Hotel Id": Sp_res[10], 
                     "Secondary Supplier Hotel Name": Sp_res[11], 
                     "Secondary Supplier Hotel Address": Sp_res[12], 
                     "Secondary Supplier Hotel Star": Sp_res[13], 
                     "Secondary Supplier Longitude": Sp_res[14],
                     "Secondary Supplier Latitude": Sp_res[15], 
                     "Destination Code": Sp_res[16], 
                     "City": Sp_res[17],
                     "Country": Sp_res[18], 
                     "Matching Type": Sp_res[19], 
                     "Added On (Secondary Supplier)": Sp_res[20],
                     "Matched On": Sp_res[21], 
                     "Secondary Hotel Last Appearance": Sp_res[22], 
                     "Primary Hotel Last Appearance": Sp_res[23], 
                     "Matching Score (%)": Sp_res[24], 
                     "Primary Matched Exist": Sp_res[25], 
                     "Secondary Matched Exist": Sp_res[26], 
                     "Secondary Supplier Zone Name": Sp_res[27] }
            list1.append(dict1)
        
   

        if len(list1) > 0:
            df = pd.DataFrame(list1)
            time = file_name
            path = '/var/www/eCube_Hotel_2/Services/media/Download_excel/%s' % time + '.xlsx'
            writer = pd.ExcelWriter(path)
            df.to_excel(writer, 'Sheet1', columns=["Secondary Supplier Company", "Primary Supplier Hotel Id", "Primary Supplier Hotel code", "Primary Supplier Hotel Name", "Primary Supplier Hotel Status", "Primary Supplier Hotel Address", "Primary Supplier Hotel Star", "Primary Supplier Longitude", "Primary Supplier Latitude", "Secondary Supplier Hotel Id", "Secondary Website Hotel Id", "Secondary Supplier Hotel Name", "Secondary Supplier Hotel Address", "Secondary Supplier Hotel Star", "Secondary Supplier Longitude", "Secondary Supplier Latitude", "Destination Code", "City", "Country", "Matching Type", "Added On (Secondary Supplier)", "Matched On", "Secondary Hotel Last Appearance", "Primary Hotel Last Appearance", "Matching Score (%)", "Primary Matched Exist", "Secondary Matched Exist", "Secondary Supplier Zone Name"], index=False)
            writer.save()
            path = '/media/%s' % time + '.xlsx'
        return AetosResponse.success_api_response({'data': list1, 'path': path})
    elif (radio_id =='unmatch_data') :
        data = SPHandler.sp_get_data_excel_dowwnload(city_id, secondry_sup_id ,3)
        file_name ='output_excel_Unmatch_%s' % datetime.now() + ''

        for Sp_res in data:
            dict1 = {"SecondarySupplierName": Sp_res[0], "PrimarySupplierName": Sp_res[1], "PrimaryHotelId": Sp_res[2], "PrimaryHotelName": Sp_res[3], "HotelStatus": Sp_res[4],
                    "PrimaryHotelCode": Sp_res[5], "Longitude": Sp_res[6], "Latitude": Sp_res[7],
                    "City": Sp_res[8], "DestinationCode": Sp_res[9], "Country": Sp_res[10], "PrimaryHotelAddress": Sp_res[11], "LastAppearance": Sp_res[12]}
            list1.append(dict1)
        
   

        if len(list1) > 0:
            df = pd.DataFrame(list1)
            time = file_name
            path = '/var/www/eCube_Hotel_2/Services/media/Download_excel/%s' % time + '.xlsx'
            writer = pd.ExcelWriter(path)
            df.to_excel(writer, 'Sheet1', columns=['SecondarySupplierName', 'PrimarySupplierName', 'PrimaryHotelId', 'PrimaryHotelName', 'HotelStatus', 'PrimaryHotelCode', 'Longitude', 'Latitude', 'City', 'DestinationCode', 'Country', 'PrimaryHotelAddress', 'LastAppearance'], index=False)
            writer.save()
            path = '/media/%s' % time + '.xlsx'
        return AetosResponse.success_api_response({'data': list1, 'path': path})
    else:
        return AetosResponse.success_api_response({'data': list1, 'path': 0})





@app.route('/api/v1/request/resume', methods=['POST'])
def resume_request():
    request_body = request.get_json()
    request_id = request_body['RequestID']

    sub_reqs = CrawlOpsHandler.resume_request(request_id)

    response = {'sub_requests': sub_reqs, 'status': CrawlOpsHandler.STATUS_VERBOSE[CrawlOpsHandler.RESUMED]}
    return AetosResponse.success_api_response(response)


@app.route('/api/v1/request/pause', methods=['POST'])
def pause_request():
    request_body = request.get_json()
    request_id = request_body['RequestID']

    sub_reqs = CrawlOpsHandler.pause_request(request_id)

    response = {'sub_requests': sub_reqs, 'status': CrawlOpsHandler.STATUS_VERBOSE[CrawlOpsHandler.PAUSED]}
    return AetosResponse.success_api_response(response)


@app.route('/api/v1/request-run/reparse', methods=['POST'])
def reparse_request():
    request_body = request.get_json()
    request_run_id = request_body['RequestRunID']

    sub_reqs = CrawlOpsHandler.reparse_request(request_run_id)

    response = {'sub_requests': sub_reqs, 'status': CrawlOpsHandler.STATUS_VERBOSE[CrawlOpsHandler.REPARSED]}
    return AetosResponse.success_api_response(response)


@app.route('/api/v1/sub-request/status', methods=['POST'])
def sub_request_status():
    request_body = request.get_json()
    request_id = request_body['RequestID']
    sub_request_id = request_body['SubRequestID']

    sub_req_status = CrawlOpsHandler.sub_request_status(request_id, sub_request_id)

    response = {'sub_request_id': sub_request_id, 'status': CrawlOpsHandler.STATUS_VERBOSE[sub_req_status]}
    return AetosResponse.success_api_response(response)

@app.route('/media/<filename>')
def downloadTestFile(filename):
    return send_from_directory('/var/www/eCube_Hotel_2/Services/media/Download_excel/', filename)

if(__name__ == '__main__'):
    app.run(debug=True, port=5002)
