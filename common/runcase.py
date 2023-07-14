# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: runcase.py
@IDE: PyCharm
@time: 2023-06-04 19:41
@description:
"""
import copy
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
from common import extract
from common import database
from common import handledict

class RunCase:
    """
    执行测试用例
    """

    def __init__(self):
        self.temp_var_dict = {}  # 临时变量字典

    def excute_case(self, casedata):
        """
        执行测试用例
        :param casedata: 用例信息
        :return:
        """
        if 'steps' in casedata.keys():
            # 获取测试步骤中的接口用例列表
            get_apicase_list = readcase.ReadCase().get_apicase_list(casedata)
            # 遍历接口用例列表
            for apicase in get_apicase_list:
                api_path = API_DIR + apicase['api_path']  # 接口用例路径
                api = apicase['api']  # 接口用例
                api_caseid = apicase['data']  # 接口用例id
                # 获取接口用例数据
                api_casedata = readcase.ReadCase().get_api_casedata(api_path, api, api_caseid)
                # 执行接口用例
                with allure.step(api_casedata['name']):
                    self.excute_apicase(api, api_casedata)

    def excute_apicase(self, api, api_casedata):
        """
        执行接口用例
        :param api: 接口
        :param api_casedata: 接口用例数据
        :return:
        """
        logging.info('-·-·-·-·-·-·-·-·-·-执行接口 START：%s-·-·-·-·-·-·-·-·-·-', api)
        # 校验用例格式
        flag, msg = handleyaml.standard_yaml(api_casedata)
        if flag:  # 用例格式无误
            # 判断是否存在前置操作
            if 'preProcessors' in api_casedata.keys():
                # 判断是否存在前置操作-数据库操作
                if 'database' in api_casedata['preProcessors'].keys():
                    # 执行数据库操作，获取参数
                    db_dict = database.SetUpDB().get_setup_sql_data(api_casedata['preProcessors']['database'])
                    # 更新临时变量字典
                    self.temp_var_dict = handledict.dict_update(self.temp_var_dict, db_dict)

            # 重组接口用例数据
            sign, api_casedata = regroupdata.RegroupData(api_casedata, self.temp_var_dict).regroup_case_data()
            if sign:  # 重组数据成功
                logging.info("重组后的用例信息：%s", api_casedata)
                # 发送请求
                recv_data, recv_code = send_request(api_casedata)
                # 结果校验
                hope_result = api_casedata['postProcessors']['assert']
                checkresult.check_result(hope_result, recv_data, recv_code)
                # 提取变量
                if 'extract' in api_casedata['postProcessors'].keys():
                    temp_value = extract.handle_extarct(api_casedata['postProcessors']['extract'], recv_data, api_casedata)
                    self.temp_var_dict = handledict.dict_update(self.temp_var_dict, temp_value)
                logging.info('-·-·-·-·-·-·-·-·-·-执行接口 END：%s-·-·-·-·-·-·-·-·-·-', api)
                return api_casedata, recv_data
            else:
                raise Exception(api_casedata)
        else:
            logging.error("用例格式错误：%s", msg)
            raise Exception("用例格式校验失败，" + msg)

def excute_apicase(api_casedata):
    """
    执行用例
    :param api_casedata: 接口用例数据
    :return:
    """
    logging.info('-·-·-·-·-·-·-·-·-·-发送请求并接受信息 START-·-·-·-·-·-·-·-·-·-')
    # 校验用例格式
    flag, msg = handleyaml.standard_yaml(api_casedata)
    if flag:  # 用例格式无误
        extract_dict = handleyaml.YamlHandle(EXTRACT_DIR).read_yaml()  # 全局参数
        db_dict = {}   #数据库参数
        # 判断是否存在前置操作
        if 'preProcessors' in api_casedata.keys():
            # 判断是否存在前置操作-数据库操作
            if 'database' in api_casedata['preProcessors'].keys():
                db_dict = database.SetUpDB().get_setup_sql_data(api_casedata['preProcessors']['database'])
        # relevance_dict = {}  # 关联参数
        # # 判断是否存在关联用例，若存在，执行前置用例获取参数值
        # if 'relevance' in case_data.keys():
        #     relevance_dict = relevancecase.Relevance().get_relevance_data(case_data['relevance'])

        # 重组用例信息
        # casedata = regroupdata.RegroupData(case_data, relevance_dict, extract_dict, config_dict).replace_value()
        sign, casedata = regroupdata.RegroupData(copy.deepcopy(case_data), relevance_dict, extract_dict,
                                                 db_dict).regroup_case_data()
        if sign == 'success':
            logging.info("重组后的用例信息：%s", casedata)
            # 发送请求
            recv_data, recv_code = send_request(casedata)
            # 结果校验
            hope_result = casedata['validate']
            checkresult.check_result(hope_result, recv_data, recv_code)
            # 取值
            if 'extract' in casedata.keys():
                extract.handle_extarct(casedata['extract'], recv_data, casedata['caseid'])
            # 执行后置接口
            teardowncase.case_teardown(casedata)
            logging.info('-·-·-·-·-·-·-·-·-·-发送请求并接受信息 END-·-·-·-·-·-·-·-·-·-')
            return casedata, recv_data
        else:
            raise Exception(casedata)
    else:
        raise Exception("用例格式校验失败，" + msg)


def send_request(casedata):
    """
    发送请求
    :param casedata: 用例信息
    :return:
    """
    with allure.step("发送请求"):
        request_data = casedata['request']
        url = casedata['base_url'] + request_data['address']
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
            logging.info("上传文件：%s", file)
            allure.attach(name="上传文件", body=str(file))

        #发送请求
        if method in ['post', 'POST']:
            recv_data, recv_code = ApiMethod(url, headers, data, file).post()
        elif method in ['get', 'GET']:
            recv_data, recv_code = ApiMethod(url, headers, data, file).get()
        elif method in ['put', 'PUT']:
            recv_data, recv_code = ApiMethod(url, headers, data, file).put()
        elif method in ['delete', 'DELETE']:
            recv_data, recv_code = ApiMethod(url, headers, data, file).delete()
        else:
            raise Exception("暂不支持" + method + "请求类型！")
        return recv_data, recv_code


class ApiMethod:
    """
    request请求封装
    """

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
            if self.file:
                for key in self.file:
                    value = self.file[key]
                    # 判定参数值是否为文件，如果是则替换为二进制值
                    # if '/' in value:
                    file_path = FILE_DIR + '/' + value
                    self.file[key] = (os.path.basename(file_path), open(file_path, 'rb'), 'application/octet-stream')
                if self.data:
                    self.file = dict(self.file, **self.data)
                multipart = MultipartEncoder(
                    fields=self.file
                    # boundary='-----------------------------' + str(random.randint(int(1e28), int(1e29 - 1)))
                )
                self.headers['Content-Type'] = multipart.content_type
                recv_result = requests.post(url=self.url, data=multipart, headers=self.headers, verify=False)
            else:
                recv_result = requests.post(url=self.url, headers=self.headers, data=self.data, verify=False)
        else:
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
                self.data = json.dumps(self.data)
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
        if 'application/json' in self.headers.values():
            recv_result = requests.delete(url=self.url, json=self.data, headers=self.headers, verify=False)
        else:
            recv_result = requests.delete(url=self.url, params=self.data, headers=self.headers, verify=False)
        try:
            res = recv_result.json()
        except:
            res = recv_result.text
        logging.info("请求接口结果： %s", str(res))
        allure.attach(name="请求结果", body=str(res))
        return res, recv_result.status_code
