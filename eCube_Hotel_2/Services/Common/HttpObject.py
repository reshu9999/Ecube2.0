class HttpObject:
    def get_useragent(self):
        return self.__useragent

    def set_useragent(self, value):
        self.__useragent = value

    useragent = property(get_useragent,set_useragent)
