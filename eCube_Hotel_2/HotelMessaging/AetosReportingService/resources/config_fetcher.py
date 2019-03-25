class ConfigFetcherBase(object):

    def __init__(self, service_name):
        self.service_name = service_name
        self._config = None

    def _make_config(self):
        raise NotImplementedError

    @property
    def get_config(self):
        if self._config is not None:
            return self._config

        self._config = self._make_config()

        return self.get_config

    # TODO: "ironeagle" implement this later
    # @property
    # def set_config(self):
    #     return None

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


class ConfigFetcherAPI(ConfigFetcherBase):

    HOST = 'localhost/config'
    VERSION = 'api/v1'
    PATH = 'service/%s/config'

    def __init__(self, service_name):
        super().__init__(service_name)
        self.config_url = 'http://%s/%s/%s/' % (self.HOST, self.VERSION, self.PATH % self.service_name)

    def _make_config(self):
        import requests
        return requests.get(self.config_url).json()['data']['config']


class ConfigFetcherFile(ConfigFetcherBase):

    FILEPATH = '/home/tech/HotelMessaging/config_data.json'

    def _make_config(self):
        import json
        with open(self.FILEPATH, 'r') as config_file:
            file_data = config_file.read()
            file_data = file_data.replace('\n', '').replace(' ', '')
            return json.loads(file_data)


class AetosConfigFetcher(ConfigFetcherFile):

    @property
    def get_pymysql_kwargs(self):
        return {
            'host': self.get_mysql_config['HOST'],
            'user': self.get_mysql_config['USER'],
            'password': self.get_mysql_config['PASSWORD'],
            'db_name': self.get_mysql_config['DB']
        }

    @property
    def get_rabbitmq_min_args(self):
        return self.get_rabbitmq_config['HOST']

    @property
    def get_rabbitmq_args(self):
        return self.get_rabbitmq_config['HOST'], self.get_rabbitmq_config['USER'], self.get_rabbitmq_config['PASSWORD'], self.get_rabbitmq_config['PORT'], self.get_rabbitmq_config['PATH']

    @property
    def get_pymysql_args(self):
        return self.get_mysql_config['HOST'], self.get_mysql_config['USER'], self.get_mysql_config['PASSWORD'], self.get_mysql_config['DB']


reporting_config = AetosConfigFetcher('reporting_service')