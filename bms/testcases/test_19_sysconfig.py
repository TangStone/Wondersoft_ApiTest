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

    # 系统邮箱配置查询
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/sysconfig/sysconfig_info.yaml').items()])
    def test_sysconfig_info(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)