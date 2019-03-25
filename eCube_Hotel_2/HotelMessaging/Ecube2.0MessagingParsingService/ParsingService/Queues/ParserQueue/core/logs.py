import os
import logging
from logging.handlers import TimedRotatingFileHandler


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


class ParsingLogger(TimedRotatedLoggerBase):

    INTERVAL = 2
    INTERVAL_TYPE = 'H'
    BACKUP_COUNT = 12
    LOG_PATH = '../logs'
    ALLOWED_LEVELS = {
        'DEBUG': 'debug',
        'WARNING': 'warning',
        'ERROR': 'error',
    }

    @classmethod
    def _get_log_message(cls, message, r_id=None, sr_id=None, rd_id=None, proxy=None, headers=None):
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
        if proxy:
            msg_meta.append('|PRX:')
            msg_meta.append(proxy.to_log)
        if headers:
            msg_meta.append('|HDR:')
            msg_meta.append(headers)
        return "".join(msg_meta) + message

    @classmethod
    def _make_log(cls, level, message, r_id=None, sr_id=None, rd_id=None, proxy=None, headers=None):
        logger = cls.get_logger()
        log_writer = getattr(logger, cls.ALLOWED_LEVELS[level])
        log_writer(cls._get_log_message(message, r_id, sr_id, rd_id, proxy, headers))

    @classmethod
    def debug_log(cls, message, r_id=None, sr_id=None, rd_id=None, proxy=None, headers=None):
        return cls._make_log('DEBUG', message, r_id, sr_id, rd_id, proxy, headers)

    @classmethod
    def warning_log(cls, message, r_id=None, sr_id=None, rd_id=None, proxy=None, headers=None):
        return cls._make_log('WARNING', message, r_id, sr_id, rd_id, proxy, headers)

    @classmethod
    def error_log(cls, message, r_id=None, sr_id=None, rd_id=None, proxy=None, headers=None):
        return cls._make_log('ERROR', message, r_id, sr_id, rd_id, proxy, headers)


