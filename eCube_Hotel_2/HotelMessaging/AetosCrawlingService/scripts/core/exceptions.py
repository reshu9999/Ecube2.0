class HotelNotFound(Exception):
    pass


class ScriptTimeout(Exception):
    pass


class ScriptPNF(Exception):
    pass


class IncorrectRequestType(Exception):
    pass


class MissingRequestType(Exception):
    pass


class MissingVisitHomePage(Exception):
    pass


class GetProxyParamsMissing(Exception):
    pass


class ProxyProtocolNotAllowed(Exception):
    pass


class ProxySetParamsMissing(Exception):
    pass


class ProxyNotFound(Exception):
    pass


class ProxyNotWorking(Exception):
    pass


class ProxyServiceNotWorking(Exception):
    pass


class ProxyGivingServerError(Exception):
    pass


class ProxyGivingPNF(Exception):
    pass


class ProxyGivingAuthError(Exception):
    pass


class ProxyNotAuthError(Exception):
    pass


class InvalidURL(Exception):
    pass


class LatLongNotFountError(Exception):
    pass
