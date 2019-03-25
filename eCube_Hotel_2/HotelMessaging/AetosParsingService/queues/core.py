import json
import datetime

from queues.executor import ScriptHandler
from resources.logs import TimedRotatedLoggerBase
from queues.connections import MongoConnection, RabbitConnection, MySQLConnection


class QueueLogger(TimedRotatedLoggerBase):

    NAME = 'parser_queue'
    INTERVAL = 2
    INTERVAL_TYPE = 'H'
    BACKUP_COUNT = 12
    LOG_PATH = 'logs'
    ALLOWED_LEVELS = {
        'INFO': 'info',
        'DEBUG': 'debug',
        'WARNING': 'warning',
        'ERROR': 'error',
    }

    @classmethod
    def _get_log_message(cls, message, r_id=None, sr_id=None, rd_id=None):
        msg_meta = list()
        if r_id:
            msg_meta.append('|R:')
            msg_meta.append(r_id)
        if sr_id:
            msg_meta.append('|SR:')
            msg_meta.append(sr_id)
        if rd_id:
            msg_meta.append('|RD:')
            msg_meta.append(rd_id)
        return "".join([str(m) for m in msg_meta]) + ' | ' + message

    @classmethod
    def _make_log(cls, level, message, r_id=None, sr_id=None, rd_id=None):
        logger = cls.get_logger()
        log_writer = getattr(logger, cls.ALLOWED_LEVELS[level])
        log_writer(cls._get_log_message(message, r_id, sr_id, rd_id))

    @classmethod
    def info_log(cls, message, r_id=None, sr_id=None, rd_id=None):
        return cls._make_log('INFO', message, r_id, sr_id, rd_id)

    @classmethod
    def debug_log(cls, message, r_id=None, sr_id=None, rd_id=None):
        return cls._make_log('DEBUG', message, r_id, sr_id, rd_id)

    @classmethod
    def warning_log(cls, message, r_id=None, sr_id=None, rd_id=None):
        return cls._make_log('WARNING', message, r_id, sr_id, rd_id)

    @classmethod
    def error_log(cls, message, r_id=None, sr_id=None, rd_id=None):
        return cls._make_log('ERROR', message, r_id, sr_id, rd_id)


QueueLogger.set_logger()


class ReparseBase(object):

    HTML_READER = MongoConnection
    QUEUE_CONN = RabbitConnection
    MYSQL_CONN = MySQLConnection

    def __init__(self, reparse_id, reparse_type):
        self._id = reparse_id
        self._type = reparse_type

    @property
    def _get_query(self):
        raise NotImplementedError

    @property
    def _read_from_html_repository(self):
        return self.HTML_READER.get_crawled_html(self._get_query)

    def update_status(self):
        connection = self.MYSQL_CONN()
        connection.update_procedure('sp_PushToReparse', self._id, self._type)
        connection.clean_connections()

    def clean_parsed_data(self):
        self.HTML_READER.delete_parsed_data(self._get_query)

    def push_to_reparse_queue(self):
        queue_connection = RabbitConnection().connection
        channel = queue_connection.channel()
        channel.queue_declare("Reparse")
        reparse_list = list(self._read_from_html_repository)
        self.HTML_READER.mark_hotels_to_be_reparsed(reparse_list)
        print('queueing "%s" hotels for reparse' % len(reparse_list))
        for reparse_data in reparse_list:
            reparse_data.pop('_id')
            channel.basic_publish(exchange='', routing_key='Reparse', body=json.dumps(reparse_data))
        queue_connection.close()


class RequestReparse(ReparseBase):

    def __init__(self, request_id):
        super().__init__(request_id, 'request')

    @property
    def _get_query(self):
        return {'requestId': self._id}


class SubRequestReparse(ReparseBase):

    def __init__(self, sub_request_id):
        super().__init__(sub_request_id, 'sub_request')

    @property
    def _get_query(self):
        return {'subRequestId': self._id}


class BaseCallback(object):

    LOGGER = QueueLogger

    def __init__(self, channel, method, properties, body, redelivered=None):
        """
        :param channel:
        :param method:
        :param properties:
        :param body:
        """
        self.channel = channel
        self.method = method
        self.properties = properties
        self.redelivered = redelivered if redelivered is not None else self.method.redelivered
        self.body = body

        self._data = None
        self.processed_data = None

        self.request_id = None
        self.sub_request_id = None
        self.request_run_id = None

        self._error = None
        self._error_code = None
        self._error_message = None

    def _make_debug_log(self, message):
        self.LOGGER.debug_log(message, self.request_id, self.sub_request_id, self.request_run_id)

    def _make_error_log(self, message):
        self._make_debug_log('[ERROR]' + message)
        self.LOGGER.error_log(message, self.request_id, self.sub_request_id, self.request_run_id)

    def _make_info_log(self, message):
        self._make_error_log('[INFO]' + message)
        self.LOGGER.info_log(message, self.request_id, self.sub_request_id, self.request_run_id)

    @property
    def _get_process_data(self):
        if self._data is not None:
            return self._data
        try:
            self._data = json.loads(self.body.decode('utf-8'))
        except Exception as e:
            self._data = eval(self.body.decode('utf-8'))
        return self._get_process_data

    def prep_process_data(self):
        process_data = self._get_process_data
        self.request_id = process_data['requestId']
        self.sub_request_id = process_data['subRequestId']
        self.request_run_id = process_data['requestRunId']

    def _set_error(self, error_code, error_message):
        # TODO: make checks for only allowed error_codes and corresponding _process_<error_code>_error functions
        self._error = True
        self._error_code = error_code
        self._error_message = error_message
        self._make_error_log("Setting Error Code:'%s' with Error Msg:'%s'" % (self._error_code, self._error_message))

    def _process_error(self):
        self._make_info_log("Processing Error Code:'%s' with Error Msg:'%s'" % (self._error_code, self._error_message))
        getattr(self, '_process_%s_error' % self._error_code)()

    def _execute_script(self):
        raise NotImplementedError

    def _process_success(self):
        raise NotImplementedError

    def consume(self):
        self.prep_process_data()
        self._make_info_log("Method:%s" % self.method)
        self._make_info_log("Properties:%s" % self.properties)
        self._make_debug_log("Receiving Messages:%r" % self.body)
        self._make_info_log("Consumer Start Time:%s" % datetime.datetime.now())

        self._execute_script()

        if self._error:
            self._process_error()
        else:
            self._process_success()

        self.channel.basic_ack(delivery_tag=self.method.delivery_tag)


class Callback(BaseCallback):

    def _process_success(self):
        sub_request_completed = MongoConnection().save_partial_parse(self.processed_data, 'to_be_reparsed')
        if sub_request_completed:
            request_id = self.request_id
            sub_req_id = self.sub_request_id
            mysql_conn = MySQLConnection()._db
            print('args for update request run detail "%s"' % (",".join(['lasun', str(request_id), str(sub_req_id), '69'])))
            cur = mysql_conn.cursor()
            cur.execute('call sp_UpdateRequestRunDetail("lasun", %s, %s, "69")' % (request_id, sub_req_id))
            mysql_conn.commit()
            cur.close()
            mysql_conn.close()

    @property
    def _get_processed_data(self):
        return ScriptHandler(self._get_process_data).execute_parse()

    def _execute_script(self):
        self.processed_data = self._get_processed_data
