# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: basefunc.py
@IDE: PyCharm
@time: 2023-06-02 17:36
@description: 基础处理函数
"""
import os
from config import *
from common import logger
from common import handleyaml
from common import readcase

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

def file_execute_list(rootpath, filetype):
    """
    获取当前目录下所有的文件
    :param rootpath: 文件夹路/文件路径
    :param filetype: 文件类型
    :return: 文件绝对路径列表
    """
    # 获取当前路径下所有文件
    file_path_list = []

    if os.path.isdir(rootpath):   #文件夹
        for root, dirs, files in os.walk(rootpath):
            if files:
                for file in files:
                    if filetype in file:
                        file_path_list.append(root + '/' + file)
    else:
        if filetype in rootpath:
            file_path_list.append(rootpath)

    return file_path_list


def pre_process():
    """
    执行用例前置处理操作
    :return:
    """
    # 开启日志记录(默认logs目录)
    logger.MyLogs().setup_logging(ROOT_DIR)

    # 清空临时文件目录
    clean_dir(ROOT_DIR + 'report/tmp')
    # 清空报告
    clean_dir(ROOT_DIR + 'report/report')
    # 清空中间件文件
    handleyaml.YamlHandle(EXTRACT_DIR).clear_yaml()
    # 获取用例数据
    config_dict = handleyaml.YamlHandle(CONFIG_DIR).read_yaml()
    casedata_path = config_dict['casedata_path']
    readcase.ReadCase().read_case([ROOT_DIR + casedata_path])

def post_process():
    """
    执行用例后置处理操作
    :return:
    """
    # 添加environment.properties到allure目录
    config_dict = handleyaml.YamlHandle(CONFIG_DIR).read_yaml()
    # project_name = config_dict['project_name']
    baseurl = config_dict['host']
    environment = 'BaseURL=' + baseurl + '\n'
    with open(ROOT_DIR + 'report/tmp/environment.properties', 'w', encoding='ascii', errors='ignore') as file_obj:
        file_obj.write(environment)
