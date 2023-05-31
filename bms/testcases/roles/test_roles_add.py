# -*- coding: utf-8 -*-

"""
@author:  gaojie
@File：test_roles_add.py
@IDE: PyCharm
@time: 2023-05-30 15:45
@description:
"""
import allure, pytest
from config import *
from common import handleyaml
from common import apisend

api_data = handleyaml.read_yaml_data(ROOT_DIR + "bms/data/roles/roles_add.yaml")


@allure.epic(api_data['epic'])
@allure.feature(api_data['feature'])
class TestRoles:

    @allure.story(api_data['story'])
    @pytest.mark.parametrize("casedata", api_data['case'].values())
    def test_roles_list(self,casedata):
        case_send_data, recv_data = apisend.RequestsSend().excute_case(casedata)