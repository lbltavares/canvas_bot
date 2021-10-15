# -*- coding: utf-8 -*-

"""
Utilitarios para geração de loggers
"""

from logging.handlers import RotatingFileHandler
import logging
import os
import config

_LOGS_DIR = config.Log.LOGS_DIR


class LoggerFactory:
    """
    Cria os loggers padronizados
    """

    @staticmethod
    def get_rotating_file_handler(filename, max_bytes=1024 * 1024 * 10, backup_count=5):
        """
        Gera um handler de log com rotação de arquivos
        """
        return RotatingFileHandler(
            filename=f'{_LOGS_DIR}/{filename}.log',
            maxBytes=max_bytes,  # 10MB
            backupCount=backup_count,
            encoding='utf-8',
            delay=True
        )

    @staticmethod
    def get_default_logger(name, filename=None):
        """
        Returns a logger with a rotating file handler.
        """
        if config.Log.UNIQUE_LOG_FILE:
            filename = config.Log.LOG_FILENAME

        logger = logging.getLogger(name)

        # create a file handler
        handler = LoggerFactory.get_rotating_file_handler(filename)
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
