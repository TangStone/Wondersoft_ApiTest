# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: runcase.py
@IDE: PyCharm
@time: 2023-06-04 19:41
@description:
"""
import logging, allure, sys, requests, random, json
from requests_toolbelt import MultipartEncoder

from config import *
from common import readcase
from common import handleyaml
from common import regroupdata
from common import exceptions
from common import checkresult
from common import teardowncase
from common import relevancecase

def excute_case(case_data):
    """
    执行用例
    :param case_data: 用例数据
    :return:
    """
    logging.info('-·-·-·-·-·-·-·-·-·-发送请求并接受信息 START-·-·-·-·-·-·-·-·-·-')

    # 校验用例格式
    flag = handleyaml.standard_yaml(case_data)
    if flag:  # 用例格式无误

        relevance_dict = {}  # 关联参数
        # 判断是否存在关联用例，若存在，执行前置用例获取参数值
        if 'relevance' in case_data.keys():
            relevance_dict = relevancecase.Relevance().get_relevance_data(case_data['relevance'])
        extract_dict = handleyaml.YamlHandle(EXTRACT_DIR).read_yaml()  # 全局参数
        config_dict = handleyaml.YamlHandle(CONFIG_DIR).read_yaml()  # 配置参数
        # 重组用例信息
        # casedata = regroupdata.RegroupData(case_data, relevance_dict, extract_dict, config_dict).replace_value()
        sign, casedata = regroupdata.RegroupData(case_data, relevance_dict, extract_dict,
                                                 config_dict).regroup_case_data()
        if sign == 'success':
            logging.info("重组后的用例信息：%s", casedata)

            # 发送请求
            recv_data, recv_code = send_request(casedata)

            # 结果校验
            hope_result = casedata['expect']
            checkresult.check_result(hope_result, recv_data, recv_code)

            # 取值
            if 'expect' in casedata.keys():
                pass

            # 执行后置接口
            teardowncase.case_teardown(casedata)

    logging.info('-·-·-·-·-·-·-·-·-·-发送请求并接受信息 END-·-·-·-·-·-·-·-·-·-')
    return casedata, recv_data


def send_request(casedata):
    """
    发送请求
    :param casedata: 用例信息
    :return:
    """
    with allure.step("执行当前接口：" + casedata['name']):
        request_data = casedata['request']
        url = casedata['base_url'] + request_data['url']
        method = request_data['method']
        headers = request_data['headers']

        logging.info("请求地址：%s", url)
        logging.info("请求方法：%s", method)
        logging.info("请求头：%s", headers)

        allure.attach(name="请求方法：", body=method)
        allure.attach(name="请求地址", body=url)
        allure.attach(name="请求头", body=str(headers))

        data = None
        file = None
        if 'data' in request_data.keys():
            data = request_data['data']
            logging.info("请求参数：%s", data)
            allure.attach(name="请求参数", body=str(data))
        if 'file' in request_data.keys():
            file = request_data['file']

        #发送请求
        if method == 'post':
            recv_data, recv_code = ApiMethod(url, headers, data, file).post()
        elif method == 'get':
            recv_data, recv_code = ApiMethod(url, headers, data, file).get()
        elif method == 'put':
            recv_data, recv_code = ApiMethod(url, headers, data, file).put()
        elif method == 'delete':
            recv_data, recv_code = ApiMethod(url, headers, data, file).delete()
        else:
            pass
        return recv_data, recv_code


class ApiMethod:
    "request请求封装"

    def __init__(self, url, headers, data=None, file=None):
        self.url = url
        self.headers = headers
        self.data = data
        self.file = file

    #post请求
    def post(self):
        if "application/json" in self.headers.values():
            recv_result = requests.post(url=self.url,
                                        headers=self.headers,
                                        json=self.data, verify=False)
        elif "multipart/form-data" in self.headers.values():
            for key in self.file:
                value = self.file[key]
                # 判定参数值是否为文件，如果是则替换为二进制值
                if '/' in value:
                    self.file[key] = (os.path.basename(value), open(value, 'rb'))
            enc = MultipartEncoder(
                fields=self.file,
                boundary='--------------' + str(random.randint(1e28, 1e29 - 1))
            )
            self.headers['Content-Type'] = enc.content_type
            recv_result = requests.post(url=self.url, data=enc, headers=self.headers, verify=False)
        else:
            if self.data:
                data = json.dumps(self.data)
            recv_result = requests.post(url=self.url, headers=self.headers, data=self.data, verify=False)
        try:
            res = recv_result.json()
        except:
            res = recv_result.text
        logging.info("请求接口结果： %s", str(res))
        allure.attach(name="请求结果", body=str(res))
        return res, recv_result.status_code

    #get请求
    def get(self):
        recv_result = requests.get(url=self.url, headers=self.headers, params=self.data, verify=False)
        try:
            res = recv_result.json()
        except:
            res = recv_result.text
        logging.info("请求接口结果： %s", str(res))
        allure.attach(name="请求结果", body=str(res))

        return res, recv_result.status_code

    #put请求
    def put(self):
        if 'application/json' in self.headers.values():
            recv_result = requests.put(url=self.url, headers=self.headers, json=self.data, verify=False)
        else:
            if self.data:
                data = json.dumps(self.data)
            recv_result = requests.put(url=self.url, headers=self.headers, data=self.data, verify=False)
        try:
            res = recv_result.json()
        except:
            res = recv_result.text
        logging.info("请求接口结果： %s", str(res))
        allure.attach(name="请求结果", body=str(res))
        return res, recv_result.status_code

    #delete请求
    def delete(self):
        recv_result = requests.delete(url=self.url, params=self.data, headers=self.headers, verify=False)
        try:
            res = recv_result.json()
        except:
            res = recv_result.text
        logging.info("请求接口结果： %s", str(res))
        allure.attach(name="请求结果", body=str(res))
        return res, recv_result.status_code
