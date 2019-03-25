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
            "EMAIL": {
                "HOST": "",
                "PORT": "",
                "USER": "", 
                "PASSWORD": "",
            }
        }
        self._config = config_response

        return self.get_config

    @property
    def get_email_config(self):
        return self.get_config['EMAIL']

    # TODO: "ironeagle" implement this later
    @property
    def set_config(self):
        return None


config_fetcher = ConfigFetcher('crawl_ops')
