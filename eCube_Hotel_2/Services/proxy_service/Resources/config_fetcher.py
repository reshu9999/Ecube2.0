class ConfigFetcherBase(object):

    _CONFIG_PROPERTY = 'get_%s_config'
    CONFIGS = list()

    def __init__(self, service_name):
        self.service_name = service_name
        self._config = None
        for config in self.CONFIGS:
            self.__set_config_property(config)

    def __set_config_property(self, config_name):
        config_data = self.get_config.get(config_name.upper())
        setattr(self, self._CONFIG_PROPERTY % config_name.lower(), config_data)

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

    # @property
    # def get_redis_config(self):
    #     return self.get_config['REDIS']

    # @property
    # def get_mysql_config(self):
    #     return self.get_config['MYSQL']

    # @property
    # def get_mongodb_config(self):
    #     return self.get_config['MONGODB']

    # @property
    # def get_memcache_config(self):
    #     return self.get_config['MEMCACHE']

    # @property
    # def get_rabbitmq_config(self):
    #     return self.get_config['RABBITMQ']

    # @property
    # def get_services_config(self):
    #     return self.get_config['SERVICES']

    # @property
    # def get_report_caching_config(self):
    #     return self.get_config['REPORT_CACHING']


class ConfigFetcherAPI(ConfigFetcherBase):

    HOST = 'localhost/config'
    VERSION = 'api/v1'
    PATH = 'service/%s/config'

    def __init__(self, service_name):
        super(self, ConfigFetcherAPI).__init__(service_name)
        self.config_url = 'http://%s/%s/%s/' % (self.HOST, self.VERSION, self.PATH % self.service_name)

    def _make_config(self):
        import requests
        return requests.get(self.config_url).json()['data']['config']


class ConfigFetcherFile(ConfigFetcherBase):

    FILEPATH = None

    def _make_config(self):
        import json
        with open(self.FILEPATH, 'r') as config_file:
            file_data = config_file.read().replace('\n', '')
            return json.loads(file_data)
