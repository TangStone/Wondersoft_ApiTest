# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_03_syncManage.py
@IDE: PyCharm
@time: 2023-06-15 19:07
@description: 用户推送模块测试用例
"""
import logging, pytest

from config import *
from common import readcase
from common import runcase
from common import handleallure

class TestUserSyncManage:
    """
    用户推送模块
    """

    # 同步用户列表状态查询
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/usersyncManage/usersyncManage_list.yaml').items()])
    def test_usersyncManage_list(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 用户推送
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/usersyncManage/usersyncManage_push.yaml').items()])
    def test_usersyncManage_push(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)