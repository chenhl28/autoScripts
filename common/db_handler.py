# -*- coding:utf-8 -*-
# @Author:huan
# @Time  :2021-06-10
import os

import pymysql
from common.log_handler import log
from common.read_data import read
import cx_Oracle

data = read.load_ini("configs\cfg.ini")
DB_CONF = {
    "host": data["mysql"]["host"],
    "port": int(data["mysql"]["port"]),
    "user": data["mysql"]["user"],
    "password": data["mysql"]["password"],
    "db": data["mysql"]["db"],
    "charset": "utf8"
}

class MysqlHandler:
    def __init__(self, db_conf=DB_CONF):
        #通过字典拆包传递配置信息，建立数据库连接
        self.conn = pymysql.connect(**db_conf, autocommit=True)
        #通过cursor() 创建游标对象，并让查询结果以字典格式输出
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 对象资源被释放时触发，在对象即将被删除时的最后操作
    def __del__(self):
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def execute_sql(self, sql, one=False):
        try:
            # 检查连接是否断开，如果断开就进行重连
            self.conn.ping(reconnect=True)
            if sql.startswith("select"):
                self.cur.execute(sql)
                if one:
                    return self.cur.fetchone()
                else:
                    return self.cur.fetchall()
            else:
                self.cur.execute(sql)
                # 提交事务
                self.conn.commit()
        except Exception as e:
            log.error(f"操作MySQL出现错误，错误原因：{e}")
            # 回滚所有更改
            self.conn.rollback()

class OracleHandler:

    def __init__(self, conn_url):
        self.conn = self.createConn(conn_url)
        self.cur = self.conn.cursor

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def createConn(self, conn_url):
        os.environ["NLS_LANG"] = "SIMPLIFIED CHINESE_CHINA.UTF8"
        try:
            conn = cx_Oracle.connect(conn_url)
            log.info("-----------数据库连接成功-----------")
            return conn
        except Exception as e:
            log.error(f"数据库连接异常，错误原因：{e}")

    def execute_sql(self, sql, one=False):
        try:
            # 检查连接是否断开，如果断开就进行重连
            self.conn.ping(reconnect=True)
            if sql.startswitch("select"):
                self.cur.execute(sql)
                if one:
                    return self.cur.fetchone()
                else:
                    return self.cur.fetchall()
            else:
                self.cur.execute(sql)
                # 提交事务
                self.conn.commit()
        except Exception as e:
            log.error(f"操作Oracle出现错误，错误原因：{e}")
            # 回滚所有更改
            self.conn.rollback()


if __name__ == '__main__':
    db = MysqlHandler(DB_CONF)
    sql = """select * from course"""
    sql2 = """INSERT INTO course VALUES (5, "化学11")"""
    db.execute_sql(sql2)
    data = db.execute_sql(sql)
    print(data)