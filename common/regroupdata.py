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
from common import handleyaml
from common.basefunc import config_dict

class RegroupData:
    """
    参数替换
    """

    def __init__(self, api_casedata, temp_var_dict):
        """
        :param api_casedata: 接口用例信息
        :param temp_var_dict: 临时变量字典
        """
        self.api_casedata = api_casedata    # 接口用例信息
        self.global_var_dict = handleyaml.YamlHandle(EXTRACT_DIR).read_yaml()   #全局变量字典
        self.temp_var_dict = temp_var_dict  # 临时变量字典
        self.env_var_dict = config_dict     # 环境变量字典
        # logging.info("api_casedata:%s", self.api_casedata)
        # logging.info("global_var_dict:%s", self.global_var_dict)
        # logging.info("temp_var_dict:%s", self.temp_var_dict)
        # logging.info("env_var_dict:%s", self.env_var_dict)

    def get_value(self, param):
        """
        获取参数值
        :param param: 取值参数
        :return:
        """
        # 从临时变量字典中取值
        if self.temp_var_dict and param in self.temp_var_dict.keys():
            return self.temp_var_dict[param]
        # 从全局变量中取值
        elif self.global_var_dict and param in self.global_var_dict.keys():
            return self.global_var_dict[param]
        # 从环境变量中取值
        elif self.env_var_dict and param in self.env_var_dict.keys():
            return self.env_var_dict[param]
        else:
            raise Exception("参数取值失败，参数名：%s" % param)

    def eval_data(self, param):
        """
        还原数据类型
        :param param: key
        :return:
        """
        param_list = param.split(";")  # 拆分取值需求 ${relevance(fileContent)};path=filelist[0].md5
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

    def regroup_case_data(self):
        """
        重组用例数据
        :return:
        """
        sign, rawDict = self.regroup_dict(self.api_casedata)
        return sign, rawDict

    def regroup_dict(self, rawDict):
        """
        递归重组接口用例数据
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
        var_list = re.findall(r"\$\{(.*?)\}", str_data)  # 变量替换
        eval_list = re.findall(r"\$Eval\((.*)\)", str_data)  # 格式转换,非贪婪模式
        enc_list = re.findall(r"\$Enc\((.*?)\)", str_data)  # 加密
        time_list = re.findall(r"\$GetTime\((.*?)\)", str_data)  # 时间

        if len(eval_list):
            for i in eval_list:
                value = self.eval_data(i)
                if str_data[0:6] == '$Eval(' and str_data[-1:] == ')':  #当前值需要转换类型
                    return value
                else:  #返回字符串
                    rep_data = '$Eval(' + i + ')'
                    str_data = str_data.replace(rep_data, str(value), 1)
                    return str_data

        if var_list:
            for var in var_list:
                pattern = re.compile(r'\$\{' + var + r'\}')
                value = self.get_value(var)
                str_data = re.sub(pattern, str(value), str_data, count=1)

        if len(enc_list):
            for i in enc_list:
                pattern = re.compile(r'\$Enc\(' + i + r'\)')
                value = self.get_enc_value(i)
                str_data = re.sub(pattern, str(value), str_data, count=1)

        if len(time_list):
            for i in time_list:
                value = self.get_time(i)
                if '+' in i:   #日期向后偏移时 +字符转换
                    i = i.replace('+', '\+')
                pattern = re.compile(r'\$GetTime\(' + i + r'\)')
                str_data = re.sub(pattern, str(value), str_data, count=1)

        return str_data
