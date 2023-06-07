# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_cases.py
@IDE: PyCharm
@time: 2023-06-04 18:53
@description: 执行用例
"""
import logging, copy

import pytest, allure

from config import *
from common import readcase
from common import runcase

all_case = copy.deepcopy(readcase.ReadCase().read_all_case([ROOT_DIR + 'bms/data']))

# all_case = copy.deepcopy(readcase.ReadCase().read_all_case([ROOT_DIR + 'bms/data/login',
#                                                             ROOT_DIR + 'bms/data/role/role_add.yaml']))

all_case.pop('login_01')

@pytest.mark.parametrize('caseid', all_case.keys())
def test_cases(caseid):
    case_info = readcase.all_case[caseid]
    case_data = readcase.ReadCase().get_case_data(caseid, case_info['casepath'])

    allure.dynamic.epic(case_info['epic'])
    allure.dynamic.feature(case_info['feature'])
    allure.dynamic.story(case_info['story'])
    allure.dynamic.title(case_info['title'])
    logging.info("==========开始执行用例：%s==========", caseid)
    runcase.excute_case(case_data)
