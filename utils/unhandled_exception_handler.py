import sys
import traceback

from utils import log


def log_unhandled_exception(exctype, value, tb):
    logger = log.get_logger('unhandled_exception')
    logger.exception(traceback.format_exception(exctype, value, tb))


def configure_unhandled_exception_handler():
    sys.excepthook = log_unhandled_exception