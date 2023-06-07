# -*- coding: utf-8 -*-

"""
@author:  gaojie
@File：exceptions.py
@IDE: PyCharm
@time: 2023-05-29 14:31
@description:
"""
import traceback

def get_error_info(ex_type, ex_val, ex_stack):
    error_info = str(ex_type) + '\n' + str(ex_val) + '\n'
    for stack in traceback.extract_tb(ex_stack):
        error_info += str(stack)
    return error_info
