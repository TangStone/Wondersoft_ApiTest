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

        casedata = yaml_data[caseid]

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

    def get_api_casedata(self, api_path, api, api_caseid):
        """
        获取接口用例
        :param api_path: 接口路径
        :param api: 接口id
        :param api_caseid: 接口用例id
        :return: 接口用例
        """
        # 读取yaml文件
        yaml_data = handleyaml.YamlHandle(api_path).read_yaml()
        if isinstance(yaml_data, dict):
            api_info = yaml_data[api]['ApiInfo']  #接口基本信息
            api_data = yaml_data[api]['ApiData'][api_caseid]  #接口数据
            api_casedata = handledict.dict_update(api_info, api_data)
            return api_casedata
        else:
            raise Exception(api_path + 'yaml文件编写有误，非json格式！')

    def get_apicase_list(self, casedata):
        """
        根据用例信息获取测试步骤中的接口用例列表
        :param casedata: 测试用例数据
        :return:
        """
        api_case_list = []
        step_list = casedata['steps']
        for step in step_list:
            if 'api_path' in step.keys():    #调用接口用例
                api_case_list.append(step)
            elif 'case_path' in step.keys():    #引用其它用例
                case_path = CASE_DIR + step['case_path']
                case_id = step['case']
                case_data = self.get_case_data(case_id, case_path)
                api_case_list += self.get_apicase_list(case_data)
            else:
                raise Exception('用例步骤编写有误！步骤：' + step + '非接口用例或引用其它用例！')
        return api_case_list

    def get_case(self, file_pathlist):
        """
        获取yaml文件中的所有用例
        :param file_pathlist: yaml文件路径列表
        :return:
        """
        logging.info(file_pathlist)
        case_list = []
        if file_pathlist:
            for file_path in file_pathlist:
                file_data = handleyaml.YamlHandle(file_path).read_yaml()
                for case, casedata in file_data.items():
                    case_list.append((case, casedata))
        return case_list
