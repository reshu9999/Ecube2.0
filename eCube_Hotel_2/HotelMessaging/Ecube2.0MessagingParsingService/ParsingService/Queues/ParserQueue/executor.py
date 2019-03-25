import re


class ScriptHandler(object):

    def __init__(self, consume_data):
        self.consume_data = consume_data
        if self.consume_data["ParserScript"]:
            self.consumer_script = __import__(re.sub(".py", "", self.consume_data["ParserScript"]))

    def execute_parse(self):
        # self.consume_data['call_func'] = crawl_hotels
        tries = 3
        self.remove_proxies()
        try:
            getattr(self.consumer_script, self.consume_data['call_func'])()
        except Exception:
            tries -= 1
            if tries:
                getattr(self.consumer_script, self.consume_data['call_func'])()


    def remove_proxies(self):
        import os
        if 'http_proxy' in os.environ:
            os.environ.pop('http_proxy')
        if 'https_proxy' in os.environ:
            os.environ.pop('https_proxy')
        if 'ftp_proxy' in os.environ:
            os.environ.pop('ftp_proxy')
