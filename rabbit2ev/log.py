import sys
import logging


def setup_log_handlers(
        level='INFO', name='rabbit2ev', datefmt='%d-%m-%Y %H:%M:%S',
        log_args='(sys.stderr,)', log_class='StreamHandler',
        formfmt='[%(asctime)s] [%(levelname)s:%(name)s]: %(message)s'):

    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        formatter = logging.Formatter(fmt=formfmt, datefmt=datefmt)
        handle = "logging." + log_class + log_args
        handler = eval(handle)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def getVersion():
    return sys.version
