# -*- coding: utf-8 -*-

"""
@author:  gaojie
@File：apisend.py
@IDE: PyCharm
@time: 2023-05-21 15:54
@description: 发送请求
"""
import json, logging, requests, allure, os, random
from requests_toolbelt import MultipartEncoder
from common import apiinit
from common import checkresult


class RequestsSend:
    """封装发送请求"""

    def excute_case(self, case_data):
        """
        执行用例
        :param case_data: 用例信息
        :return:
        """
        # 重组用例信息
        logging.info('-·-·-·-·-·-·-·-·-·-发送请求并接受信息 START-·-·-·-·-·-·-·-·-·-')
        case_data = apiinit.RequestsInit().regroup_casedata(case_data)
        logging.info("重组后的用例信息：%s", case_data)
        # 发送请求
        with allure.step("执行当前接口：" + case_data['name']):
            recv_data, recv_code = self.send_request(case_data)
        #结果校验
            with allure.step("结果校验"):
                hope_result = case_data['expect']
                checkresult.check_result(hope_result, recv_data, recv_code)
        #执行后置接口
        self.case_teardown(case_data)
        logging.info('-·-·-·-·-·-·-·-·-·-发送请求并接受信息 END-·-·-·-·-·-·-·-·-·-')
        return case_data, recv_data

    def case_teardown(self, case_data):
        """
        后置请求处理
        :param case_data: 用例信息
        :return:
        """
        if 'teardown' in case_data.keys():
            for teardown_case in case_data['teardown']:
                api = teardown_case['api']   # 后置用例接口
                caseid = teardown_case['caseid']   # 关联用例id

                #读取用例信息
                casedata = apiinit.RequestsInit().get_casedata(api, caseid)
                with allure.step("执行后置接口"):
                    case_send_data, recv_data = self.excute_case(casedata)

    def send_request(self, case_data):
        """
        发送请求
        :param case_data: 用例信息
        :return:
        """
        request_data = case_data['request']
        url = case_data['base_url'] + request_data['url']
        method = request_data['method']
        headers = request_data['headers']
        logging.info("请求地址：%s", url)
        logging.info("请求方法：%s", method)
        logging.info("请求头：%s", headers)
        data = None
        file = None
        # print("request_data:%s", request_data)
        if 'data' in request_data.keys():
            data = request_data['data']
            logging.info("请求参数：%s", data)
        if 'file' in request_data.keys():
            file = request_data['file']

        if method == 'post':
            recv_data, recv_code = self.post(url, headers, data, file)
        elif method == 'get':
            recv_data, recv_code = self.get(url, headers, data)
        elif method == 'put':
            recv_data, recv_code = self.put(url, headers, data)
        elif method == 'delete':
            recv_data, recv_code = self.delete(url, headers, data)
        else:
            recv_data = ""
            recv_code = ""
        return recv_data, recv_code

    def post(self, url, headers, data=None, file=None):
        """
        post请求
        :param url: 请求地址
        :param headers: 请求头
        :param data: 请求数据
        :param file: 请求文件
        :return:
        """
        with allure.step("POST请求"):
            allure.attach(name="请求地址", body=url)
            allure.attach(name="请求头", body=str(headers))
            if data:
                allure.attach(name="请求参数", body=str(data))

            if "application/json" in headers.values():
                print(data)
                print(type(data))
                recv_result = requests.post(url=url, headers=headers, json=data, verify=False)
            elif "multipart/form-data" in headers.values():
                for key in file:
                    value = file[key]
                    # 判定参数值是否为文件，如果是则替换为二进制值
                    if '/' in value:
                        file[key] = (os.path.basename(value), open(value, 'rb'))
                enc = MultipartEncoder(
                    fields=file,
                    boundary='--------------' + str(random.randint(1e28, 1e29 - 1))
                )
                headers['Content-Type'] = enc.content_type
                recv_result = requests.post(url=url, data=enc, headers=headers, verify=False)
            else:
                if data:
                    data = json.dumps(data)
                recv_result = requests.post(url=url, headers=headers, data=data, verify=False)
            try:
                res = recv_result.json()
            except:
                res = recv_result.text
            logging.info("请求接口结果： %s", str(res))
            allure.attach(name="请求结果", body=str(res))
        return res, recv_result.status_code

    def get(self, url, headers, data=None):
        """
        get请求
        :param url: 请求地址
        :param headers: 请求头
        :param data: 请求数据
        :return:
        """
        with allure.step("GET请求"):
            allure.attach(name="请求地址", body=url)
            allure.attach(name="请求头", body=str(headers))
            if data:
                allure.attach(name="请求参数", body=str(data))
            recv_result = requests.get(url=url, headers=headers, params=data, verify=False)
            try:
                res = recv_result.json()
            except:
                res = recv_result.text
            logging.info("请求接口结果： %s", str(res))
            allure.attach(name="请求结果", body=str(res))
        return res, recv_result.status_code

    def put(self,url, headers, data=None):
        """
        put请求
        :param url: 请求地址
        :param headers: 请求头
        :param data: 请求数据
        :return:
        """
        with allure.step("PUT请求"):
            allure.attach(name="请求地址", body=url)
            allure.attach(name="请求头", body=str(headers))
            if data:
                allure.attach(name="请求参数", body=str(data))
            if 'application/json' in headers.values():
                recv_result = requests.put(url=url, headers=headers, json=data, verify=False)
            else:
                if data:
                    data = json.dumps(data)
                recv_result = requests.put(url=url, headers=headers, data=data, verify=False)
            try:
                res = recv_result.json()
            except:
                res = recv_result.text
            logging.info("请求接口结果： %s", str(res))
            allure.attach(name="请求结果", body=str(res))
        return res, recv_result.status_code

    def delete(self, url, headers, data=None):
        """
        delete请求
        :param url: 请求地址
        :param headers: 请求头
        :param data: 请求数据
        :return:
        """
        with allure.step("DELETE请求"):
            allure.attach(name="请求地址", body=url)
            allure.attach(name="请求头", body=str(headers))
            if data:
                allure.attach(name="请求参数", body=str(data))
            recv_result = requests.delete(url=url, params=data, headers=headers, verify=False)
            try:
                res = recv_result.json()
            except:
                res = recv_result.text
            logging.info("请求接口结果： %s", str(res))
            allure.attach(name="请求结果", body=str(res))
        return res, recv_result.status_code
