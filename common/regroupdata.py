# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: replacedata.py
@IDE: PyCharm
@time: 2023-06-04 20:19
@description: 参数替换
"""
import json, re

from config import *

from common import handleyaml


class RegroupData:
    "参数替换"

    def __init__(self, casedata, relevance_dict, extract_dict, config_dict):
        """
        :param casedata: 用例信息
        :param relevance_dict: 关联参数
        :param extract_dict: 全局参数
        :param config_dict: 配置参数
        """
        self.casedata = casedata
        self.relevance_dict = relevance_dict
        self.extract_dict = extract_dict
        self.config_dict = config_dict

    @classmethod
    def get_value(cls, param, data):
        """
        获取参数值
        :param param: key
        :param data: 取值字典
        :return:
        """
        if isinstance(data, dict):
            if ',' in param:
                expect_value_list = param.split(',')
                for i in expect_value_list:
                    data = data[i]
                return data
            else:
                return data[param]

    def replace_value(self):
        """
        参数替换
        :return:
        """
        # 保存数据类型
        data_type = type(self.casedata)
        if isinstance(self.casedata, dict) or isinstance(self.casedata, list):
            str_data = json.dumps(self.casedata)
        else:
            str_data = str(self.casedata)

        relevance_list = re.findall(r"\$\{relevance\((.*?)\)\}", str_data)  # 关联参数替换
        config_list = re.findall(r"\$\{config\((.*?)\)\}", str_data)  # 配置文件参数替换
        extract_list = re.findall(r"\$\{extract\((.*?)\)\}", str_data)  # 配置文件参数替换

        if len(config_list):
            for i in config_list:
                pattern = re.compile(r'\$\{config\(' + i + r'\)\}')
                value = self.get_value(i, self.config_dict)
                str_data = re.sub(pattern, str(value), str_data, count=1)

        if len(extract_list):
            for i in extract_list:
                pattern = re.compile(r'\$\{extract\(' + i + r'\)\}')
                # print("conf_patt: ", pattern)
                value = self.get_value(i, self.extract_dict)
                str_data = re.sub(pattern, str(value), str_data, count=1)

        if len(relevance_list):
            for i in relevance_list:
                pattern = re.compile(r'\$\{relevance\(' + i + r'\)\}')
                value = self.get_value(i, self.relevance_dict)
                str_data = re.sub(pattern, str(value), str_data, count=1)

        # 还原数据类型
        if isinstance(self.casedata, dict) or isinstance(self.casedata, list):
            casedata = json.loads(str_data)
        else:
            casedata = data_type(str_data)

        return casedata