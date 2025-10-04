import os
import logging
from datetime import datetime


class Logger:

    def __init__(self):
        t = datetime.now()
        current_time = t.strftime("%Y_%m_%d_%H_%M_%S.%f")

        # Define formatters
        log_format = "%(asctime)-15s [%(levelname)s] %(module)s.%(funcName)s: %(message)s"
        self.default_logging_formatter = logging.Formatter(log_format)

        # Create logger
        self.log_filepath = f"output/{current_time}"
        if not os.path.exists(self.log_filepath):
            os.makedirs(self.log_filepath)

        self.logger = self.create_logger(f"{self.log_filepath}/main.log", self.default_logging_formatter, 'default')


    def create_logger(self, log_filepath: str, formatter, logger_name: str = None):
        logger = logging.getLogger(logger_name)

        # Check if the logger has any handlers. If it does, assume it's already configured.
        if not logger.hasHandlers():
            file_handler = logging.FileHandler(log_filepath)
            stream_handler = logging.StreamHandler()

            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)

            file_handler.setLevel(logging.INFO)
            stream_handler.setLevel(logging.INFO)

            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)

        logger.setLevel(logging.INFO)

        return logger
