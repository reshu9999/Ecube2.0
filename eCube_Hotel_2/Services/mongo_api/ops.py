from db_connectors import DBHandler, CacheHandler


class SPHandler(object):

    @classmethod
    def sp_Bind_grid_for_UI(cls, primry_sup__id, city_id,selected_all,primary_hotel_id,secondry_sup_id,hotel_status_id,matching_status_id):
        sp_name = 'sp_HotelMainMatch_GetSupplierHotels'
        return DBHandler.fetch_procedure_bl(sp_name, primry_sup__id, city_id,selected_all,primary_hotel_id,secondry_sup_id,hotel_status_id,matching_status_id)

    @classmethod
    def Get_data_for_match_json(cls, Country_id,city_id,primry_sup__id):
        sp_name = 'sp_GetMatchHotelfromSupplierforCountryCity'
        return DBHandler.fetch_procedure_Match(sp_name, Country_id,city_id,primry_sup__id)

    @classmethod
    def sp_Bind_grid_for_sec_popup(cls, city_id, secondry_sup_id):
        sp_name = 'sp_GetSecondarySupplierHotelsCitywise'
        return DBHandler.fetch_procedure_sec_popup(sp_name, city_id, secondry_sup_id)

    @classmethod
    def sp_update_unmatch(cls, primary_identity_id, user_id):
        sp_name = 'sp_SaveUnMatch'
        return DBHandler.update_procedure_update_unmatch(sp_name, primary_identity_id,user_id)

    @classmethod
    def sp_get_data_excel_dowwnload(cls, city_id, sup_id, type_id):
        if type_id == 1:
           sp_name = 'OfflineMatching_MatchUnmatchHotel_Supplier'
        elif type_id == 2:   
            sp_name = 'OfflineMatching_MatchUnmatchHotel_Supplier_Probable'
        elif type_id == 3:   
            sp_name = 'GetPrimaryHotelNorExcatNorProbable'
        return DBHandler.Sp_get_data_for_excel_download(sp_name, city_id, sup_id)



    @classmethod
    def sp_update_match(cls, primary_hotels__id, Sec_hotel_id,user_id):
        sp_name = 'sp_SaveExcatMatch'
        return DBHandler.update_procedure_update_match(sp_name, primary_hotels__id, Sec_hotel_id,user_id)


class CrawlOpsHandler(object):

    UNPAUSED = 0
    PAUSED = 1
    RESUMED = 2
    REPARSED = 3

    STATUS_VERBOSE = {
        UNPAUSED: 'unpaused',
        PAUSED: 'paused',
        RESUMED: 'resumed',
        REPARSED: 'reparsed'
    }

    @classmethod
    def resume_request(cls, request_id):
        DBHandler.resume_request(request_id)
        sub_requests = DBHandler.sub_requests(request_id)
        CacheHandler.resume_sub_requests(sub_requests)
        return sub_requests

    @classmethod
    def pause_request(cls, request_id):
        DBHandler.pause_request(request_id)
        sub_requests = DBHandler.sub_requests(request_id)
        CacheHandler.pause_sub_requests(sub_requests)
        return sub_requests

    @classmethod
    def reparse_request(cls, request_run_id):
        return list()

    @classmethod
    def sub_request_status(cls, request_id, sub_request_id):
        paused = CacheHandler.is_sub_request_paused(sub_request_id)
        if paused:
            DBHandler.pause_sub_request(request_id, sub_request_id)
            return cls.PAUSED
        return cls.UNPAUSED
