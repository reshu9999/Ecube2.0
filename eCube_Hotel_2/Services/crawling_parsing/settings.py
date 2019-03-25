from Resources.config_fetcher import ConfigFetcherFile


class ServiceConfigFetcher(ConfigFetcherFile):

    CONFIGS = [
        'MYSQL',
        'REDIS'
    ]

    FILEPATH = '/var/www/eCube_Hotel_2/Services/proxy_service/config_data.json'

    @property
    def get_pymysql_args(self):
        CONFIG = self.get_mysql_config
        return CONFIG['HOST'], CONFIG['USER'], CONFIG['PASSWORD'], CONFIG['DB']


CONFIG = ServiceConfigFetcher('proxy_service')

