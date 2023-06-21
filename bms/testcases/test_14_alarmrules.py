# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_14_alarmrules.py
@IDE: PyCharm
@time: 2023-06-21 16:24
@description: 系统管理-运维管理-告警规则模块测试用例
"""
import logging, pytest

from config import *
from common import readcase
from common import runcase
from common import handleallure

class TestAlarmRules:
    """
    告警规则模块
    """

    # 新增告警规则
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/alarmrules/alarmrules_add.yaml').items()])
    def test_alarmrules_add(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 查询监控报警规则
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/alarmrules/alarmrules_list.yaml').items()])
    def test_alarmrules_list(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 修改告警规则
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/alarmrules/alarmrules_update.yaml').items()])
    def test_alarmrules_update(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 状态启停
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/alarmrules/alarmrules_isenable.yaml').items()])
    def test_alarmrules_isenable(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 删除告警规则
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/alarmrules/alarmrules_delete.yaml').items()])
    def test_alarmrules_delete(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)
