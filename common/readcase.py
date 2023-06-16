# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: readcase.py
@IDE: PyCharm
@time: 2023-06-04 18:07
@description: 处理用例数据
"""
import collections, logging

from config import *
from common import basefunc
from common import handleyaml
from common import handledict

all_case = collections.OrderedDict()

class ReadCase:
    """
    获取用例数据
    """

    def read_all_case(self, path_list):
        """
        获取当前目录下所有测试用例
        :param path_list: 路径列表
        :return: 用例数据{'casepath': 'E:/Wondersoft_ApiTest/bms/data/roles/roles_add.yaml', 'epic': '系统管理', 'feature': '权限管理-角色配置', 'story': '角色新增接口'}
        """
        global all_case
        # 获取yaml文件路径
        files_paths_list = []
        for path in path_list:
            # 获取当前路径下所有yaml文件
            files_paths_list += basefunc.file_execute_list(path, '.yaml')

        # 遍历读取yaml文件
        for file_path in files_paths_list:
            file_data = handleyaml.YamlHandle(file_path).read_yaml()

            case_data = file_data.pop('case')
            # 获取用例
            for caseid in case_data.keys():
                all_case[caseid] = handledict.dict_update({"casepath": file_path}, file_data)
                all_case[caseid]['title'] = case_data[caseid]['name']
        return all_case


    def get_case_data(self, caseid, casepath):
        """
        获取用例数据
        :param caseid: 用例id
        :param casepath: 用例路径
        :return: 用例信息
        """
        yaml_data = handleyaml.YamlHandle(casepath).read_yaml()

        casedata = yaml_data['case'][caseid]

        return casedata


    def get_case_dict(self, casepath):
        """
        获取用例数据
        :param casepath: 用例路径
        :return: case_dict   {caseid: casedata}
        """
        yaml_data = handleyaml.YamlHandle(casepath).read_yaml()

        if isinstance(yaml_data, list):
            case_dict = collections.OrderedDict()
            for api in yaml_data:
                case_info = api.pop('case_info')  # 接口基本信息
                case_data = api.pop('case_data')  # 用例信息
                case_info = handledict.dict_update(api, case_info)
                if isinstance(case_data, dict):
                    for caseid, casedata in case_data.items():
                        casedata = handledict.dict_update(casedata, case_info)   #用例基础信息与用例数据合并
                        casedata['caseid'] = caseid   #在用例信息中添加用例id
                        case_dict[caseid] = casedata
                else:
                    raise Exception(api['story'] + '用例case_data模块编写有误，非字典格式！')
            return case_dict
        else:
            raise Exception(casepath + 'yaml文件编写有误，非列表格式！')


    def read_case(self, path_list):
        """
        获取当前目录下所有测试用例
        :param path_list: 路径列表
        :return: 用例数据{'caseid':'casepath': 'E:/Wondersoft_ApiTest/bms/data/roles/roles_add.yaml'}
        """
        global all_case
        # 获取yaml文件路径
        files_paths_list = []
        for path in path_list:
            # 获取当前路径下所有yaml文件
            files_paths_list += basefunc.file_execute_list(path, '.yaml')

        # 遍历读取yaml文件
        for file_path in files_paths_list:
            file_data = handleyaml.YamlHandle(file_path).read_yaml()
            if isinstance(file_data, list):
                for api in file_data:
                    case_data = api.pop('case_data')  # 用例信息
                    if isinstance(case_data, dict):
                        for caseid in case_data.keys():
                            all_case[caseid] = file_path
                    else:
                        raise Exception(api['story'] + '用例case_data模块编写有误，非字典格式！')
            else:
                raise Exception(file_path + 'yaml文件编写有误，非列表格式！')
        return all_case
