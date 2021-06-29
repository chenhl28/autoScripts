# -*- coding:utf-8 -*-
# @Author:huan
# @Time  :2021-06-09

import datetime
from loguru import logger
import os

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)


class LogHandler:
    """
    按日期创建日志文件
    INFO、ERROR类型的日志分别写入不同的日志文件，INFO日志包含了ERROR日志
    """
    @staticmethod
    def log():
        today_now = datetime.datetime.now().strftime("%Y%m%d")
        logger.add(os.path.join(LOG_PATH, f"info_{today_now}.log"),
                   level="INFO",
                   encoding="utf-8",
                   format="{time:YYYY-MM-DD HH:mm:ss}|{level}|{file}|{line}: {message}",
                   rotation="00:00",
                   retention="7 days")
        logger.add(os.path.join(LOG_PATH, f"error_{today_now}.log"),
                   level="ERROR",
                   encoding="utf-8",
                   format="{time:YYYY-MM-DD HH:mm:ss}|{level}|{file}|{line}: {message}",
                   rotation="00:00",
                   retention="7 days")
        return logger


log = LogHandler().log()

if __name__ == '__main__':
    log.info("就是这么简单，调用即可")
    log.warning("就是这么简单，调用即可")
    log.error("就是这么简单，调用即可")
    log.debug("就是这么简单，调用即可")
