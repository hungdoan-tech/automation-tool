import os.path
import logging
import sys

from logging import Logger, FileHandler, StreamHandler, Formatter
from typing import TextIO
from logging.handlers import RotatingFileHandler

from Constants import LOG_FOLDER


def create_logger(class_name: str, level: int = logging.INFO) -> Logger:
    logger: Logger = logging.getLogger(class_name)

    if not os.path.exists(LOG_FOLDER):
        os.mkdir(LOG_FOLDER)

    file_handler: FileHandler = RotatingFileHandler(os.path.join(LOG_FOLDER, 'Automated_Tasks.log'),
                                                    maxBytes=1024 * 1000 * 10,
                                                    backupCount=3)
    file_handler.setLevel(level)

    console_handler: StreamHandler[TextIO] = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    formatter: Formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s %(funcName)s %(lineno)d: %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(level)

    return logger


centralized_logger: Logger = create_logger('Automated_Task')
