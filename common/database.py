# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: database.py
@IDE: PyCharm
@time: 2023-06-12 16:06
@description: 数据库操作
"""
import pymysql, logging
import pymysql.cursors

class MysqlServer:
    """
    封装MySQL常用方法。
    """
    def __init__(self, host, port, user, passwd, charset='utf8'):
        try:
            # 建立数据库连接
            self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, charset=charset)
            # 创建游标
            self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        except Exception as e:
            raise Exception("数据库连接失败：" + str(e))

    def __del__(self):
        try:
            # 关闭游标
            self.cur.close()
            # 关闭连接
            self.conn.close()
        except Exception as e:
            raise Exception("关闭数据库连接失败：" + str(e))

    # 增加、修改、删除命令语句
    def execute(self, sql):
        try:
            # 执行sql语句
            self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
        except Exception as e:
            # 出错时回滚
            self.conn.rollback()
            raise Exception('执行数据库操作失败：' + str(e))

    # 查询所有数据,多个值
    def query(self, sql):
        try:
            # 执行sql语句
            self.cur.execute(sql)
            # 查询结果
            data = self.cur.fetchall()
            return data
        except Exception as e:
            raise Exception('执行数据库查询失败：' + str(e))

