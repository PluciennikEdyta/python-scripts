#!/usr/bin/python
from __future__ import unicode_literals

import json
import logging.config
import os


def setup_logging(path='logging.json', default_level=logging.INFO):
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def log_debug(logger):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            logger.debug(
                "[{}][{}][START]".format(
                    type(self).__name__,
                    func.__name__,
                )
            )

            result = func(self, *args, **kwargs)

            logger.debug(
                "[{}][{}][STOP]".format(
                    type(self).__name__,
                    func.__name__,
                )
            )
            logger.debug(
                "[{}][{}][RESULT]".format(
                    type(self).__name__,
                    func.__name__,
                )
            )
            logger.debug(result)
            return result
        return wrapper
    return decorator
