# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: handleyaml.py
@IDE: PyCharm
@time: 2023-06-02 16:00
@description: yaml文件处理
"""
import yaml, logging, sys, traceback

from common import exceptions
from common import handledict

class YamlHandle:
    "yaml文件处理"

    def __init__(self, path, data=None):
        self.path = path    #yaml文件绝对路径
        self.data = data    #数据文件

    def read_yaml(self):
        """
        读取yaml文件
        :return: yaml数据
        """
        yaml_data = ""
        try:
            with open(self.path, 'r', encoding='utf-8') as file_obj:
                yaml_data = yaml.load(file_obj, Loader=yaml.SafeLoader)
        except:
            #异常处理
            ex_type, ex_val, ex_stack = sys.exc_info()
            error_info = exceptions.get_error_info(ex_type, ex_val, ex_stack)
            logging.error("读取yaml文件【%s】异常：%s", self.path, error_info)
            raise
        return yaml_data

    def write_yaml(self):
        """
        写入yaml文件
        :return:
        """
        with open(self.path, 'w', encoding='utf-8') as file_obj:
            yaml.dump(data=self.data, stream=file_obj, allow_unicode=True)

    def updata_yaml(self):
        """
        更新yaml文件
        :return:
        """
        yaml_data = self.read_yaml()    #读取yaml文件
        self.data = handledict.dict_update(yaml_data, self.data)   #获取更新后的数据
        self.write_yaml()

    def clear_yaml(self):
        """
        清空yaml文件
        :return:
        """
        with open(self.path, 'w', encoding='utf-8') as file_obj:
            file_obj.truncate()

    # def get_yaml_value(self):
    #     """
    #     获取yaml文件中的指定值
    #     :return:
    #     """
    #     yaml_data = self.read_yaml()
    #     expect_value_list = self.data.split(',')
    #     if isinstance(yaml_data, dict):
    #         for i in expect_value_list:
    #             yaml_data = yaml_data[i]
    #     return yaml_data


def standard_yaml(casedata):
    """
    判断测试用例格式是否有误
    :param casedata: 用例数据
    :return:
    """
    flag = True
    try:
        casedata_key = casedata.keys()
        # 判断一级关键字是否包含有：name, base_url, request, validate
        if "name" in casedata_key and "base_url" in casedata_key and "request" in casedata_key and "expect" in casedata_key:
            # 判断request下是否包含有： method，url，headers
            request_key = casedata['request'].keys()
            if "method" in request_key and "url" in request_key and "headers" in request_key:
                logging.info("Yaml测试用例基础架构检查通过")
            else:
                flag = False
                logging.error("用例编写有误，request下必须包含：method，url，headers")
        else:
            flag = False
            logging.error("用例编写有误，一级关键字必须包含：name，base_url，request，expect")
    except:
        ex_type, ex_val, ex_stack = sys.exc_info()
        error_info = exceptions.get_error_info(ex_type, ex_val, ex_stack)
        logging.error("规范Yaml测试用例异常：%s", error_info)
        flag = False
    return flag

