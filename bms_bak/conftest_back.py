# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: conftest.py
@IDE: PyCharm
@time: 2023-06-04 22:04
@description:
"""
import logging

import pytest, allure
from config import *
from common import handleyaml
from common import runcase
from common import basefunc
from common import readcase

# @pytest.fixture(scope='session', autouse=True)
# def login_init():
#     """
#     登录获取token值
#     :return:
#     """
#     caseid = 'login_01'
#     case_data = readcase.ReadCase().get_case_dict(ROOT_DIR + 'bms/data/login/login.yaml')[caseid]
#     logging.info("case_data:%s", case_data)
#     # 获取所有测试用例
#     # all_case_dict = readcase.ReadCase().read_all_case(ROOT_DIR + 'bms/data/')
#
#     # caseid = 'login_01'
#     #
#     # # 获取用例数据
#     # case_info = readcase.all_case[caseid]
#     # case_data = readcase.ReadCase().get_case_data(caseid, case_info['casepath'])
#     #发送请求
#     send_data, recv_data = runcase.excute_case(case_data)
#
#     #获取token值
#     token = recv_data['data']['token']
#     extract_value = {"token": token}
#
#     handleyaml.YamlHandle(EXTRACT_DIR, extract_value).updata_yaml()


@pytest.fixture(scope='session', autouse=True)
def remove_tmp():
    """
    清空report/tmp目录
    :return:
    """
    #清空临时文件目录
    basefunc.clean_dir(ROOT_DIR + 'report/tmp')
    #清空报告
    basefunc.clean_dir(ROOT_DIR + 'report/report')

@pytest.fixture(scope='session', autouse=True)
def clear_yaml():
    handleyaml.YamlHandle(EXTRACT_DIR).clear_yaml()