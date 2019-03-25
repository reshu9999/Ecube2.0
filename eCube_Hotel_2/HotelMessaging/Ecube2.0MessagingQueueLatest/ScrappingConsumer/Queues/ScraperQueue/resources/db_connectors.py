import redis
import pymysql
import pymongo
import threading

from .custom_exceptions import *
from .config_coordinator import config_fetcher


class MongoBaseHandler(object):
    CONN = None
    DB_NAME = None
    DB_CLIENT = pymongo.MongoClient

    @classmethod
    def set_mongo_url(cls, url=None):
        if not url:
            url = config_fetcher.get_mongodb_config['URL']
        cls.CONN = cls.DB_CLIENT(url)
        return cls.CONN

    @classmethod
    def get_db(cls, db_name):
        return getattr(cls.CONN, db_name)

    @classmethod
    def get_collection(cls, collection_name, db_name=None):
        db = cls.get_db(cls.DB_NAME or db_name)
        return getattr(db, collection_name)


class MySQLBaseHandler(object):

    def __init__(self, host, user, password, db_name):
        self._db = pymysql.connect(host=host, user=user, passwd=password, db=db_name)
        self._cursors = list()

    def clean_connections(self):
        for cur in self._cursors:
            cur.close()
        self._db.close()

    def _cursor(self):
        if not self._db:
            raise MySQLConnectionNotFound
        cursor = self._db.cursor()
        self._cursors.append(cursor)
        return cursor

    def execute_query(self, queries):
        if not isinstance(queries, list):
            queries = [queries]

        cursor = self._cursor()
        for query in queries:
            cursor.execute(query)
        cursor.close()

    @classmethod
    def fetch_objects(cls, cursor):
        response = cursor.fetchall()
        return cursor, response

    def update_procedure(self, procedure, *args):
        cursor = self._cursor()
        cursor.callproc(procedure, list(args))
        self._db.commit()
        cursor.close()

    def fetch_from_procedure(self, procedure, *args):
        cursor = self._cursor()
        cursor.callproc(procedure, list(args))
        return self.fetch_objects(cursor)

    def fetch_from_query(self, query, *args):
        cursor = self._cursor()
        cursor.execute(query % list(args))
        return self.fetch_objects(cursor)


class RedisBaseHandler(object):
    NAMESPACE = None
    HOST = None
    PORT = None
    DB = None
    POOL = None

    SET_BATCH_SIZE = None

    @classmethod
    def _connection(cls):
        if not cls.POOL:
            raise RedisPoolNotFound
        if not cls.HOST:
            raise HostNotFound
        if not cls.PORT:
            raise PortNotFound
        if not cls.DB:
            raise DBNotFound
        if not isinstance(cls.DB, int):
            raise DBIndexIncorrect
        return redis.Redis(connection_pool=cls.POOL)

    @classmethod
    def _name_spaced_key(cls, key):
        if not cls.NAMESPACE:
            raise NamespaceNotFound
        return '%s__%s' % (cls.NAMESPACE, key)

    @classmethod
    def set_key(cls, key, value):
        return cls._connection().set(cls._name_spaced_key(key), value)

    @classmethod
    def _make_batches(cls, obj_list, batch_size):
        if not batch_size:
            raise SetBatchSizeNotFound
        if not isinstance(batch_size, int):
            raise SetBatchSizeIncorrect
        if not isinstance(obj_list, list):
            try:
                obj_list = list(obj_list)
            except Exception as e:
                raise BatchObjectsNotList
        return [obj_list[x * batch_size:(x + 1) * batch_size]
                for x in range(0, int(len(obj_list) / batch_size) + 1)]

    @classmethod
    def batch_set_keys(cls, key_values, batch_size=None):
        batch_size = batch_size or cls.SET_BATCH_SIZE
        for batch in cls._make_batches(key_values.items(), batch_size):
            cls._connection().mset({cls._name_spaced_key(key_value[0]): key_value[1] for key_value in batch})

    @classmethod
    def get_key(cls, key):
        return cls._connection().get(cls._name_spaced_key(key))

    @classmethod
    def key_exists(cls, key):
        return cls._connection().exists(cls._name_spaced_key(key))

    @classmethod
    def delete_key(cls, key):
        return cls._connection().delete(cls._name_spaced_key(key))

    @classmethod
    def incr_key(cls, key):
        return cls._connection().incr(cls._name_spaced_key(key))


class ListenerBase(threading.Thread, RedisBaseHandler):

    CHANNELS = None

    def __init__(self):
        if not self.CHANNELS:
            raise MessageChannelsNotFound
        threading.Thread.__init__(self)

        self.redis = self._connection()
        self._pub_sub_channels = self.redis.pubsub()
        self._pub_sub_channels.subscribe(self.CHANNELS)

    def process(self, item):
        raise NotImplementedError

    def run(self):
        for item in self._pub_sub_channels.listen():
            self.process(item)
