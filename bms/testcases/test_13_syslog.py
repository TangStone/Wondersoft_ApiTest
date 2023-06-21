# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_13_syslog.py
@IDE: PyCharm
@time: 2023-06-21 9:46
@description: 系统管理-运维管理-管理员审计模块测试用例
"""
import logging, pytest

from config import *
from common import readcase
from common import runcase
from common import handleallure

class TestSysLog:
    """
    管理员审计模块
    """

    # 管理员日志查询条件初始化
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/syslog/syslog_getAllComboBoxData.yaml').items()])
    def test_syslog_getAllComboBoxData(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 管理员日志查询条件
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/syslog/syslog_getQueryParamList.yaml').items()])
    def test_syslog_getQueryParamList(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 管理员日志模块查询
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/syslog/syslog_getModuleByParams.yaml').items()])
    def test_syslog_getModuleByParams(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 管理员日志查看
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/syslog/syslog_list.yaml').items()])
    def test_syslog_list(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)