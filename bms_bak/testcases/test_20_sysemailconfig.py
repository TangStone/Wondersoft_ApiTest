# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_20_sysemailconfig.py
@IDE: PyCharm
@time: 2023-06-21 18:12
@description: 系统管理-参数管理-系统邮箱配置模块测试用例
"""
import logging, pytest

from config import *
from common import readcase
from common import runcase
from common import handleallure

class TestSysEmailConfig:
    """
    系统邮箱配置模块
    """

    # 系统邮箱配置查询
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/sysemailconfig/sysemailconfig_info.yaml').items()])
    def test_sysemailconfig_info(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 系统邮箱验证
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/sysemailconfig/sysemailconfig_verify.yaml').items()])
    def test_sysemailconfig_verify(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)