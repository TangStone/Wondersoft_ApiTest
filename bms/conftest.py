# -*- coding: utf-8 -*-

"""
@author:  gaojie
@File：conftest.py
@IDE: PyCharm
@time: 2023-05-29 10:18
@description:
"""
import pytest
from config import *
from common import handleyaml
from common import apisend
from common import basefunc

@pytest.fixture(scope='session', autouse=True)
def login_init():
    """
    登录获取token值
    :return:
    """
    casedata = handleyaml.read_yaml_data(ROOT_DIR + "bms/data/login/login.yaml")['case']['login_01']

    case_send_data, recv_data = apisend.RequestsSend().excute_case(casedata)

    #获取token值
    token = recv_data['data']['token']

    extract_value = {"token": token}

    handleyaml.update_yaml_value(EXTRACT_DIR, extract_value)

@pytest.fixture(scope='session', autouse=True)
def remove_tmp():
    """
    清空report/tmp目录
    :return:
    """
    #临时文件目录
    tmp_path = ROOT_DIR + 'report/tmp'

    basefunc.clean_dir(tmp_path)

@pytest.fixture(scope='session', autouse=True)
def clear_yaml():
    handleyaml.clear_yaml_data(EXTRACT_DIR)