# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: test_cases.py
@IDE: PyCharm
@time: 2023-06-04 18:53
@description: 执行用例
"""
import logging, pytest

from config import *
from common import readcase
from common import runcase
from common import handleallure
from common import handleyaml
# from common.basefunc import file_execute_list
from common.basefunc import config_dict

# 基础用例模块用例路径列表
# basecase_pathlist = file_execute_list([CASE_DIR + '/base'], 'yaml')
# # 业务用例模块用例路径列表
# exclude_file = [CASE_DIR + '/extract.yaml', CASE_DIR + '/base']
# businesscase_pathlist = file_execute_list([[CASE_DIR + '/' + i for i in config_dict['casedata_path']] if config_dict['casedata_path'] else CASE_DIR], 'yaml', exclude_file)


class TestCases:
    """
    用例执行
    """
    # # 执行基础初始化用例集
    # @pytest.mark.parametrize('case, casedata', readcase.ReadCase().get_case(basecase_pathlist))
    # def test_basecases(self, case, casedata):
    #     handleallure.allure_display(casedata)
    #     logging.info("==========执行用例START：%s==========", case)
    #     runcase.RunCase().excute_case(casedata)
    #     logging.info("==========执行用例END：%s==========", case)
    #
    # # 执行业务用例集
    # @pytest.mark.parametrize('case, casedata', readcase.ReadCase().get_case(businesscase_pathlist))
    # def test_businesscases(self, case, casedata):
    #     handleallure.allure_display(casedata)
    #     logging.info("==========执行用例START：%s==========", case)
    #     runcase.RunCase().excute_case(casedata)
    #     logging.info("==========执行用例END：%s==========", case)

    # # 执行基础初始化用例集
    # # @pytest.mark.parametrize('case, casedata', readcase.ReadCase().get_case(basecase_pathlist))
    # @pytest.mark.parametrize('case, casedata', readcase.ReadCase().get_cases([[CASE_DIR + '/' + i for i in config_dict['casedata_path']] if config_dict['casedata_path'] else CASE_DIR], 'yaml', exclude_file))
    # def test_basecases(self, case, casedata):
    #     logging.info("==========执行用例case：%s==========", case)
    #     logging.info("用例casedata：%s", casedata)

    # 执行基础初始化用例集
    @pytest.mark.parametrize('case, casedata', readcase.ReadCase().get_cases([CASE_DIR + '/base'], 'yaml'))
    def test_basecases(self, case, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========执行用例START：%s==========", case)
        runcase.RunCase().excute_case(casedata)
        logging.info("==========执行用例END：%s==========", case)

    # 执行业务用例集
    @pytest.mark.parametrize('case, casedata', readcase.ReadCase().get_cases([[CASE_DIR + '/' + i for i in config_dict['casedata_path']] if config_dict['casedata_path'] else CASE_DIR], 'yaml', [CASE_DIR + '/extract.yaml', CASE_DIR + '/base']))
    def test_businesscases(self, case, casedata):
        handleallure.allure_display(casedata)
        logging.info("==========执行用例START：%s==========", case)
        runcase.RunCase().excute_case(casedata)
        logging.info("==========执行用例END：%s==========", case)


