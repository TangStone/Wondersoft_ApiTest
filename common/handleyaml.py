#coding=utf-8

"""
@author:  gaojie
@File：handleyaml.py
@IDE: PyCharm
@time: 2023-04-04 14:26
@description: yaml文件处理
"""
import logging, os
import yaml

def read_yaml_data(filepath):
    """
    读取yaml文件
    :param filepath: yaml文件
    :return:
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        yaml_data = yaml.load(f, Loader=yaml.SafeLoader)
    return yaml_data

def write_yaml_data(filepath, data):
    """
    写入yaml文件
    :param filepath: yaml文件
    :param data: 写入对象
    :return:
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data=data, stream=f, allow_unicode=True)

def get_yaml_value(filepath, expect_str):
    """
    获取yaml文件中的指定值
    :param filepath: yaml文件路径
    :param expect_str: 期望值字符串，‘bms_env,host'
    :return:
    """
    yaml_data = read_yaml_data(filepath)
    expect_value_list = expect_str.split(',')
    if isinstance(yaml_data, dict):
        for i in expect_value_list:
            yaml_data = yaml_data[i]
    return yaml_data

def update_yaml_value(filepath, obj):
    """
    更新yaml值
    :param filepath: yaml文件路径
    :param obj: 写入对象{"token": token}
    :return:
    """
    print(filepath)
    print(obj)
    yaml_data = read_yaml_data(filepath)   #读取yaml文件

    yaml_data = dict_update(yaml_data, obj) #修改yaml文件
    write_yaml_data(filepath, yaml_data)  #写入yaml文件


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


def clear_yaml_data(filepath):
    """
    清空yaml文件
    :param filepath:
    :return:
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        f.truncate()


def read_case(path):
    """
    获取测试用例数据
    :param path:
    :return:
    """
    all_case_data = {}
    # 获取yaml文件路径
    file_path_list = file_execute_list(path)

    #遍历读取yaml文件
    for file_path in file_path_list:
        file_data = read_yaml_data(file_path)

        #获取用例数据
        case_dict = file_data.pop('case')
        for caseid, casedata in case_dict.items():
            new_casedata = {**casedata, **file_data}
            all_case_data[caseid] = new_casedata

    return all_case_data

def file_execute_list(path):
    """
    获取当前目录下所有的测试用例文件路径
    :param path: 文件夹路/文件路径
    :return:
    """
    # 获取当前路径下所有文件
    file_path_list = []

    if os.path.isdir(path):   #文件夹
        for root, dirs, files in os.walk(path):
            if files:
                for file in files:
                    if '.yaml' in file:
                        file_path_list.append(root + '/' + file)
    else:
        file_path_list.append(path)

    return file_path_list
