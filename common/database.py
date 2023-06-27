# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: database.py
@IDE: PyCharm
@time: 2023-06-12 16:06
@description: 数据库操作
"""
import pymysql, logging, jsonpath
import pymysql.cursors
from warnings import filterwarnings
from common.basefunc import config_dict

# 忽略 Mysql 告警信息
filterwarnings("ignore", category=pymysql.Warning)

# from common import handleyaml
# from config import *
# config_dict = handleyaml.YamlHandle(CONFIG_DIR).read_yaml()

class MysqlConn:
    """
    封装MySQL常用方法。
    """

    def __init__(self):
        try:
            # 建立数据库连接
            mysql_db = config_dict['mysql_db']
            self.conn = pymysql.connect(host=mysql_db['host'],
                                        port=mysql_db['port'],
                                        user=mysql_db['user'],
                                        passwd=mysql_db['password'])
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
    def mysql_execute(self, sql):
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
    def mysql_query(self, sql):
        try:
            # 执行sql语句
            self.cur.execute(sql)
            # 查询结果
            # data = self.cur.fetchall()
            # 查询单条数据
            data = self.cur.fetchone()
            return data
        except Exception as e:
            raise Exception('执行数据库查询失败：' + str(e))

class SetUpDB(MysqlConn):
    """
    处理前置数据库操作
    """

    def get_setup_sql_data(self, setup_sql):
        """
        处理前置sql请求，获取sql参数
        :param setup_sql:
        :return:
        """
        try:
            db_dict = {}
            if setup_sql:
                for sql_data in setup_sql:
                    db_type = sql_data['type']  #数据库类型
                    db_sql = sql_data['sql']
                    if db_type == 'mysql':
                        if db_sql[0:6].upper() == 'SELECT':
                            sql_date = self.mysql_query(db_sql)
                            for param in sql_data['sqldata']:
                                value = jsonpath.jsonpath(sql_date, param['value'])
                                name = param['name']
                                if value:
                                    db_dict[name] = value[0]
                                else:
                                    raise Exception("数据库参数：" + name + "获取失败，请检查用例！")
                        else:
                            self.mysql_execute(db_sql)
                    else:
                        raise Exception("当前暂不支持此种数据库类型：" + str(db_type))
            return db_dict
        except Exception as e:
            raise Exception("sql 数据查询失败，请检查setup_sql语句是否正确：报错信息：" + str(e))
