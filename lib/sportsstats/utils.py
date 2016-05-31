#!/usr/bin/env python

"""utils

Utilities used in sportsstats
"""

import logging


def add_years(dt, years):
    """Add (or subtract) years, handling leap years.

    Args:
        dt (datetime): The datetime object.
        years (int): Positive or negative number of years to add.

    Returns:
        datetime: The same calendar date (month and day) in the
            destination year, if it exists, otherwise use the following day
            (thus changing February 29 to March 1).
    """
    try:
        dt = dt.replace(year=dt.year + years)
    except ValueError:
        # handle leap years
        #  dt = d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))
        dt = dt.replace(year=dt.year + years, day=dt.day + 1)
    return dt


def _log_level(verbosity):
    switcher = {
        None: logging.CRITICAL,
        0: logging.CRITICAL,
        1: logging.ERROR,
        2: logging.WARNING,
        3: logging.INFO,
        4: logging.DEBUG
    }
    # no matter how many '-v's above 3 are input, the level is still DEBUG
    return switcher.get(verbosity, logging.DEBUG)


def init_logging(verbosity):
    logger = logging.getLogger('sportsstats')
    level = _log_level(verbosity)
    shared_fmt = ' [%(filename)s:%(funcName)s:%(lineno)s]  %(message)s'

    try:
        from colorlog import ColoredFormatter
        formatter = ColoredFormatter(
                '%(log_color)s%(levelname)s%(reset)s' + shared_fmt,
                log_colors={
                    'DEBUG':    'cyan',
                    'INFO':     'green',
                    'WARNING':  'yellow',
                    'ERROR':    'red',
                    'CRITICAL': 'black,bg_red',
                }
        )
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        logger.addHandler(stream)
        logger.setLevel(level)
    except ImportError:
        logging.basicConfig(level=level, format='%(levelname)s' + shared_fmt)
    return logger
