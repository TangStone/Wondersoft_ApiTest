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
from common.readcase import ReadCase
from common.runcase import RunCase

@pytest.fixture(scope='session', autouse=True)
def login_init():
    """
    登录获取token值
    :return:
    """
    api_path = API_DIR + '/bms/login/login.yaml'  # 接口用例路径
    api = 'login'  # 接口用例
    api_caseid = 'login_01'  # 接口用例id
    # 获取接口用例数据
    api_casedata = ReadCase().get_api_casedata(api_path, api, api_caseid)
    # 执行接口用例
    RunCase().excute_apicase(api, api_casedata)
