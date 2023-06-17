# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_100_delete.py
@IDE: PyCharm
@time: 2023-06-17 22:55
@description: 后置删除用例模块
"""
import logging, pytest

from config import *
from common import readcase
from common import runcase
from common import handleallure

class Delete:
    """
    删除模块
    """

    # 删除用户
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/user/user_delete.yaml').items()])
    def test_user_delete(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 删除用户组
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/user/user_group_delete.yaml').items()])
    def test_user_group_delete(self, caseid, casedata):
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

    # 角色删除
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/role/role_delete.yaml').items()])
    def test_role_delete(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 管理员删除
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/useradmin/useradmin_delete.yaml').items()])
    def test_useradmin_delete(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)