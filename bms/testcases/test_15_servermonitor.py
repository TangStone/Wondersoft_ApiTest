# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_15_servermonitor.py
@IDE: PyCharm
@time: 2023-06-21 17:49
@description: 系统管理-运维管理-服务监控模块测试用例
"""
import logging, pytest

from config import *
from common import readcase
from common import runcase
from common import handleallure

class TestServerMonitor:
    """
    服务监控模块
    """

    # 查询服务器列表
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/servermonitor/servermonitor_serverlist.yaml').items()])
    def test_servermonitor_serverlist(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 查询集群列表
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/servermonitor/servermonitor_endponitlist.yaml').items()])
    def test_servermonitor_endponitlist(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)