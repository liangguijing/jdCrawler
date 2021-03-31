# -*- coding: utf-8 -*-
"""
@Time: 3/29/2021 18:00
@Name: crawler.py
@Author: https://github.com/liangguijing
@Description: 
"""

from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait
from config import config
from log import logger
from mysql import sql_queue
from requests import Session
from util import get_parsed_json, retry


class Crawler:
    def __init__(self):
        self._session = Session()
        self._session.headers = {
            "User-Agent": config.get("config", "user_agent"),
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        self._sort = config.get("sort", "sort")

    @retry(retry_times=3, wait_secs=3)
    def search(self, keyword, page, pagesize=10):
        """

        :param keyword: 商品名
        :param page: 当前页数
        :param pagesize: 返回多少个商品
        :return:
        """
        url = "https://so.m.jd.com/ware/search._m2wq_list"
        params = {
            "callback": "jdSearchResultBkCbA",
            "datatype": 1,
            "keyword": keyword,
            "page": page,
            "pagesize": pagesize,
            "sort_type": self._sort,
        }
        resp = self._session.get(url, params=params, allow_redirects=False)
        if resp.status_code > 200 or not resp.text:
            # 可能会出错跳转到html页面，也有可能返回空白页面
            raise Exception(f"京东返回页面异常, 关键字:{keyword}-页面{page}，准备重试..")
        result = get_parsed_json(resp.text)["data"]["searchm"]
        page_count = int(result["Head"]["Summary"]["Page"]["PageCount"])
        page_index = int(result["Head"]["Summary"]["Page"]["PageIndex"])
        if page_index > page_count:
            # 当前页面大于搜索结果页面总数
            logger.error(f"keyword:{keyword} 当前页面{page_index}超出搜索结果{page_count}")
            return
        else:
            paragraph = result["Paragraph"]
            mysql = sql_queue.get()
            for p in paragraph:
                ware_id = str(p["wareid"])
                shop_name = str(p["shop_name"])
                ware_name = str(p["Content"]["warename"])
                color = str(p["Content"]["color"])
                price = str(p["dredisprice"])
                total_sales = str(p["totalsales15"])
                good = str(p["good"]) + "%"
                url = str(p["toItemLink"])
                mysql.write_to_db(keyword, page_index, ware_id, shop_name, ware_name, color, price, total_sales, good, url)
            sql_queue.put(mysql)
            logger.info(f"keyword:{keyword} 成功写入第{page_index}页数据")


def search(keyword_list):
    try:
        # 创建线程池
        pool = ThreadPoolExecutor(max_workers=MAX_WORKER)
        crawler = Crawler()
        tasks = [pool.submit(crawler.search, kw.strip(), i + 1) for kw in keyword_list for i in range(PAGE_COUNT)]
        wait(tasks, return_when=ALL_COMPLETED)
        logger.info("完成")
    except Exception as e:
        logger.error(e)
    finally:
        # 关闭所有mysql连接
        while not sql_queue.empty():
            sql_queue.get().close()


if __name__ == "__main__":
    KEYWORDS = config.get("config", "keywords").replace("，", ",").strip().strip(",").split(",")
    MAX_WORKER = int(config.get("config", "threads"))
    PAGE_COUNT = int(config.get("config", "page_count"))
    search(KEYWORDS)
