# -*- coding: utf-8 -*-
"""
@Time: 3/29/2021 17:53
@Name: log.py
@Author: https://github.com/liangguijing
@Description: 
"""

import logging
import logging.handlers

log_filename = "./temp/log.log"
logger = logging.getLogger()


def set_logger():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(module)s] %(levelname)s: %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.handlers.RotatingFileHandler(
        log_filename, maxBytes=1048576, backupCount=10, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


set_logger()
