# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: handleallure.py
@IDE: PyCharm
@time: 2023-06-14 15:54
@description:
"""
import allure

def allure_display(casedata):
    """
    处理allure显示
    :param casedata: 用例信息
    :return:
    """
    allure.dynamic.epic(casedata['epic'])
    allure.dynamic.feature(casedata['feature'])
    allure.dynamic.story(casedata['story'])
    allure.dynamic.title(casedata['name'])
    allure.dynamic.description(casedata['description'])