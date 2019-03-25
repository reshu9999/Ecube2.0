class ConfigFetcher(object):

    HOST = 'localhost/config'
    VERSION = 'api/v1'
    PATH = 'service/%s/config'

    def __init__(self, service_name):
        self.service_name = service_name
        self._config = None
        self.config_url = 'http://%s/%s/%s/' % (self.HOST, self.VERSION, self.PATH % (self.service_name))

    @property
    def get_config(self):
        # import requests
        if not self._config == None:
            return self._config

        # try:
        #     config_response = requests.get(self.config_url).json()['data']['config']
        # except Exception as e:
        #     print("Could not load config")
        #     print(e)
        config_response = {
            "MONGODB": {
                "HTML": {
                    "URL": "mongodb://10.100.18.11:27017"
                },
                "CRAWLED": {
                    "URL": "mongodb://10.100.18.12:27017"
                },
                "CACHE": {
                    "URL": "mongodb://10.100.18.12:27017"
                }
            },
            "MYSQL": {
                "DB": "eCube_Centralized_DB",
                "HOST": "10.100.18.85",
                "PASSWORD": "eclerx#123",
                "USER": "tech"
            },
            "REDIS": {
                "HOST": "10.100.18.87",
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
    def get_services_config(self):
        return self.get_config['SERVICES']

    # TODO: "ironeagle" implement this later
    @property
    def set_config(self):
        return None


config_fetcher = ConfigFetcher('crawl_ops')
