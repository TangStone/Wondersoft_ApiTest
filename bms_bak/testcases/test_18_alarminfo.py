# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_18_alarminfo.py
@IDE: PyCharm
@time: 2023-06-21 18:00
@description: 系统管理-运维管理-告警信息模块测试用例
"""
import logging, pytest

from config import *
from common import readcase
from common import runcase
from common import handleallure

class TestAlarmInfo:
    """
    告警信息模块
    """

    # 查询告警信息
    @pytest.mark.parametrize('caseid, casedata', [(caseid, casedata) for caseid, casedata in
                                                  readcase.ReadCase().get_case_dict(
                                                      ROOT_DIR + 'bms/data/alarminfo/alarminfo_list.yaml').items()])
    def test_alarminfo_list(self, caseid, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========开始执行用例：%s==========", caseid)
        runcase.excute_case(casedata)