import logging
import sys

class PytcLogger:
    def __init__(self):
        self.formatter = logging.Formatter('[%(name)s] %(asctime)s %(levelname)s %(message)s')


    def setup_logger(self, name, level=logging.INFO):
        handler = logging.FileHandler(f'logs/{name}.log', 'w', 'utf-8')
        handler.setLevel(level)
        handler.setFormatter(self.formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger



