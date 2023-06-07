# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: handledict.py
@IDE: PyCharm
@time: 2023-06-04 18:00
@description: 字典处理
"""
def dict_update(old_dict, update_dict):
    """
    字典更新
    :param old_dict: 原始字典
    :param update_dict: 更新字典
    :return: 更新后的字典
    """
    if old_dict:   #非空字典
        if isinstance(old_dict, dict) and isinstance(update_dict, dict):
            for key, value in update_dict.items():
                if isinstance(value, dict) and key in old_dict.keys():
                        old_value = old_dict[key]
                        old_dict[key] = dict_update(old_value, value)
                else:
                    old_dict[key] = value
    else:
        old_dict = update_dict
    return old_dict
