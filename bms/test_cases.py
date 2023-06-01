# -*- coding: utf-8 -*-

"""
@author:  gaojie
@File：test_cases.py
@IDE: PyCharm
@time: 2023-06-01 11:45
@description:
"""
import pytest, allure
from config import *
from common import handleyaml
from common import apisend

case_data = handleyaml.read_case(ROOT_DIR + 'bms/data/roles/')

@pytest.mark.parametrize('casedata', case_data.values())
def test_cases(casedata):
    allure.dynamic.epic(casedata['epic'])
    allure.dynamic.feature(casedata['feature'])
    allure.dynamic.story(casedata['story'])
    allure.dynamic.title(casedata['name'])
    apisend.RequestsSend().excute_case(casedata)


