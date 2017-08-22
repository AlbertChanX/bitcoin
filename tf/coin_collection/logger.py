# coding:utf-8
import logging
from logging import handlers


class Logger(object):

    _ss_handler = None
    _f_handler = None
    _level = 'DEBUG'
    _initialized = False

    @classmethod
    def initialize(cls, debug, level, logfile, retention=20):
        if debug:
            fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(module)s.%(funcName)s  # %(message)s")
        else:
            fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s # %(message)s")

        cls._f_handler = logging.handlers.TimedRotatingFileHandler(logfile, 'midnight', 1, retention)
        cls._f_handler.setFormatter(fmt)

        cls._ss_handler = logging.StreamHandler()
        cls._ss_handler.setFormatter(fmt)
        cls._level = level
        cls._initialized = True

    def __init__(self, name):
        self.name = name
        if self._initialized:
            self.log = self._create_logger()
        else:
            self.log = None

    def _create_logger(self):
        log = logging.getLogger(self.name)
        log.addHandler(self._ss_handler)
        log.addHandler(self._f_handler)
        log.setLevel(self._level)
        log.debug("Logging initialized")
        return log

    def debug(self, message):
        if self.log is None:
            if not self._initialized:
                print(message)
            else:
                self.log = self._create_logger()
                self.log.debug(message)
        else:
            self.log.debug(message)

    def info(self, message):
        if self.log is None:
            if not self._initialized:
                print(message)
            else:
                self.log = self._create_logger()
                self.log.info(message)
        else:
            self.log.info(message)

    def warning(self, message):
        if self.log is None:
            if not self._initialized:
                print(message)
            else:
                self.log = self._create_logger()
                self.log.warning(message)
        else:
            self.log.warning(message)

    def error(self, message):
        if self.log is None:
            if not self._initialized:
                print(message)
            else:
                self.log = self._create_logger()
                self.log.error(message)
        else:
            self.log.error(message)

    def critical(self, message):
        if self.log is None:
            if not self._initialized:
                print(message)
            else:
                self.log = self._create_logger()
                self.log.critical(message)
        else:
            self.log.critical(message)

# call 1 time only
initialize = Logger.initialize    # cls method --> logger.py initialize (method)


def get_logger(name):
    return Logger(name)

