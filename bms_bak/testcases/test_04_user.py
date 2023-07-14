# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_04_user.py
@IDE: PyCharm
@time: 2023-06-16 11:19
@description: 用户与机构管理模块测试用例
"""
import logging, pytest

from config import *
from common import readcase
from common import runcase
from common import handleallure

class TestUser:
    """
    用户与机构管理模块
    """

    # 地域列表查询
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/user/user_area_list.yaml').items()])
    def test_user_area_list(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 新增用户组
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/user/user_group_add.yaml').items()])
    def test_user_group_add(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 用户组列表搜索
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/user/user_group_list.yaml').items()])
    def test_user_group_list(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 修改用户组
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/user/user_group_update.yaml').items()])
    def test_user_group_update(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 根据用户组ID精确查询用户组
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/user/user_group_searchbyid.yaml').items()])
    def test_user_group_searchbyid(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 用户组列表查看
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/user/user_group_list_view.yaml').items()])
    def test_user_group_list_view(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 新增用户
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/user/user_add.yaml').items()])
    def test_user_add(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 用户列表搜索
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/user/user_list.yaml').items()])
    def test_user_list(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 用户信息导出
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/user/user_export.yaml').items()])
    def test_user_export(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 根据用户ID精确查询用户
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/user/user_searchbyid.yaml').items()])
    def test_user_searchbyid(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 修改用户
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/user/user_update.yaml').items()])
    def test_user_update(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 普通用户重置密码
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/user/user_passwd_reset.yaml').items()])
    def test_user_passwd_reset(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # # 删除用户
    # @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
    #                                               readcase.ReadCase().get_case_dict(
    #                                                   ROOT_DIR + 'bms/data/user/user_delete.yaml').items()])
    # def test_user_delete(self, caseid, casedata):
    #     handleallure.allure_display(casedata)
    #     logging.info("==========开始执行用例：%s==========", caseid)
    #     runcase.excute_case(casedata)

    # # 删除用户组
    # @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
    #                                               readcase.ReadCase().get_case_dict(
    #                                                   ROOT_DIR + 'bms/data/user/user_group_delete.yaml').items()])
    # def test_user_group_delete(self, caseid, casedata):
    #     handleallure.allure_display(casedata)
    #     logging.info("==========开始执行用例：%s==========", caseid)
    #     runcase.excute_case(casedata)