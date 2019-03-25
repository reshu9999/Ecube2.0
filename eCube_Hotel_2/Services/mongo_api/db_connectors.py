import os
from flask import Flask

from resources.db_connectors import redis, MySQL, MySQLBaseHandler, RedisBaseHandler
from resources.config_coordinator import config_fetcher

mysql_config = config_fetcher.get_mysql_config
redis_config = config_fetcher.get_redis_config

mysql_conn = MySQL()
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MYSQL_DATABASE_USER'] = mysql_config['USER']
app.config['MYSQL_DATABASE_PASSWORD'] = mysql_config['PASSWORD']
app.config['MYSQL_DATABASE_DB'] = mysql_config['DB']
app.config['MYSQL_DATABASE_HOST'] = mysql_config['HOST']
mysql_conn.init_app(app)

class DBHandler(MySQLBaseHandler):
    MYSQL_CONN = mysql_conn

    @classmethod
    def resume_request(cls, request_id):
        cls.update_procedure('sp_UpdateCrawlStatusResume', request_id)

    @classmethod
    def pause_request(cls, request_id):
        cls.update_procedure('sp_UpdateCrawlStatusPause', request_id)

    @classmethod
    def pause_sub_request(cls, request_id, sub_request_id):
        cls.update_procedure('sp_UpdateCrawlSubRequestStatusPause', request_id, sub_request_id)

    @classmethod
    def sub_requests(cls, request_id):
        return [db_obj[0] for db_obj in cls.fetch_procedure('sp_GetNonPausedSubRequests', request_id)]

    @classmethod
    def fetch_procedure_bl(cls, sp_name, primry_sup__id, city_id,selected_all,primary_hotel_id,secondry_sup_id,hotel_status_id,matching_status_id):
        return cls.fetch_procedure(sp_name, primry_sup__id, city_id,selected_all,primary_hotel_id,secondry_sup_id,hotel_status_id,matching_status_id)

    @classmethod
    def fetch_procedure_Match(cls, sp_name, Country_id,city_id,primry_sup__id):
        return cls.fetch_procedure(sp_name, Country_id,city_id,primry_sup__id)

    @classmethod
    def fetch_procedure_sec_popup(cls, sp_name,city_id, secondry_sup_id):
        return cls.fetch_procedure(sp_name, city_id, secondry_sup_id)

    @classmethod
    def update_procedure_update_unmatch(cls, sp_name, primary_identity_id, user_id):
        return cls.SP_all_operation_for_update_unmatch(sp_name, primary_identity_id, user_id)

    @classmethod
    def update_procedure_update_match(cls, sp_name, primary_hotels_id, Sec_hotel_id,user_id):
        return cls.SP_all_operation_for_update_match(sp_name, primary_hotels_id, Sec_hotel_id,user_id)
    
    @classmethod
    def Sp_get_data_for_excel_download(cls, sp_name, city_id, sup_id):
        return cls.fetch_procedure(sp_name, city_id, sup_id)


class CacheHandler(RedisBaseHandler):
    NAMESPACE = 'crawl_ops'
    HOST = redis_config['HOST']
    PORT = redis_config['PORT']
    DB = 2
    POOL = redis.ConnectionPool(host=HOST, port=PORT, db=DB)
    SET_BATCH_SIZE = 5000

    @classmethod
    def resume_sub_requests(cls, sub_requests):
        for sub_req in sub_requests:
            cls.delete_key(sub_req)

    @classmethod
    def pause_sub_requests(cls, sub_requests, batch_size=None):
        if batch_size == 0:
            for sub_req in sub_requests:
                cls.set_key(sub_req, 'paused')
        else:
            cls.batch_set_keys({key: 'paused' for key in sub_requests}, batch_size)

    @classmethod
    def is_sub_request_paused(cls, sub_request_id):
        exists = cls.key_exists(sub_request_id)
        if exists:
            cls.delete_key(sub_request_id)
        return exists
