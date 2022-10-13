import logging
import traceback


_log_format = f"%(asctime)s - [%(name)s] - %(message)s"


class Logger:
    def __init__(self, name: str):
        file_handler = logging.FileHandler("logfile.log")
        file_handler.setFormatter(logging.Formatter(_log_format))
        self.logger = logging.getLogger(name)
        self.logger.addHandler(file_handler)

    def log(self, msg: str) -> None:
        self.logger.setLevel(logging.INFO)
        self.logger.info(msg)

    def error(self, msg: str) -> None:
        self.logger.setLevel(logging.ERROR)
        self.logger.error(msg)


def log(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            logger = Logger(func.__name__)
            logger.error(traceback.format_exc())
            return None
    return wrapper