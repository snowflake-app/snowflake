import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")


def setup():
    logging.basicConfig(level=LOG_LEVEL)
