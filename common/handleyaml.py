# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: handleyaml.py
@IDE: PyCharm
@time: 2023-06-02 16:00
@description: yaml文件处理
"""
import yaml, logging, sys, traceback
from collections import OrderedDict
from common import exceptions
from common import handledict

class YamlHandle:
    """
    yaml文件处理
    """

    def __init__(self, path, data=None):
        self.path = path    #yaml文件绝对路径
        self.data = data    #数据文件

    def read_yaml(self):
        """
        读取yaml文件
        :return: yaml数据
        """
        try:
            with open(self.path, 'r', encoding='utf-8') as file_obj:
                yaml_data = yaml.load(file_obj, Loader=yaml.SafeLoader)
            return yaml_data
        except:
            #异常处理
            ex_type, ex_val, ex_stack = sys.exc_info()
            error_info = exceptions.get_error_info(ex_type, ex_val, ex_stack)
            logging.error("读取yaml文件【%s】异常：%s", self.path, error_info)
            raise

    # def read_yaml(self, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    #     """
    #     读取yaml文件,组成有序字典
    #     :return: yaml数据
    #     """
    #     try:
    #         class OrderedLoader(Loader):
    #             pass
    #
    #         def construct_mapping(loader, node):
    #             loader.flatten_mapping(node)
    #             return object_pairs_hook(loader.construct_pairs(node))
    #
    #         OrderedLoader.add_constructor(
    #             yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    #             construct_mapping)
    #
    #         with open(self.path, 'r', encoding='utf-8') as file_obj:
    #             yaml_data = yaml.load(file_obj, OrderedLoader)
    #         return yaml_data
    #     except:
    #         # 异常处理
    #         ex_type, ex_val, ex_stack = sys.exc_info()
    #         error_info = exceptions.get_error_info(ex_type, ex_val, ex_stack)
    #         logging.error("读取yaml文件【%s】异常：%s", self.path, error_info)
    #         raise


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

def standard_yaml(casedata):
    """
    判断测试用例格式是否有误
    :param casedata: 用例数据
    :return:
    """
    flag = True
    msg = ''
    try:
        casedata_key = casedata.keys()
        # 判断一级关键字是否包含有：name, base_url, request, postProcessors
        if "name" in casedata_key and "base_url" in casedata_key and "request" in casedata_key and "postProcessors" in casedata_key:
            # 判断request下是否包含有： method，address，headers
            request_key = casedata['request'].keys()
            if "method" in request_key and "address" in request_key and "headers" in request_key:
                # 判断postProcessors下是否有：extract
                postProcessors_key = casedata['postProcessors'].keys()
                if "assert" in postProcessors_key:
                    logging.info("Yaml测试用例基础架构检查通过")
                else:
                    flag = False
                    msg = '用例编写有误，postProcessors下必须包含：assert'
                    logging.error("用例编写有误，postProcessors下必须包含：assert")
            else:
                flag = False
                msg = '用例编写有误，request下必须包含：method，address，headers'
                logging.error("用例编写有误，request下必须包含：method，address，headers")
        else:
            flag = False
            msg = '用例编写有误，一级关键字必须包含：name，base_url，request，postProcessors'
            logging.error("用例编写有误，一级关键字必须包含：name，base_url，request，postProcessors")
    except:
        ex_type, ex_val, ex_stack = sys.exc_info()
        error_info = exceptions.get_error_info(ex_type, ex_val, ex_stack)
        flag = False
        msg = '规范Yaml测试用例异常：' + error_info
        logging.error("规范Yaml测试用例异常：%s", error_info)
    return flag, msg

