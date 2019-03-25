class FieldHTMLMapDoesNotExist(Exception):
    pass


class MissingRequiredModel(Exception):
    pass


class MySQLConnectionNotFound(Exception):
    message = 'MySQL Connection not found.\nPlease add "MYSQL_CONN = <mysql_conn>" in your MySQL Class'


class DBIndexIncorrect(Exception):
    message = 'DB Index can only be int type'


class SetBatchSizeIncorrect(Exception):
    message = 'Batch Size can only be int type'


class BatchObjectsNotList(Exception):
    message = 'Batch Objects can only be list type'


class RedisPoolNotFound(Exception):
    message = 'Redis Pool not found.\nPlease add "POOL = redis.ConnectionPool(host=HOST, port=PORT, db=DB)" in your Redis Class'


class NamespaceNotFound(Exception):
    message = 'Namespace not found.\nPlease add "NAMESPACE = <namespace>" in your Redis Class'


class HostNotFound(Exception):
    message = 'Host not found.\nPlease add "HOST = <host>" in your Redis Class'


class PortNotFound(Exception):
    message = 'Port not found.\nPlease add "PORT = <post>" in your Redis Class'


class DBNotFound(Exception):
    message = 'DB not found.\nPlease add "DB = <db>" in your Redis Class'


class SetBatchSizeNotFound(Exception):
    message = 'Set Batch Size not found.\nPlease add "DB = <db>" in your Redis Class'


class MessageChannelsNotFound(Exception):
    message = 'Message Channel not found.\nPlease add "CHANNELS = <db>" in your Listener Class'
