# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_19_sysconfig.py
@IDE: PyCharm
@time: 2023-06-21 18:32
@description: 系统管理-参数管理-系统参数管理模块测试用例
"""
import logging, pytest

from config import *
from common import readcase
from common import runcase
from common import handleallure

class TestSysConfig:
    """
    系统参数管理模块
    """

    # 系统配置查询
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/sysconfig/sysconfig_info.yaml').items()])
    def test_sysconfig_info(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 根据propKey获取对应的propValue
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/sysconfig/sysconfig_getValueByPropKey.yaml').items()])
    def test_sysconfig_getValueByPropKey(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)

    # 系统配置修改
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/sysconfig/sysconfig_update.yaml').items()])
    def test_sysconfig_update(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)
