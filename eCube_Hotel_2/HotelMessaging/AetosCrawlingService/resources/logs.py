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
