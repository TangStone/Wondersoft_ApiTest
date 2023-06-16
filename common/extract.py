# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: extract.yaml.py
@IDE: PyCharm
@time: 2023-06-08 15:59
@description: 处理参数传递
"""
import re, jsonpath, logging

from config import *
from common import handleyaml

def handle_extarct(extarct, recv_data, caseid):
    """
    处理中间参数
    :param extarct: 提取参数字典
    :param recv_data: 接口返回值
    :param caseid: 用例id
    :return:
    """
    for key, value in extarct.items():
        if "(.*?)" in value or "(.+?)" in value:  # 正则表达式
            zz_value = re.search(value, recv_data)
            if zz_value:
                extract_value = {key: zz_value.group(1)}
            else:
                raise Exception("期望值获取失败！")
        else:  # jsonpath
            js_value = jsonpath.jsonpath(recv_data, value)
            if js_value:
                extract_value = {key: js_value[0]}
            else:
                raise Exception("期望值获取失败！")
        logging.info("extract_value:%s", extract_value)
        extract_value = {caseid: extract_value}
        handleyaml.YamlHandle(EXTRACT_DIR, extract_value).updata_yaml()
