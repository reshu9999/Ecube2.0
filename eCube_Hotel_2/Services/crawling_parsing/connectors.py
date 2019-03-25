from settings import CONFIG
from core import ServiceLogger

from Resources.connections import MySQLBaseHandler

REDIS_CONFIG = CONFIG.get_redis_config


class MySQL(MySQLBaseHandler):

    FETCH_SP = 'aetos_sub_request_input'

    def __init__(self):
        super().__init__(*CONFIG.get_pymysql_args)

    def get_sub_request_input(self, sub_request_id):
        ServiceLogger.info_log('Fetching from SP:%s' % self.FETCH_SP, sub_request_id)
        return self.fetch_from_procedure(self.FETCH_SP, sub_request_id)[0]
