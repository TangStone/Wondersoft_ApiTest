# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: checkresult.py
@IDE: PyCharm
@time: 2023-06-04 21:31
@description: 结果校验
"""
import allure, logging, jsonpath

from common import handledict


def check_result(hope_res, real_res, real_code):
    """
    返回结果校验
    :param hope_res: 期望结果
    :param real_res: 实际结果
    :param real_code: 返回状态码
    :return:
    """
    with allure.step("结果校验"):
        for key, value in hope_res.items():
            if key == 'code':
                assert_code(value, real_code)
            elif key == 'jsonpath':
                assert_text(value,real_res)
            elif key == 'response':
                assert_response(value, real_res)

def assert_response(hope_res, real_res):
    """
    返回结果校验 -全返回校验
    :param hope_res: 
    :param real_res: 
    :return: 
    """
    if isinstance(hope_res, dict) and isinstance(real_res, dict):
        try:
            with allure.step("返回值校验"):
                allure.attach(name="期望返回值", body=str(hope_res))
                allure.attach(name='实际返回值', body=str(real_res))
                flag = handledict.cmp_dict(hope_res, real_res)
                assert flag
                logging.info("返回结果断言通过, 期望返回值:%s, 实际返回值:%s", hope_res, real_res)
        except AssertionError:
            logging.error("返回结果断言未通过, 期望返回值:%s, 实际返回值:%s", hope_res, real_res)
            raise

def assert_text(hope_res, real_res):
    """
    返回结果校验 -jsonpath
    :param hope_res: 期望返回结果
    :param real_res: 实际返回结果
    :return:
    """
    if isinstance(hope_res, list):
        for h_res in hope_res:
            if jsonpath.jsonpath(real_res, h_res['path']):
                r_res = jsonpath.jsonpath(real_res, h_res['path'])[0]
                if h_res['asserttype'] == '==':
                    try:
                        with allure.step("json断言判断相等"):
                            allure.attach(name="期望结果", body=str(h_res))
                            allure.attach(name='实际实际结果', body=str(r_res))
                            assert str(h_res["value"]) == str(r_res)
                            logging.info("json断言通过, 期望结果'{0}', 实际结果'{1}'".format(h_res, r_res))
                    except AssertionError:
                        logging.error("json断言未通过, 期望结果'{0}', 实际结果'{1}'".format(h_res, r_res))
                        raise
                elif h_res["asserttype"] == "!=":
                    try:
                        with allure.step("json断言判断不等"):
                            allure.attach(name="json期望结果", body=str(h_res))
                            allure.attach(name='json实际实际结果', body=str(r_res))
                            assert str(h_res["value"]) != str(r_res)
                            logging.info("json断言通过, 期望结果'{0}', 实际结果'{1}'".format(h_res, r_res))
                    except AssertionError:
                        logging.error("json断言未通过, 期望结果'{0}', 实际结果'{1}'".format(h_res, r_res))
                        raise
                elif h_res["asserttype"] == "in":
                    r_res = str(r_res)
                    try:
                        with allure.step("json断言判断包含"):
                            allure.attach(name="期望结果", body=str(h_res))
                            allure.attach(name='实际实际结果', body=str(r_res))
                            assert str(h_res["value"]) in str(r_res)
                            logging.info("json断言通过, 期望结果'{0}', 实际结果'{1}'".format(h_res, real_res))
                    except AssertionError:
                        logging.error("json断言未通过, 期望结果'{0}', 实际结果'{1}'".format(h_res, real_res))
                        raise
                else:
                    raise TypeError("asserttype方法错误")
            else:
                logging.error("获取json值失败，请检查jsonpath")
                raise ValueError('获取json值失败，请检查jsonpath')

def assert_code(hope_code, real_code):
    """
    返回状态码校验
    :param hope_res: 期望返回状态码
    :param real_res: 实际返回状态码
    :return:
    """
    try:
        with allure.step("状态码校验"):
            allure.attach(name="期望状态码", body=str(hope_code))
            allure.attach(name='实际状态码', body=str(real_code))
            assert real_code == hope_code
            logging.info("code断言通过, 期望状态码:%s, 实际状态码:%s", hope_code, real_code)
    except AssertionError:
        logging.error("code断言未通过, 期望状态码:%s, 实际状态码:%s", hope_code, real_code)
        raise