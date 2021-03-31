# -*- coding: utf-8 -*-
"""
@Time: 3/31/2021 09:35
@Name: mysql.py
@Author: https://github.com/liangguijing
@Description: 
"""

import MySQLdb
from config import config
from log import logger
from queue import Queue


sql_config = {"host": "127.0.0.1",
              "port": 3306,
              "user": 'jingdong',
              "password": 'jingdong',
              "database": 'jingdong',
              "charset": 'utf8',
              "autocommit": True,
              }


class Mysql:
    def __init__(self):
        self._conn = MySQLdb.connect(**sql_config)
        self._cursor = self._conn.cursor()

    def write_to_db(self, keyword, page_index, ware_id, shop_name, ware_name, color, price, total_sales, good, url):
        self._cursor.execute("insert into items (keyword, pageIndex, wareid, shop_name, warename, color, "
                             "price, totalsales, good, url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                             (keyword, page_index, ware_id, shop_name, ware_name, color, price, total_sales, good, url))

    def close(self):
        self._cursor.close()
        self._conn.close()


sql_queue = Queue()
# 创建与线程数相同的mysql连接
size = int(config.get("config", "threads"))

for _ in range(size):
    mysql = Mysql()
    sql_queue.put(mysql)


"""
单链接

conn = MySQLdb.connect(host="127.0.0.1", port=3306,
                       user='jingdong', password='jingdong',
                       database='jingdong', charset='utf8',
                       autocommit=True)
cursor = conn.cursor()
lock = RLock()


def write_to_db(keyword, page_index, ware_id, shop_name, ware_name, color, price, total_sales, good, url):
    try:
        # 加锁
        with lock:
            with conn.cursor() as curs:
                curs.execute("insert into items (keyword, pageIndex, wareid, shop_name, warename, color, "
                             "price, totalsales, good, url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                             (keyword, page_index, ware_id, shop_name, ware_name, color, price, total_sales, good, url))
    except MySQLdb.MySQLError as e:
        logger.error(e)

"""

