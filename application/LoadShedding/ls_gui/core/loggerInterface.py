#!/usr/bin/python3
# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.

@Author: Darren Liang
@Date  : 2021-01-05
"""

import os
import logging
import logging.handlers
from  __init__  import (LOG_FILENAME, LOG_FORMAT, LOG_FOLDER)


def logger_setup():
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
    log_dir = LOG_FOLDER
    if not os.path.isdir(log_dir):
        # On Windows, tempPath is user-specific
        log_dir = QtCore.QDir.tempPath()
    log_filename = os.path.abspath(os.path.join(log_dir, LOG_FILENAME))
    max_bytes = 1 * 1024 * 1024  # 1 MB
    file_handler = logging.handlers.RotatingFileHandler(
        log_filename, maxBytes=max_bytes, backupCount=1)
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(file_handler)