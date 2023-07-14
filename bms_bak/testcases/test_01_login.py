# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_01_login.py
@IDE: PyCharm
@time: 2023-06-14 11:05
@description: 用户登录模块测试用例
"""
import logging, pytest

from config import *
from common import readcase
from common import runcase
from common import handleyaml
from common import handleallure

class TestLogin:
    """
    登录模块测试用例
    """

    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata ) for caseid, casedata in readcase.ReadCase().get_case_dict(ROOT_DIR + 'bms/data/login/login.yaml').items()])
    def test_login(self, caseid, casedata):
        handleallure.allure_display(casedata)

        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)
        # send_data, recv_data = runcase.excute_case(casedata)

        # if caseid == 'login_01':
        #     # 获取token值
        #     token = recv_data['data']['token']   #token值
        #     userId = recv_data['data']['userId']
        #     extract_value = {"token": token, 'userId': userId}
        #
        #     handleyaml.YamlHandle(EXTRACT_DIR, extract_value).updata_yaml()   #保存到临时中间文件extract.yaml中
