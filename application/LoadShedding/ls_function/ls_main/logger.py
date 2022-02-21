#!/bin/python3.6
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
# System
import os
import logging
import logging.handlers

__author__ = 'Wilson Kuo'


def setup_logger(logname):
    LOG_FILENAME = logname + ".log"
    LOG_FORMAT   = '%(asctime)s [%(process)d] %(levelname)s %(name)s: %(message)s'

    logger = logging.getLogger(__name__)
    #=====================================================================
    # Logging setup
    #=====================================================================
    # Set the logging level of the root logger
    # logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().setLevel(logging.INFO)

    # This sets timestamp for logging to UTC, otherwise it is local
    # logging.Formatter.converter = time.gmtime

    # Set up the console logger
    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter(LOG_FORMAT)
    stream_handler.setFormatter(stream_formatter)

    logging.getLogger().addHandler(stream_handler)

    # Set up the file logger
    log_dir = '/home/acs/tmp'
    log_filename = os.path.abspath(os.path.join(log_dir, LOG_FILENAME))
    max_bytes = 1 * 1024 * 1024  # 1 MB
    file_handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=max_bytes, backupCount=0)
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(file_handler)
    logger.info("Logging to file '%s'", log_filename)

def main():
    setup_logger()


if __name__ == "__main__":
    main()


