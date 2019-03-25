from Resources.config_fetcher import crawling_config


class ServiceCaller(object):

    SERVICE_NAME = None
    SERVER_NAME = None
    PROTOCOL = None

    @classmethod
    def _get_host(cls):
        return crawling_config.get_services_config[cls.SERVICE_NAME][cls.SERVER_NAME]['HOST']

    @classmethod
    def _get_port(cls):
        return crawling_config.get_services_config[cls.SERVICE_NAME][cls.SERVER_NAME]['PORT']

    @classmethod
    def service_url(cls, path, protocol=None):
        protocol = protocol or cls.PROTOCOL or 'http'
        if cls._get_port() in ['', '80', None]:
            return "%s://%s" % (protocol, cls._get_host()) + path
        else:
            return "%s://%s:%s" % (protocol, cls._get_host(), cls._get_port()) + path
