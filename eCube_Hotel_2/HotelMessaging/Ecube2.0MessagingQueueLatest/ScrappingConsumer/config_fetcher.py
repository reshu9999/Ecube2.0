class ConfigFetcher(object):

    HOST = 'localhost/config'
    VERSION = 'api/v1'
    PATH = 'service/%s/config'

    def __init__(self, service_name):
        self.service_name = service_name
        self._config = None
        self.config_url = 'http://%s/%s/%s/' % (self.HOST, self.VERSION, self.PATH % self.service_name)

    @property
    def get_config(self):
        import requests
        if self._config is not None:
            return self._config

        try:
            config_response = requests.get(self.config_url).json()['data']['config']
        except Exception as e:
            print("Could not load config")
            print(e)
            config_response = {
                # "MONGODB": {
                #     "URL": "mongodb://192.168.8.69:27017"
                # },
                "MONGODB": {
                    "URL": "mongodb://192.168.8.51:27017"
                },
                # "MYSQL": {
                #     "DB": "eCube_Centralized_DB",
                #     "HOST": "localhost",
                #     "PASSWORD": "eclerx#123",
                #     "USER": "tech",
                # },
                # "MYSQL": {
                #     "DB": "eCube_Centralized_DB",
                #     "HOST": "192.168.8.67",
                #     "PASSWORD": "eclerx#123",
                #     "USER": "tech",
                # },
                "MYSQL": {
                    "DB": "eCube_Centralized_DB",
                    "HOST": "192.168.8.37",
                    "PASSWORD": "eclerx#123",
                    "USER": "tech",
                },
                # "MYSQL": {
                #     "DB": "eCube_Centralized_DB",
                #     "HOST": "192.168.131.23",
                #     "PASSWORD": "Eclerx#123",
                #     "USER": "tech",
                # },
                "RABBITMQ": {
                    "HOST": "localhost",
                    "USER": "guest",
                    "PASSWORD": "guest",
                    "PORT": 5672,
                    "PATH": "/",
                },
                "REDIS": {
                    "HOST": "localhost",
                    "PORT": 6379
                },
                "MEMCACHE": {
                    "HOST": "localhost",
                    "PORT": 11211
                },
                "SERVICES": {
                    "SERVICES_IP": "localhost"
                }
            }

        self._config = config_response

        return self.get_config

    @property
    def get_redis_config(self):
        return self.get_config['REDIS']

    @property
    def get_mysql_config(self):
        return self.get_config['MYSQL']

    @property
    def get_mongodb_config(self):
        return self.get_config['MONGODB']

    @property
    def get_memcache_config(self):
        return self.get_config['MEMCACHE']

    @property
    def get_rabbitmq_config(self):
        return self.get_config['RABBITMQ']

    @property
    def get_services_config(self):
        return self.get_config['SERVICES']

    # TODO: "ironeagle" implement this later
    @property
    def set_config(self):
        return None


class CrawlingConsumerConfigFetcher(ConfigFetcher):

    @property
    def get_pymysql_kwargs(self):
        return {
            'host': self.get_mysql_config['HOST'],
            'user': self.get_mysql_config['USER'],
            'passwd': self.get_mysql_config['PASSWORD'],
            'db': self.get_mysql_config['DB']
        }

    @property
    def get_mongodb_args(self):
        return self.get_mysql_config['URL']

    @property
    def get_rabbitmq_min_args(self):
        return self.get_rabbitmq_config['HOST']

    @property
    def get_rabbitmq_args(self):
        return self.get_rabbitmq_config['HOST'], self.get_rabbitmq_config['USER'], self.get_rabbitmq_config['PASSWORD'], self.get_rabbitmq_config['PORT'], self.get_rabbitmq_config['PATH']

    @property
    def get_pymysql_args(self):
        return self.get_mysql_config['HOST'], self.get_mysql_config['USER'], self.get_mysql_config['PASSWORD'], self.get_mysql_config['DB']


crawling_consumer_config = CrawlingConsumerConfigFetcher('crawling_consumer_service')