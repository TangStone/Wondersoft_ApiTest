# -*- coding: utf-8 -*-

"""
@author:  gaojie
@File：basefunc.py
@IDE: PyCharm
@time: 2023-05-30 10:45
@description:
"""
import os, shutil

def clean_dir(path):
    """清空目录下所有文件，保留文件夹"""
    for i in os.listdir(path):
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            clean_dir(c_path)
        else:
            os.remove(c_path)
    for i in os.listdir(path):
        dir_path = os.path.join(path, i)
        if os.listdir(dir_path):
            clean_dir(path)
        else:
            os.rmdir(dir_path)
