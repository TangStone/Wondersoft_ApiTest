# -*- coding: utf-8 -*-

"""
@author:  gaojie
@File：replacedata.py
@IDE: PyCharm
@time: 2023-05-29 15:29
@description:
"""
import json, re

from config import *
from common import handleyaml

class RepaceData:
    "递归重组用例数据字典"

    def __int__(self, casedata, relevance_dict):
        self.case_data = casedata     # 用例信息
        self.re_dict = relevance_dict  # 替换信息



def config_value(index_str):
    """
    获取配置文件参数值
    :param index_str: 索引字符串
    :return:
    """
    value = handleyaml.get_yaml_value(CONFIG_DIR, index_str)
    return value

def extract_value(index_str):
    """
    获取全局变量参数值
    :param index_str:
    :return:
    """
    value = handleyaml.get_yaml_value(EXTRACT_DIR, index_str)
    return value

def relevance_value(param, relevance_dict):
    """
    管理参数替换
    :param param:
    :return:
    """
    value = relevance_dict[param]
    return value


def replace_value(data, relevance_dict):
    """
    参数替换
    :param data: 原始数据
    :param relevance_dict: 关联用例参数值
    :return:
    """
    # 保存数据类型
    data_type = type(data)
    if isinstance(data, dict) or isinstance(data, list):
        str_data = json.dumps(data)
    else:
        str_data = str(data)
    relevance_list = re.findall(r"\$\{relevance\((.*?)\)\}", str_data)  # 关联参数替换
    config_list = re.findall(r"\$\{config\((.*?)\)\}", str_data)  # 配置文件参数替换
    extract_list = re.findall(r"\$\{extract\((.*?)\)\}", str_data)  # 配置文件参数替换
    # print("relevance_list:",relevance_list)
    # print("config_list:", config_list)

    if len(config_list):
        for i in config_list:
            pattern = re.compile(r'\$\{config\(' + i + r'\)\}')
            # print("conf_patt: ", pattern)
            value = config_value(i)
            str_data = re.sub(pattern, str(value), str_data, count=1)

    if len(extract_list):
        for i in extract_list:
            pattern = re.compile(r'\$\{extract\(' + i + r'\)\}')
            # print("conf_patt: ", pattern)
            value = extract_value(i)
            str_data = re.sub(pattern, str(value), str_data, count=1)

    if len(relevance_list):
        for i in relevance_list:
            pattern = re.compile(r'\$\{relevance\(' + i + r'\)\}')
            value = relevance_value(i, relevance_dict)
            str_data = re.sub(pattern, str(value), str_data, count=1)

    # 还原数据类型
    if isinstance(data, dict) or isinstance(data, list):
        data = json.loads(str_data)
    else:
        data = data_type(str_data)

    return data
