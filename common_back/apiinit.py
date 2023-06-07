# -*- coding: utf-8 -*-

"""
@author:  gaojie
@File：apiinit.py
@IDE: PyCharm
@time: 2023-05-19 17:22
@description: 接口信息重组
"""
import json, logging, traceback, requests, re, jsonpath, allure, sys

from config import *
from common import handleyaml
from common import checkresult
from common import exceptions
from common import replacedata
from common import apisend


class RequestsInit:

    def standard_yaml(self, casedata):
        """
        判断测试用例格式是否有误
        :param casedata: 用例数据
        :return:
        """
        flag = True
        try:
            casedata_key = casedata.keys()
            # 判断一级关键字是否包含有：name, base_url, request, validate
            if "name" in casedata_key and "base_url" in casedata_key and "request" in casedata_key and "expect" in casedata_key:
                # 判断request下是否包含有： method，url，headers
                request_key = casedata['request'].keys()
                if "method" in request_key and "url" in request_key and "headers" in request_key:
                    logging.info("Yaml测试用例基础架构检查通过")
                else:
                    flag = False
                    logging.error("用例编写有误，request下必须包含：method，url，headers")
            else:
                flag = False
                logging.error("用例编写有误，一级关键字必须包含：name，base_url，request，expect")
        except:
            ex_type, ex_val, ex_stack = sys.exc_info()
            error_info = exceptions.get_error_info(ex_type, ex_val, ex_stack)
            logging.error("规范Yaml测试用例异常：%s", error_info)
            flag = False
        return flag


    def regroup_casedata(self, casedata):
        """
        重组用例
        :param casedata:
        :return:
        """
        # 校验用例信息
        flag = self.standard_yaml(casedata)
        if flag:
            casedata_key = casedata.keys()
            relevance_dict = {}
            # 判断是否存在关联用例
            if 'relevance' in casedata_key:#存在关联用例，先执行关联用例，获取关联参数值后再进行参数替换
                relevance_dict = self.get_relevance_data(casedata['relevance'])   # 请求关联用例，获取关联参数值
            casedata = replacedata.replace_value(casedata, relevance_dict)
        return casedata


    def get_relevance_data(self, relevance):
        """
        获取依赖参数值
        :param relevance:
        :return:
        """
        relevance_dict = {}
        if relevance:
            with allure.step("执行关联接口"):
                for rele_case in relevance:
                    api = rele_case['api']   # 关联用例接口
                    caseid = rele_case['caseid']   # 关联用例id
                    #读取用例信息

                    casedata = self.get_casedata(api, caseid)
                    case_send_data, recv_data = apisend.RequestsSend().excute_case(casedata)
                    if 'relevance_data' in rele_case.keys():
                        relevance_data = rele_case['relevance_data']  #参数提取列表
                        for param in relevance_data:
                            if param['relevance_type'] == 'response':  #从返回数据中提取参数值
                                value = jsonpath.jsonpath(recv_data, param['value'])
                                name = param['name']
                                relevance_dict[name] = value[0]
                            elif param['relevance_type'] == 'request': #从请求数据中提取参数值
                                value = jsonpath.jsonpath(case_send_data, param['value'])
                                name = param['name']
                                relevance_dict[name] = value[0]
        return relevance_dict

    def get_casedata(self, api, caseid):
        """
        获取用例信息
        :param api: 用例接口，bms.data.roles.roles_list
        :param caseid: 用例id
        :return:
        """
        api_list = api.split('.')
        api_path = ROOT_DIR
        for i in api_list:
            api_path += '/' + i
        api_path += '.yaml'
        api_data = handleyaml.read_yaml_data(api_path)
        casedata = api_data['case'][caseid]
        return casedata


    # # 规范YAML测试用例
    # def standard_yaml(self, casedata):
    #     try:
    #         casedata_key = casedata.keys()
    #         #判断一级关键字是否包含有：name, base_url, request, validate
    #         if "name" in casedata_key and "base_url" in casedata_key and "request" in casedata_key and "validate" in casedata_key:
    #             #判断request下是否包含有： method，url，headers
    #             request_key = casedata['request'].keys()
    #             if "method" in request_key and "url" in request_key and "headers" in request_key:
    #                 logging.info("Yaml测试用例基础架构检查通过")
    #                 # 重组用例信息
    #                 casedata = self.replace_value(casedata)
    #                 logging.info("重组后的用例信息：%s", casedata)
    #                 method = casedata['request'].pop('method')
    #                 url = casedata['base_url'] + casedata['request'].pop('url')
    #                 case_request = casedata['request']
    #                 logging.info("请求类型：%s，请求url：%s，请求数据：%s", method, url, case_request)
    #                 with allure.step("发送请求"):
    #                     allure.attach(name="请求类型", body=str(method))
    #                     allure.attach(name="请求地址", body=str(url))
    #                     allure.attach(name="请求头", body=str(case_request['headers']))
    #                     if "json" in case_request.keys():
    #                         allure.attach(name="请求参数", body=str(case_request['json']))
    #                     recv_result = requests.request(method, url, **case_request)   #发送请求
    #                 result_code = recv_result.status_code
    #                 result_text = recv_result.text
    #                 result_json = recv_result.json()
    #                 hope_result = casedata['validate']
    #                 checkresult.check_result(hope_result, result_json, result_code)    #断言
    #                 # 提取值并写入extract.yaml文件
    #                 if "extract" in casedata_key:
    #                     for key, value in casedata['extract'].items():
    #                         if "(.*?)" in value or "(.+?)" in value: #正则表达式
    #                             zz_value = re.search(value, result_text)
    #                             if zz_value:
    #                                 extract_value = {key: zz_value.group(1)}
    #                         else: #jsonpath
    #                             js_value = jsonpath.jsonpath(result_json, value)
    #                             if js_value:
    #                                 extract_value = {key: js_value[0]}
    #                         logging.info("extract_value:%s",extract_value)
    #                         handleyaml.write_yaml_data(EXTRACT_DIR, extract_value)
    #             else:
    #                 logging.error("用例编写有误，request下必须包含：method，url，headers")
    #         else:
    #             logging.error("用例编写有误，一级关键字必须包含：name，base_url，request，validate")
    #
    #     except Exception as e:
    #         error_info = traceback.format_exc()
    #         logging.error("规范Yaml测试用例异常：%s", error_info)

    # def replace_value(self,data):
    #     """
    #     参数替换
    #     :param data:
    #     :return:
    #     """
    #     if data:
    #         # 保存数据类型
    #         data_type = type(data)
    #         # 判断数据类型
    #         if isinstance(data, dict) or isinstance(data, list):
    #             str_data = json.dumps(data)
    #         else:
    #             str_data = str(data)
    #         #替换
    #         for cs in range(1, str_data.count('${') + 1):
    #             if '${' in str_data and '}' in str_data:
    #                 start_index = str_data.index("${")
    #                 end_index = str_data.index("}", start_index)
    #                 old_value = str_data[start_index:end_index + 1]
    #                 replace_type = old_value[2:old_value.index('(')]
    #                 args_value = old_value[old_value.index('(') + 1:old_value.index(')')]
    #                 if replace_type == 'config':
    #                     new_value = handleyaml.get_yaml_value(CONFIG_DIR,args_value)
    #                 elif replace_type == 'extract':
    #                     new_value = handleyaml.get_yaml_value(EXTRACT_DIR,args_value)
    #                 else: #其它取值方式，后续补充
    #                     new_value = ""
    #                 # str_data = str_data.replace(old_value,new_value)
    #                 # 数字类型去掉“”
    #                 if isinstance(new_value, int) or isinstance(new_value, float):
    #                     str_data = str_data.replace('"' + old_value + '"', str(new_value))
    #                 else:
    #                     str_data = str_data.replace(old_value, str(new_value))
    #         #还原数据类型
    #         if isinstance(data, dict) or isinstance(data, list):
    #             data = json.loads(str_data)
    #         else:
    #             data = data_type(str_data)
    #     return data




















