import importlib
from queues.cache import ReportingCacheHandler


class ScriptHandler(object):
    SCRIPTS_IMPORT_PATH = 'scripts'

    def __init__(self, consume_data):
        self.consume_data = consume_data
        if self.consume_data["ParserScript"]:
            self.consumer_script = importlib.import_module("%s.%s" % (self.SCRIPTS_IMPORT_PATH, self.consume_data["ParserScript"]))
            importlib.reload(self.consumer_script)

    def _execute_script_function(self, tries):
        self.consume_data['call_func'] = 'crawl_hotels'
        print("self.consumer_script")
        print(self.consumer_script)
        # print("self.consume_data['call_func']")
        # print(self.consume_data['call_func'])
        return getattr(self.consumer_script, self.consume_data['call_func'])(self.consume_data)

    def execute_parse(self):
        tries = 3
        self.remove_proxies()
        parsed_response = self._execute_script_function(tries)
        if parsed_response is not None:
            self._save_in_redis(parsed_response)
            # if parse_type == 'production':
            #     pass
            # elif parse_type == 'testing':
            #     return parsed_response
        return parsed_response

    def _save_in_redis(self, data):
        """
        :param data:
        :return:
        """
        # print('saving in redis "%s" hotels' % (len(data['hotels'])))
        # print(type(data))
        # from pdb import set_trace;set_trace();#Bhavin
        meta_data = data.copy()
        # meta_data.pop('hotels')
        meta_data.pop('hotel')
        # for i, hd in enumerate(data['hotels']):
        #     ReportingCacheHandler(i, hd, meta_data).make_entry()
        ReportingCacheHandler(data['hotel']['index'], data['hotel'], meta_data).make_entry()

    @staticmethod
    def remove_proxies():
        import os
        if 'http_proxy' in os.environ:
            os.environ.pop('http_proxy')
        if 'https_proxy' in os.environ:
            os.environ.pop('https_proxy')
        if 'ftp_proxy' in os.environ:
            os.environ.pop('ftp_proxy')
