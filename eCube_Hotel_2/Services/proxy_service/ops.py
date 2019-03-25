from connectors import ProxyDirectory, ProxyBlocker, ProxyMySQL, UserRunDirectory
from exceptions import ProxyCacheEmpty


class UserRunHandler(UserRunDirectory):
    def __init__(self, user_type, run_type, request_id):
        self.user_type = user_type
        self.run_type = run_type
        self.request_id = request_id

    def set_request_details(self):
        self._set_request_details(self.user_type, self.run_type, self.request_id)

    @classmethod
    def remove_request_details(cls, request_id):
        cls._remove_request_details(request_id)

    @classmethod
    def get_type(cls, request_id):
        return cls._get_request_details(request_id)


class ProxyHandler(object):

    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'

    PROXY_FETCHER = ProxyDirectory.get_proxy
    PROXY_BLOCKER = ProxyBlocker.block_proxy
    PROXY_REFRESHER = ProxyDirectory.refresh_proxies
    PROXY_DUMP = ProxyMySQL.get_proxy_details
    USER_RUN_TYPE_FETCHER = UserRunHandler.get_type

    PROXY_PATTERN = {
        'OPS': {
            'PNF': [LOW, MEDIUM, MEDIUM],
            'NORMAL': [LOW, LOW, LOW]
        },
        'CLIENT': {
            'PNF': [MEDIUM, HIGH, HIGH],
            'NORMAL': [LOW, MEDIUM, HIGH]
        }
    }

    def __init__(self, domain, request_id):
        self.domain = domain
        self.request_id = request_id

    def _get_proxy_pattern(self, user_type, run_type):
        return self.PROXY_PATTERN[user_type][run_type]

    def _get_proxy_by_type(self, proxy_type):
        return self.PROXY_FETCHER(self.domain, proxy_type)

    @property
    def get_proxy(self):
        user_type, run_type = self.USER_RUN_TYPE_FETCHER(self.request_id)
        proxy_pattern = self._get_proxy_pattern(user_type, run_type)

        try:
            return [self._get_proxy_by_type(proxy_type) for proxy_type in proxy_pattern]
        except ProxyCacheEmpty:
            proxies_from_dump = self.PROXY_DUMP()
            self.PROXY_REFRESHER(proxies_from_dump)
            return self.get_proxy

    @classmethod
    def block_proxy(cls, proxy, domain, reason):
        cls.PROXY_BLOCKER(proxy, domain, reason)
