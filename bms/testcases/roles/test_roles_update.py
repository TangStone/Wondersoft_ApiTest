# -*- coding: utf-8 -*-

"""
@author:  gaojie
@File：test_roles_update.py
@IDE: PyCharm
@time: 2023-05-30 16:06
@description:
"""
import allure, pytest
from config import *
from common import handleyaml
from common import apisend

api_data = handleyaml.read_yaml_data(ROOT_DIR + "bms/data/roles/roles_update.yaml")


@allure.epic(api_data['epic'])
@allure.feature(api_data['feature'])
class TestRoles:

    @allure.story(api_data['story'])
    @pytest.mark.parametrize("casedata", api_data['case'].values())
    def test_roles_list(self,casedata):
        # pytest.mark.parametrize(ids=casedata['name'])
        case_send_data, recv_data = apisend.RequestsSend().excute_case(casedata)