import time
from multiprocessing import Process
from Resources.logs import TimedRotatedLoggerBase


class CrawlingLogger(TimedRotatedLoggerBase):

    NAME = 'process'
    INTERVAL = 2
    INTERVAL_TYPE = 'H'
    BACKUP_COUNT = 12
    LOG_PATH = 'logs'
    ALLOWED_LEVELS = {
        'DEBUG': 'debug',
        'WARNING': 'warning',
        'ERROR': 'error',
    }

    @classmethod
    def _get_log_message(cls, message):
        return message

    @classmethod
    def _make_log(cls, level, message):
        logger = cls.get_logger()
        log_writer = getattr(logger, cls.ALLOWED_LEVELS[level])
        log_writer(cls._get_log_message(message))

    @classmethod
    def debug_log(cls, message):
        return cls._make_log('DEBUG', message)

    @classmethod
    def warning_log(cls, message):
        return cls._make_log('WARNING', message)

    @classmethod
    def error_log(cls, message):
        return cls._make_log('ERROR', message)


CrawlingLogger.set_logger()


class ProcessRun(object):

    PROCESS = Process
    REST = time.sleep
    TIMER = 5
    LOGGER = CrawlingLogger

    def __init__(self, process_function, no_of_consumers):
        self.LOGGER.debug_log('INIT process function "%s" with "%s" consumers' % (
            process_function, no_of_consumers
        ))
        self.process_function = process_function
        self.no_of_consumers = no_of_consumers

    def run_threads(self, *args):
        self.LOGGER.debug_log('Process Args "%s"' % ", ".join(list(args)))
        self.LOGGER.debug_log('Starting "%s" Consumers' % self.no_of_consumers)
        for p in range(self.no_of_consumers):
            p1 = Process(target=self.process_function, args=tuple(args))
            self.LOGGER.debug_log('Starting Process ID: "%s"' % p1)
            p1.start()
            self.LOGGER.debug_log('Started Process ID: "%s"' % p1.pid)
            self.REST(self.TIMER)
            self.LOGGER.debug_log('Resting for "%s" Seconds' % self.TIMER)
        self.LOGGER.debug_log('Started "%s" Consumers' % self.no_of_consumers)

    def run_simple(self, *args):
        self.LOGGER.debug_log('Process Args "%s"' % ", ".join(list(args)))
        self.LOGGER.debug_log('Starting Simple Run')
        self.process_function(*args)
        self.LOGGER.debug_log('Ending Simple Run')

    def run_loop(self, *args, **kwargs):
        rest_seconds = kwargs['sleep'] if kwargs and 'sleep' in kwargs else 30
        self.LOGGER.debug_log('Process Args "%s"' % ", ".join(list(args)))
        self.LOGGER.debug_log('Starting Loop Run')
        while True:
            self.process_function(*args)
            self.REST(rest_seconds)
