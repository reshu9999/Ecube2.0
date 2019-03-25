import redis
import threading
import pymysql

from flaskext.mysql import MySQL
from .custom_exceptions import *


class MySQLBaseHandler(object):

    MYSQL_CONN = None

    @classmethod
    def _cursor(cls):
        if not cls.MYSQL_CONN:
            raise MySQLConnectionNotFound
        return cls.MYSQL_CONN.connect().cursor()

    @classmethod
    def update_procedure(cls, procedure, *args):
        # cursor = cls._cursor()
        # cursor.callproc(procedure, list(args))
        # # print(dir(cursor))
        # print(procedure)
        # print(args)
        # cls.MYSQL_CONN.connect().commit()
        # cursor.close()
        db = pymysql.connect(host='10.100.18.85',
                         user='tech',
                         passwd='eclerx#123',
                         db='eCube_Centralized_DB')
        cursor = db.cursor()
        # args = [userid]
        cursor.callproc(procedure, list(args))
        
    @classmethod
    def SP_all_operation_for_update_match(cls,sp_name, primary_hotels_id, Sec_hotel_id,user_id):
        db = pymysql.connect(host='10.100.18.85',
                        user='tech',
                        passwd='eclerx#123',
                        db='eCube_Centralized_DB')
        cursor = db.cursor()
        args = [primary_hotels_id, Sec_hotel_id,user_id]
        cursor.callproc(procname=sp_name , args=args)
        cursor.close()
        db.commit()

    @classmethod
    def SP_all_operation_for_update_unmatch(cls,sp_name, primary_hotels_id,user_id):
        db = pymysql.connect(host='10.100.18.85',
                        user='tech',
                        passwd='eclerx#123',
                        db='eCube_Centralized_DB')
        cursor = db.cursor()
        args = [primary_hotels_id, user_id]
        cursor.callproc(procname=sp_name , args=args)
        cursor.close()
        db.commit()
        

    @classmethod
    def fetch_procedure(cls, procedure, *args):
        cursor = cls._cursor()
        cursor.callproc(procedure, list(args))
        response = cursor.fetchall()
        cursor.close()
        return response


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
