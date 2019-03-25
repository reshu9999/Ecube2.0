import re


class ScriptHandler(object):

    def __init__(self, consume_data):
        self.consume_data = consume_data
        if self.consume_data["CrawlerScript"]:
            self.consumer_script = __import__(re.sub(".py", "", self.consume_data["CrawlerScript"]))
        print('initiated')

    def execute_crawl(self):
        # self.consume_data['call_func'] = crawl_hotels
        print('Called')
        tries = 3
        self.remove_proxies()
        try:
            response = getattr(self.consumer_script, self.consume_data['call_func'])
        except Exception:
            tries -= 1
            if tries:
                response = getattr(self.consumer_script, self.consume_data['call_func'])
            else:
                response = None
        return response

    def remove_proxies(self):
        import os
        if 'http_proxy' in os.environ:
            os.environ.pop('http_proxy')
        if 'https_proxy' in os.environ:
            os.environ.pop('https_proxy')
        if 'ftp_proxy' in os.environ:
            os.environ.pop('ftp_proxy')
