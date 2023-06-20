# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_12_dlpSeverityLevel.py
@IDE: PyCharm
@time: 2023-06-20 14:32
@description: 严重性等级管理模块测试用例
"""
import logging, pytest

from config import *
from common import readcase
from common import runcase
from common import handleallure

class TestDlpSeverityLevel:
    """
    严重性等级管理模块
    """

    # 严重性等级新增
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/dlpSeverityLevel/dlpSeverityLevel_add.yaml').items()])
    def test_dlpSeverityLevel_add(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 严重性等级列表查询
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/dlpSeverityLevel/dlpSeverityLevel_list.yaml').items()])
    def test_dlpSeverityLevel_list(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 严重性等级修改
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/dlpSeverityLevel/dlpSeverityLevel_update.yaml').items()])
    def test_dlpSeverityLevel_update(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 严重性等级删除
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/dlpSeverityLevel/dlpSeverityLevel_delete.yaml').items()])
    def test_dlpSeverityLevel_delete(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)