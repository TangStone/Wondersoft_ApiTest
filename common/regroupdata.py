# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: replacedata.py
@IDE: PyCharm
@time: 2023-06-04 20:19
@description: 参数替换
"""
import json, re, sys, logging

from config import *

from common import exceptions


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

    @staticmethod
    def get_value(param, data):
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

    # def replace_value(self):
    #     """
    #     参数替换
    #     :return:
    #     """
    #     # 保存数据类型
    #     data_type = type(self.casedata)
    #     if isinstance(self.casedata, dict) or isinstance(self.casedata, list):
    #         str_data = json.dumps(self.casedata)
    #     else:
    #         str_data = str(self.casedata)
    #
    #     relevance_list = re.findall(r"\$\{relevance\((.*?)\)\}", str_data)  # 关联参数替换
    #     config_list = re.findall(r"\$\{config\((.*?)\)\}", str_data)  # 配置文件参数替换
    #     extract_list = re.findall(r"\$\{extract\((.*?)\)\}", str_data)  # 配置文件参数替换
    #
    #     if len(config_list):
    #         for i in config_list:
    #             pattern = re.compile(r'\$\{config\(' + i + r'\)\}')
    #             value = self.get_value(i, self.config_dict)
    #             str_data = re.sub(pattern, str(value), str_data, count=1)
    #
    #     if len(extract_list):
    #         for i in extract_list:
    #             pattern = re.compile(r'\$\{extract\(' + i + r'\)\}')
    #             # print("conf_patt: ", pattern)
    #             value = self.get_value(i, self.extract_dict)
    #             str_data = re.sub(pattern, str(value), str_data, count=1)
    #
    #     if len(relevance_list):
    #         for i in relevance_list:
    #             pattern = re.compile(r'\$\{relevance\(' + i + r'\)\}')
    #             value = self.get_value(i, self.relevance_dict)
    #             str_data = re.sub(pattern, str(value), str_data, count=1)
    #
    #     # 还原数据类型
    #     if isinstance(self.casedata, dict) or isinstance(self.casedata, list):
    #         casedata = json.loads(str_data)
    #     else:
    #         casedata = data_type(str_data)
    #
    #     return casedata

    def regroup_case_data(self):
        """
        重组用例数据
        :return:
        """
        sign, rawDict = self.regroup_dict(self.casedata)
        return sign, rawDict


    def regroup_dict(self, rawDict):
        """
        递归重组用例数据
        :param rawdict: 用例数据字典
        :return:
        """
        try:
            sign = 'success'   #标识参数
            if isinstance(rawDict, dict):
                for dict_key in rawDict:    #遍历字典
                    if isinstance(rawDict[dict_key], dict):
                        sign, tem_rawDict = self.regroup_dict(rawDict[dict_key])   #递归处理
                        if sign == 'success':
                            rawDict[dict_key] = tem_rawDict
                        else:
                            rawDict = tem_rawDict
                            break
                    elif isinstance(rawDict[dict_key], list):
                        tem_raw_list = []
                        for list_value in rawDict[dict_key]:
                            if isinstance(list_value, dict):
                                sign, tem_rawDict = self.regroup_dict(list_value)
                                if sign == 'success':
                                    tem_raw_list.append(tem_rawDict)
                                else:
                                    rawDict = tem_rawDict
                                    break
                            elif isinstance(list_value, str):
                                tem_str = self.replace_value(list_value)
                                tem_raw_list.append(tem_str)
                            else:
                                tem_raw_list.append(list_value)
                    elif isinstance(rawDict[dict_key], str):
                        tem_str = self.replace_value(rawDict[dict_key])
                        rawDict[dict_key] = tem_str
        except:
            # 异常处理
            ex_type, ex_val, ex_stack = sys.exc_info()
            error_info = exceptions.get_error_info(ex_type, ex_val, ex_stack)
            rawDict = "重组用例数据异常" + str(error_info)
            sign = 'error'
        return sign, rawDict


    def replace_value(self, str_data):
        """
        参数值替换
        :param data_str: 原始字符串
        :return:
        """
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

        return str_data