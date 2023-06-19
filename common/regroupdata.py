# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: replacedata.py
@IDE: PyCharm
@time: 2023-06-04 20:19
@description: 参数替换
"""
import json, re, sys, logging, time

import jsonpath

from config import *

from common import exceptions
from common import encryption

class RegroupData:
    """
    参数替换
    """

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
        logging.info("casedata:%s", self.casedata)
        logging.info("relevance_dict:%s", self.relevance_dict)
        logging.info("extract_dict:%s", self.extract_dict)
        logging.info("config_dict:%s", self.config_dict)

    # @staticmethod
    # def get_value(param, data):
    #     """
    #     获取参数值
    #     :param param: key
    #     :param data: 取值字典
    #     :return:
    #     """
    #     if isinstance(data, dict):
    #         if ',' in param:
    #             expect_value_list = param.split(',')
    #             for i in expect_value_list:
    #                 data = data[i.strip()]
    #             return data
    #         else:
    #             return data[param]

    def get_value(self, param, data):
        """
        获取参数值
        :param param: key
        :param data: 取值字典
        :return:
        """
        param_list = param.split(";")  # 拆分取值需求 docrule_01.c_id;type=list
        #获取参数值
        if isinstance(data, dict):
            # 获取参数值
            expect_value_list = param_list[0].split('.')
            for i in expect_value_list:
                data = data[i.strip()]

            if len(param_list) >= 2:
                for pa in param_list[1:]:
                    pa_list = pa.split("=")
                    if pa_list[0] == 'type':
                        return data
            else:  #中间件参数使用jsonpath提取的是列表，取第一个值
                if type(data) == list:
                    return data[0]
                else:
                    return data

    @staticmethod
    def get_enc_value(param):
        """
        参数加密
        :param param: key
        :return:
        """
        data = encryption.encryption(param)
        return data

    @staticmethod
    def get_time(str):
        """
        获取时间
        :param str: format='%Y-%m-%d %H:%M:%S'
        :return:
        """
        param_list = str.split(',')   #获取多个配置项
        time_str = ''
        for param in param_list:
            pa_list = param.split('=')  #拆分配置项
            if pa_list[0] == 'format':   #时间格式
                time_str = time.strftime(pa_list[1])
        return time_str


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
                        rawDict[dict_key] = tem_raw_list
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
        Eval_list = re.findall(r"\$\{Eval\((.*)\)\}", str_data)  # 格式转换,非贪婪模式
        relevance_list = re.findall(r"\$\{relevance\((.*?)\)\}", str_data)  # 关联参数替换
        config_list = re.findall(r"\$\{config\((.*?)\)\}", str_data)  # 配置文件参数替换
        extract_list = re.findall(r"\$\{extract\((.*?)\)\}", str_data)  # 配置文件参数替换
        enc_list = re.findall(r"\$\{enc\((.*?)\)\}", str_data)  # 加密替换
        time_list = re.findall(r"\$\{GetTime\((.*?)\)\}", str_data)  # 时间

        if len(Eval_list):
            for i in Eval_list:
                value = self.replace_value(i)
                try:
                    str_data = eval(value)
                except:
                    str_data = value
                return str_data

        if len(time_list):
            for i in time_list:
                pattern = re.compile(r'\$\{GetTime\(' + i + r'\)\}')
                value = self.get_time(i)
                str_data = re.sub(pattern, str(value), str_data, count=1)

        if len(config_list):
            for i in config_list:
                pattern = re.compile(r'\$\{config\(' + i + r'\)\}')
                value = self.get_value(i, self.config_dict)
                str_data = re.sub(pattern, str(value), str_data, count=1)

        if len(extract_list):
            for i in extract_list:
                pattern = re.compile(r'\$\{extract\(' + i + r'\)\}')
                value = self.get_value(i, self.extract_dict)
                str_data = re.sub(pattern, str(value), str_data, count=1)

        if len(relevance_list):
            for i in relevance_list:
                pattern = re.compile(r'\$\{relevance\(' + i + r'\)\}')
                value = self.get_value(i, self.relevance_dict)
                str_data = re.sub(pattern, str(value), str_data, count=1)

        if len(enc_list):
            for i in enc_list:
                pattern = re.compile(r'\$\{enc\(' + i + r'\)\}')
                value = self.get_enc_value(i)
                str_data = re.sub(pattern, str(value), str_data, count=1)

        return str_data

    @staticmethod
    def restore_datatype(data, str_data):
        """
        还原数据类型
        :param data: 取值数据
        :param str_data: 原始字符串数据
        :return:
        """
        pass
