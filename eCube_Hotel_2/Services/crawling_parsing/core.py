from Resources.logs import PropLogger


class ServiceLogger(PropLogger):

    NAME = 'proxy_api'
    INTERVAL = 2
    INTERVAL_TYPE = 'H'
    BACKUP_COUNT = 12
    LOG_PATH = '/var/www/eCube_Hotel_2/Services/proxy_service/logs'
    PROPERTIES = [
        {'arg': 'sub_request_id', 'log': 'SRID'},
    ]


ServiceLogger.set_logger()
