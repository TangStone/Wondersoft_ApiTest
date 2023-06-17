# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_06_role.py
@IDE: PyCharm
@time: 2023-06-16 17:49
@description: 角色配置模块测试用例
"""
import logging, pytest

from config import *
from common import readcase
from common import runcase
from common import handleallure

class TestRole:
    """
    角色配置模块
    """

    # 新增角色
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/role/role_add.yaml').items()])
    def test_role_add(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 管理员角色列表
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/role/role_list.yaml').items()])
    def test_role_list(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 角色详情查看
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/role/role_detail.yaml').items()])
    def test_role_detail(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 角色待选菜单列表
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/role/role_menu_list.yaml').items()])
    def test_role_menu_list(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 角色修改
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/role/role_update.yaml').items()])
    def test_role_update(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # # 角色删除
    # @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
    #                                               readcase.ReadCase().get_case_dict(
    #                                                   ROOT_DIR + 'bms/data/role/role_delete.yaml').items()])
    # def test_role_delete(self, caseid, casedata):
    #     handleallure.allure_display(casedata)
    #     logging.info("==========开始执行用例：%s==========", caseid)
    #     runcase.excute_case(casedata)