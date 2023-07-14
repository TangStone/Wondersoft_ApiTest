# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_allcase.py
@IDE: PyCharm
@time: 2023-07-05 16:23
@description:
"""
import logging, pytest

from config import *
from common import readcase
from common import runcase
from common import handleallure
from common.basefunc import file_execute_list
from common.basefunc import config_dict

# 基础用例模块用例路径列表
basecase_pathlist = file_execute_list(CASE_DIR + 'basecase', 'yaml')
# 业务用例模块用例路径列表
businesscase_pathlist = file_execute_list([CASE_DIR + i for i in config_dict['casedata_path']], 'yaml')

class TestUserSync:
    """
    用户同步模块
    """

    # 执行基础初始化用例集
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/usersync/usersync_config_add.yaml').items()])
    def test_usersync_config_add(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)


    # 执行指定模块用例集
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/usersync/usersync_config_add.yaml').items()])
    def test_usersync_config_add(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)