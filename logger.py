from logging.handlers import RotatingFileHandler
import logging
import os
import config

_LOGS_DIR = config.LogConfig.LOGS_DIR


class LoggerFactory:

    @staticmethod
    def get_default_logger(name, filename=None):
        """
        Returns a logger with a rotating file handler.
        """
        if config.LogConfig.UNIQUE_LOG_FILE:
            filename = config.LogConfig.LOG_FILENAME

        logger = logging.getLogger(name)

        # create a file handler
        handler = RotatingFileHandler(
            filename=f'{_LOGS_DIR}/{filename or name}.log',
            maxBytes=1024 * 1024 * 10,  # 10MB
            backupCount=2,
            encoding='utf-8',
            delay=True
        )
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            datefmt='%d/%m/%y %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # create a stream handler
        shandler = logging.StreamHandler()
        shandler.setLevel(logging.DEBUG)
        shandler.setFormatter(formatter)
        logger.addHandler(shandler)
        return logger


if not os.path.exists(_LOGS_DIR):
    os.mkdir(_LOGS_DIR)
