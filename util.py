# -*- coding: utf-8 -*-
"""
@Time: 3/29/2021 17:57
@Name: util.py
@Author: https://github.com/liangguijing
@Description: 
"""

import json
from log import logger
from time import sleep


def get_parsed_json(text):
    """
    获取callback的json
    jdSearchResultBkCbA({"errId":"0"})
    """
    begin = text.find("{")
    end = text.rfind("}") + 1
    return json.loads(text[begin:end])


def retry(*, retry_times=3, wait_secs=3, errors=(Exception, )):
    """
    重试装饰器
    :param retry_times: 重试次数
    :param wait_secs: 等待重试时间
    :param errors: Exception
    :return:
    """
    def decorate(fn):
        def wrapper(*args, **kwargs):
            for _ in range(retry_times):
                try:
                    return fn(*args, **kwargs)
                except errors as e:
                    logger.error(e)
                    sleep(wait_secs)
            logger.error(f"重试{retry_times}次后失败 {fn},{args},{kwargs}")
            return None
        return wrapper
    return decorate
