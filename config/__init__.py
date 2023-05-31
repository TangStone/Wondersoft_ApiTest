#coding=utf-8

"""
@author:  gaojie
@File：__init__.py.py
@IDE: PyCharm
@time: 2023-04-03 14:45
@description:
"""

import os

# 获取主目录路径
ROOT_DIR = os.path.realpath(__file__).split('config')[0].replace('\\', '/')

# 获取配置文件路径
CONFIG_DIR = ROOT_DIR + 'config/config.yml'

# 中间件参数传递文件路径
EXTRACT_DIR = ROOT_DIR + 'bms/extract.yaml'
