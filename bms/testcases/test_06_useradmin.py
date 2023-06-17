# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_06_useradmin.py
@IDE: PyCharm
@time: 2023-06-17 22:46
@description: 管理员配置模块测试用例
"""
import logging, pytest
import time

from config import *
from common import readcase
from common import runcase
from common import handleallure

class TestUserAdmin:
    """
    管理员配置模块
    """

    # 管理员批量创建
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/useradmin/useradmin_add.yaml').items()])
    def test_useradmin_add(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 管理员列表查询
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/useradmin/useradmin_list.yaml').items()])
    def test_useradmin_list(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 管理员密码修改
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/useradmin/useradmin_passwd_update.yaml').items()])
    def test_useradmin_passwd_update(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 管理员密码重置
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/useradmin/useradmin_passwd_reset.yaml').items()])
    def test_useradmin_passwd_reset(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 管理员修改
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/useradmin/useradmin_update.yaml').items()])
    def test_useradmin_update(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # # 管理员删除
    # @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
    #                                               readcase.ReadCase().get_case_dict(
    #                                                   ROOT_DIR + 'bms/data/useradmin/useradmin_delete.yaml').items()])
    # def test_useradmin_delete(self, caseid, casedata):
    #     handleallure.allure_display(casedata)
    #     logging.info("==========开始执行用例：%s==========", caseid)
    #     runcase.excute_case(casedata)
