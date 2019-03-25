class ProxyHandler:
    def get_proxy(self):
        return self.__proxy

    def set_proxy(self, value):
        self.__proxy = value

    proxy = property(get_proxy,set_proxy)