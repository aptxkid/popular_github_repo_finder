from __future__ import unicode_literals

import logging


LOG_FILE_NAME = None


def get_logger(logger_name=None):
    """
    :param logger_name: Name for the logger
    :type logger_name: unicode
    :return: A logger instance
    :rtype: :class:`Logger`
    """
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(logger_name)
    if LOG_FILE_NAME:
        fh = logging.FileHandler(LOG_FILE_NAME)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)
    return logger

