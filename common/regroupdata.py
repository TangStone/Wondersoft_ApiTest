# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: regroupdata.py
@IDE: PyCharm
@time: 2023-06-04 20:19
@description: 参数替换
"""
import json, re, sys, logging, time, datetime

import jsonpath

from config import *

from common import exceptions
from common import encryption
from common.basefunc import config_dict

class RegroupData:
    """
    参数替换
    """

    def __init__(self, casedata, relevance_dict, extract_dict, db_dict):
        """
        :param casedata: 用例信息
        :param relevance_dict: 关联参数
        :param extract_dict: 全局参数
        :param config_dict: 配置参数
        :param db_dict: 数据库查询参数
        """
        self.casedata = casedata
        self.relevance_dict = relevance_dict
        self.extract_dict = extract_dict
        self.config_dict = config_dict
        self.db_dict = db_dict
        # logging.info("casedata:%s", self.casedata)
        # logging.info("relevance_dict:%s", self.relevance_dict)
        # logging.info("extract_dict:%s", self.extract_dict)
        # logging.info("config_dict:%s", self.config_dict)

    @staticmethod
    def get_value(param, data):
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
                    if pa_list[0] == 'type':   #返回整个列表，针对a[*]取值类型
                        return data
            else:
                if type(data) == list: #中间件参数使用jsonpath提取的是列表，取第一个值
                    return data[0]
                else:
                    return data

    def eval_data(self, param):
        """
        还原数据类型
        :param param: key
        :return:
        """
        param_list = param.split(";;")  # 拆分取值需求 ${relevance(fileContent)};path=filelist[0].md5
        value = self.replace_value(param_list[0])
        try:
            path = None
            if len(param_list) >= 2:
                for pa in param_list[1:]:
                    pa_list = pa.split("=")
                    if pa_list[0] == 'path':  # 获取字典中的特定值
                        value = value.replace("\\", '/')
                        path = '$.' + pa_list[1]
                    if pa_list[0] == 'cal':   #计算
                        value = value + pa_list[1]
            str_data = eval(value)
            if path:
                str_data = jsonpath.jsonpath(str_data, path)[0]
        except:
            str_data = value
        return str_data

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
        param_list = str.split(';')   #获取多个配置项
        time_str = datetime.datetime.now()   #获取当前时间
        format = None
        for param in param_list:
            pa_list = param.split('=')  #拆分配置项
            if pa_list[0] == 'format':   #时间格式
                format = pa_list[1]
                # time_str = time.strftime(pa_list[1])
            if pa_list[0] == 'cal':   #时间偏移
                cal_list = pa_list[1].split(',')
                for cal in cal_list:
                    num = int(cal[2:])
                    if cal[1] == '+': #向后偏移
                        if cal[0] == 'w':  #周偏移
                            time_str += datetime.timedelta(weeks=num)
                        elif cal[0] == 'd': #天偏移
                            time_str += datetime.timedelta(days=num)
                        elif cal[0] == 'h': #天偏移
                            time_str += datetime.timedelta(hours=num)
                        elif cal[0] == 'm': #分钟偏移
                            time_str += datetime.timedelta(minutes=num)
                        else:
                            raise Exception("暂不支持此种时间偏移：" + pa_list[1])
                    elif cal[1] == '-': #向前偏移
                        if cal[0] == 'w':  #周偏移
                            time_str -= datetime.timedelta(weeks=num)
                        elif cal[0] == 'd': #天偏移
                            time_str -= datetime.timedelta(days=num)
                        elif cal[0] == 'h': #天偏移
                            time_str -= datetime.timedelta(hours=num)
                        elif cal[0] == 'm': #分钟偏移
                            time_str -= datetime.timedelta(minutes=num)
                        else:
                            raise Exception("暂不支持此种时间偏移：" + pa_list[1])
        if format:
            time_str = time_str.strftime(format)
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
        db_list = re.findall(r"\$\{db\((.*?)\)\}", str_data)  # 配置文件参数替换
        extract_list = re.findall(r"\$\{extract\((.*?)\)\}", str_data)  # 配置文件参数替换
        enc_list = re.findall(r"\$\{enc\((.*?)\)\}", str_data)  # 加密替换
        time_list = re.findall(r"\$\{GetTime\((.*?)\)\}", str_data)  # 时间

        if len(Eval_list):
            for i in Eval_list:
                value = self.eval_data(i)
                if str_data[0:7] == '${Eval(' and str_data[-2:] == ')}':  #当前值需要转换类型
                    return value
                else:  #返回字符串
                    rep_data = '${Eval(' + i + ')}'
                    str_data = str_data.replace(rep_data, str(value), 1)
                    return str_data

        if len(time_list):
            for i in time_list:
                value = self.get_time(i)
                if '+' in i:   #日期向后偏移时 +字符转换
                    i = i.replace('+', '\+')
                pattern = re.compile(r'\$\{GetTime\(' + i + r'\)\}')
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

        if len(db_list):
            for i in db_list:
                pattern = re.compile(r'\$\{db\(' + i + r'\)\}')
                value = self.get_value(i, self.db_dict)
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
