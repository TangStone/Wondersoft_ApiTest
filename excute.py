#coding=utf-8

"""
@author:  gaojie
@File：excute.py
@IDE: PyCharm
@time: 2023-03-29 14:35
@description：
"""
import pytest, time, copy
from requests.packages import urllib3
urllib3.disable_warnings()
from config import *
from common import basefunc

if __name__ == '__main__':

    # 执行用例前置处理操作
    basefunc.pre_process()
    # 执行用例
    pytest.main()
    # 执行用例后置处理操作
    basefunc.post_process()
    # 生成allure报告
    times = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    os.system("allure generate ./report/tmp -o ./report/report/report_" + times + " --clean")
