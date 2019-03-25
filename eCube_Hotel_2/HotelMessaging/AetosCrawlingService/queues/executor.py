import copy
import datetime
import importlib


class ScriptHandler(object):

    def __init__(self, consume_data):
        self.consume_data = copy.deepcopy(consume_data)

        self.consume_data['RequestInputs'].update({'country': self.consume_data['country']})
        # self.consume_data['RequestInputs']['pos'] = 'United Kingdom'
        self.consume_data.update({
            # "ParserScript": "ParserTravelRepublicPython",
            # "ScraperScript": "ScrapperTravelRepublicPython",
            "domainName": "https://www.aetos-skia.com/",
        })
        # print("self.consume_data")
        # print(self.consume_data)

        check_in = datetime.datetime.strptime(self.consume_data['RequestInputs']['checkIn'], '%Y-%m-%d')
        check_out = check_in + datetime.timedelta(days=self.consume_data['RequestInputs']['nights'])
        self.consume_data['RequestInputs']['checkIn'] = check_in
        self.consume_data['RequestInputs']['checkOut'] = check_out

        if self.consume_data["ScraperScript"]:
            self.consumer_script = importlib.import_module("scripts.%s" % self.consume_data["ScraperScript"])
            importlib.reload(self.consumer_script)
        else:
            # from pdb import set_trace; set_trace()
            raise ValueError('Need Scraper Script to Proceed')

    def _execute_script_function(self, tries, redelivered):
        self.consume_data['call_func'] = 'crawl_hotels'
        print("self.consumer_script")
        print(self.consumer_script)
        # print("self.consume_data['call_func']")
        # print(self.consume_data['call_func'])
        return getattr(self.consumer_script, self.consume_data['call_func'])(self.consume_data, redelivered)

    def execute_crawl(self, redelivered):
        tries = 3
        self.remove_proxies()
        return self._execute_script_function(tries, redelivered)

    def remove_proxies(self):
        import os
        if 'http_proxy' in os.environ:
            os.environ.pop('http_proxy')
        if 'https_proxy' in os.environ:
            os.environ.pop('https_proxy')
        if 'ftp_proxy' in os.environ:
            os.environ.pop('ftp_proxy')
