import os
import logging
from logging.handlers import TimedRotatingFileHandler

from .exceptions import MissingProp


class TimedRotatedLoggerBase(object):
    """
    NAME: name of log file
    INTERVAL: time interval when to rotate log file
    INTERVAL_TYPE: time interval type OPTIONS: 'S', 'M', 'H', 'D'
    BACKUP_COUNT: how many backups to keep
    LOG_PATH: path to keep logs
    """

    NAME = None
    INTERVAL = None
    INTERVAL_TYPE = None
    BACKUP_COUNT = None
    LOG_PATH = None

    @classmethod
    def set_logger(cls):
        handler = TimedRotatingFileHandler(
            filename=os.path.join(cls.LOG_PATH, cls.NAME + '.log'),
            when=cls.INTERVAL_TYPE,
            interval=cls.INTERVAL,
            backupCount=cls.BACKUP_COUNT
        )

        logger = cls.get_logger()
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s| %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    @classmethod
    def get_logger(cls):
        return logging.getLogger(cls.NAME)


class PropLogger(TimedRotatedLoggerBase):

    ALLOWED_LEVELS = {
        'INFO': 'info',
        'DEBUG': 'debug',
        'WARNING': 'warning',
        'ERROR': 'error',
    }
    PROPERTIES = list()

    @classmethod
    def prop_string(cls, *args, **kwargs):
        msg_meta = list()
        for i, prop in enumerate(cls.PROPERTIES):
            if len(args) >= i + 1:
                prop_value = args[i]
            elif prop['arg'] in kwargs:
                prop_value = kwargs[prop['arg']]
            else:
                prop_value = None
                # raise MissingProp('Missing Prop "%s"' % prop['arg'])
            if prop_value:
                msg_meta.append('|%s:%s' % (prop['arg'], prop_value))

        return "".join([str(m) for m in msg_meta]) + '|'

    @classmethod
    def _get_log_message(cls, message, *arg, **kwargs):
        return cls.prop_string(*arg, **kwargs) + message

    @classmethod
    def _make_log(cls, level, message, *arg, **kwargs):
        logger = cls.get_logger()
        log_writer = getattr(logger, cls.ALLOWED_LEVELS[level])
        log_writer(cls._get_log_message(message, *arg, **kwargs))

    @classmethod
    def info_log(cls, message, *arg, **kwargs):
        return cls._make_log('INFO', message, *arg, **kwargs)

    @classmethod
    def debug_log(cls, message, *arg, **kwargs):
        return cls._make_log('DEBUG', message, *arg, **kwargs)

    @classmethod
    def warning_log(cls, message, *arg, **kwargs):
        return cls._make_log('WARNING', message, *arg, **kwargs)

    @classmethod
    def error_log(cls, message, *arg, **kwargs):
        return cls._make_log('ERROR', message, *arg, **kwargs)
