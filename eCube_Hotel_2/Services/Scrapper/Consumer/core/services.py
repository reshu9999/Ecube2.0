from core.utils import get_aetos_proxy, get_user_agent, hotel_data_save_checker


class API(object):

    @classmethod
    def GetProxy(cls, domain, country):
        return get_aetos_proxy(domain, country)

    @classmethod
    def SaveProxyDetails(cls, domain, server, port, username, reason, country, region, code):
        pass

    @classmethod
    def GetUserAgent(cls, domain):
        return get_user_agent(domain)

    @classmethod
    def SaveHtml(cls, hotel_data):
        return hotel_data_save_checker(hotel_data)
