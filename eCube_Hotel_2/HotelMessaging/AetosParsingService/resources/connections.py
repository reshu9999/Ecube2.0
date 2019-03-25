import pika
import redis
import pymysql
import pymongo


class RabbitBaseConnection(object):

    def __init__(self, host):
        self.host = host

    @property
    def connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(host=self.host))

    def channel(self, *args, **kwargs):
        return self.connection.channel(*args, **kwargs)

    # def __init__(self, host, user, password, port, path):
    #     self.host = host
    #     self.user = user
    #     self.password = password
    #     self.port = port
    #     self.path = path

    @classmethod
    def report_queue(cls):
        credentials = pika.PlainCredentials('guest', 'guest')

        parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue='Report', durable=True)
        return channel


class MySQLBaseHandler(object):

    def __init__(self, host, user, password, db_name):
        self._db = pymysql.connect(host=host, user=user, passwd=password, db=db_name)
        self._cursors = list()

    def _clean_db(self):
        try:
            self._db.close()
        except Exception as e:
            print('Clean DB "%s"' % e)

    def _clean_cursors(self):
        for cur in self._cursors:
            try:
                cur.close()
            except Exception as e:
                print('Clean Cursor "%s"' % e)

    def clean_connections(self):
        self._clean_cursors()
        self._clean_db()

    @property
    def _cursor(self):
        if not self._db:
            raise Exception('MySQLConnectionNotFound')
        cursor = self._db.cursor()
        self._cursors.append(cursor)
        return cursor

    def execute_query(self, queries):
        if not isinstance(queries, list):
            queries = [queries]

        cursor = self._cursor
        for query in queries:
            cursor.execute(query)
        cursor.close()

    @classmethod
    def fetch_objects(cls, cursor, close=True):
        response = cursor.fetchall()
        if close:
            cursor.close()
        return response

    def update_procedure(self, procedure, *args):
        cursor = self._cursor
        cursor.callproc(procedure, list(args))
        self._db.commit()
        cursor.close()

    def update_query(self, query, *args):
        cursor = self._cursor
        cursor.execute(query % list(args))
        self._db.commit()
        cursor.close()

    def fetch_from_procedure(self, procedure, *args):
        cursor = self._cursor
        cursor.callproc(procedure, list(args))
        return self.fetch_objects(cursor)

    def fetch_from_query(self, query, *args):
        cursor = self._cursor
        cursor.execute(query % list(args))
        return self.fetch_objects(cursor)


class RedisBaseHandler(object):
    NAMESPACE = None
    HOST = None
    PORT = None
    DB = None
    POOL = redis.ConnectionPool

    SET_BATCH_SIZE = None

    @classmethod
    def _connection(cls):
        if not cls.POOL:
            raise Exception('RedisPoolNotFound')
        if not cls.HOST:
            raise Exception('HostNotFound')
        if not cls.PORT:
            raise Exception('PortNotFound')
        if not cls.DB:
            raise Exception('DBNotFound')
        if not isinstance(cls.DB, int):
            raise Exception('DBIndexIncorrect')
        return redis.Redis(connection_pool=cls.POOL(host=cls.HOST, port=cls.PORT, db=cls.DB))

    @classmethod
    def set_key(cls, key, value):
        if not cls.NAMESPACE:
            raise Exception('NamespaceNotFound')
        return cls._connection().set('%s__%s' % (cls.NAMESPACE, key), value)

    @classmethod
    def _make_batches(cls, obj_list, batch_size=None):
        batch_size = cls.SET_BATCH_SIZE or batch_size
        if not batch_size:
            raise Exception('SetBatchSizeNotFound')
        if not isinstance(batch_size, int):
            raise Exception('SetBatchSizeIncorrect')
        if not isinstance(obj_list, list):
            try:
                obj_list = list(obj_list)
            except Exception as e:
                raise Exception('BatchObjectsNotList')
        return [obj_list[x * batch_size:(x + 1) * batch_size]
                for x in range(0, int(len(obj_list) / batch_size) + 1)]

    @classmethod
    def batch_set_keys(cls, key_values, batch_size):
        if not cls.NAMESPACE:
            raise Exception('NamespaceNotFound')
        for batch in cls._make_batches(key_values.items(), batch_size):
            cls._connection().mset({'%s__%s' % (cls.NAMESPACE, key_value[0]): key_value[1] for key_value in batch})

    @classmethod
    def get_key(cls, key):
        if not cls.NAMESPACE:
            raise Exception('NamespaceNotFound')
        return cls._connection().get('%s__%s' % (cls.NAMESPACE, key))

    @classmethod
    def scan_keys(cls, pattern):
        if not cls.NAMESPACE:
            raise Exception('NamespaceNotFound')
        return cls._connection().scan_iter('%s__%s' % (cls.NAMESPACE, pattern))

    @classmethod
    def key_exists(cls, key):
        if not cls.NAMESPACE:
            raise Exception('NamespaceNotFound')
        return cls._connection().exists('%s__%s' % (cls.NAMESPACE, key))

    @classmethod
    def delete_key(cls, key):
        if not cls.NAMESPACE:
            raise Exception('NamespaceNotFound')
        return cls._connection().delete('%s__%s' % (cls.NAMESPACE, key))


class MongoBaseHandler(object):
    CONN = None
    DB_NAME = None
    DB_CLIENT = pymongo.MongoClient

    @classmethod
    def set_mongo_url(cls, url):
        cls.CONN = cls.DB_CLIENT(url)
        return cls.CONN

    @classmethod
    def get_db(cls, db_name):
        return getattr(cls.CONN, db_name)

    @classmethod
    def get_collection(cls, collection_name, db_name=None):
        db = cls.get_db(cls.DB_NAME or db_name)
        return getattr(db, collection_name)
