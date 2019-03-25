import random

from settings import CONFIG
from core import ServiceLogger

from Resources.connections import MySQLBaseHandler

REDIS_CONFIG = CONFIG.get_redis_config


class ProxyMySQL(MySQLBaseHandler):

    FETCH_SP = 'aetos_proxy_fetcher'
    SP_MAPPING = {
        "id": {"db_key": "ProxyMasterId", "d_type": int, "index": 0},
        "ip": {"db_key": "ProxyName", "d_type": str, "index": 2},
        "port": {"db_key": "ProxyPort", "d_type": int, "index": 8},
        "username": {"db_key": "ProxyUserName", "d_type": str, "index": 6},
        "password": {"db_key": "ProxyPassword", "d_type": str, "index": 7},
        "tag": {"db_key": "VendorName", "d_type": str, "index": 9},
        "domain": {"db_key": "DomainName", "d_type": str, "index": 1},
        "type": {"db_key": "TypeName", "d_type": str, "index": 3},
    }

    def __init__(self):
        super().__init__(*CONFIG.get_pymysql_args)

    def _fetch_proxies(self, domain, country, pos, tag, all_proxies):
        print("domain, country, pos, tag")
        print(domain, country, pos, tag)
        # objs = self.fetch_from_procedure(self.FETCH_SP, domain, country, pos, tag)[0]
        # print("objs")
        # print(objs)
        # return objs
        proxies = self.fetch_from_procedure(self.FETCH_SP, domain, country, pos, tag)
        if all_proxies:
            return proxies
        else:
            # return proxies
            return proxies[random.randint(0, len(proxies) - 1)]

    @classmethod
    def get_value(cls, raw_proxy, mapping):
        # print("raw_proxy")
        # print(raw_proxy)
        return raw_proxy[cls.SP_MAPPING[mapping]['index']]

    @classmethod
    def _make_proxy_dict(cls, raw_proxy):
        return {key: cls.get_value(raw_proxy, key) for key in cls.SP_MAPPING}

    @classmethod
    def get_proxy_details(cls, domain, country, pos, tag, all_proxies=None):
        ServiceLogger.info_log('Getting Proxy Details', domain, country, pos, tag)
        proxies = cls()._fetch_proxies(domain, country, pos, tag, all_proxies)
        if all_proxies:
            return [cls._make_proxy_dict(p) for p in proxies]
        else:
            return cls._make_proxy_dict(proxies)
