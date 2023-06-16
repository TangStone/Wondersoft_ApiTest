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

def cmp_dict(expect_dict, recv_dict):
    """
    字典比较
    :param expect_dict: 期望字典
    :param recv: 返回值
    :return:
    """
    flag = True
    if set(expect_dict.keys()).issubset(set(recv_dict.keys())):
        for field, data in expect_dict.items():
            if type(data) == dict:   #预期值为字典
                if type(recv_dict[field]) == dict: #返回值也为字典
                    flag = cmp_dict(data, recv_dict[field])  #递归比较
                else:
                    flag = False
                if not flag:
                    break
            elif type(data) == list:  #预期值为列表
                if type(recv_dict[field]) == list: #返回值也为列表
                    for i in data:
                        print("====",i)
                        if type(i) == dict:
                            flag = False
                            for j in recv_dict[field]:
                                flag = cmp_dict(i, j)
                                if flag:   #字典中有一个比较成功就返回
                                    break
                            if not flag:
                                break
                        else:  #非字典格式直接比较
                            # if data != recv_dict[field]:
                            if str(data) != str(recv_dict[field]):  #暂时只进行字符串比较
                                flag = False
                            break
                else:
                    flag = False
                if not flag:
                    break
            else:  #非字典，列表格式直接比较
                # if expect_dict[field] != recv_dict[field]:
                if str(expect_dict[field]) != str(recv_dict[field]):  #暂时只进行字符串比较
                    flag = False
                    break
    else:
        flag = False
    return flag



# rec = {'statusCode': 0, 'msg': 'success', 'data': {'totalCount': 1, 'list': [{'id': 5, 'modifyTime': '2023-06-14 20:37:45', 'type': 'domain', 'name': '70.235', 'configs': '{"name":"70.235","host":"192.168.70.235","port":"389","username":"xiantest\\\\administrator","password":"Ws-123456abc","base":"DC=xiantest,DC=com","org":"ou=北京明朝万达","isEncrypt":false,"userFilter":"","groupFilter":"","isIncrement":false}', 'relations': '{"sourceUUID":"objectGUID","groupLabel":"ou","groupName":"name","userLabel":"cn","userName":"sAMAccountName","userSid":"objectSid"}', 'isRemoved': 0}]}}
# exp = {'statusCode': 0, 'msg': 'success', 'data': {'list': [{'name': '70.235'}]}}
#
# flag = cmp_dict(exp, rec)
#
# print(flag)

