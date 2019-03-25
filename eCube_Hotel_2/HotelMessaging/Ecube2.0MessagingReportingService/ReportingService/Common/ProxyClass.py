class ProxyClass():
    # Username
    def get_username(self):
        return self.__username

    def set_username(self, value):
        self.__username = value

    username = property(get_username, set_username)

    # Password
    def get_password(self):
        return self.__password

    def set_password(self, value):
        self.__password = value

    password = property(get_password, set_password)

    # Address
    def get_address(self):
        return self.__address

    def set_address(self, value):
        self.__address = value

    address = property(get_address, set_address)

    # Port
    def get_port(self):
        return self.__port

    def set_port(self, value):
        self.__port = value

    port = property(get_port, set_port)