# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_05_userrole.py
@IDE: PyCharm
@time: 2023-06-15 19:29
@description: 职位管理模块测试用例
"""
import logging, pytest

from config import *
from common import readcase
from common import runcase
from common import handleallure

class TestUserRole:
    """
    职位管理模块
    """

    # 新增职位
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/userrole/userrole_add.yaml').items()])
    def test_userrole_add(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 职位列表搜索
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/userrole/userrole_list.yaml').items()])
    def test_userrole_list(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 修改职位
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/userrole/userrole_update.yaml').items()])
    def test_userrole_update(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 删除职位
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/userrole/userrole_delete.yaml').items()])
    def test_userrole_delete(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

