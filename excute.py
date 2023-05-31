#coding=utf-8

"""
@author:  gaojie
@File：excute.py
@IDE: PyCharm
@time: 2023-03-29 14:35
@description：
"""
import pytest, time
from requests.packages import urllib3
urllib3.disable_warnings()
from common import logger
from config import *


if __name__ == '__main__':

    # 开启日志记录(默认logs目录)
    logger.MyLogs().setup_logging(ROOT_DIR)

    # pytest.main(['-vs', '--alluredir', './report/tmp'])
    pytest.main()

    times = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    # 将report/tmp目录下的结果文件生成html类型的测试报告文件到report/report目录下
    # -o report/report --clean 清空已有的测试报告再生成
    os.system("allure generate ./report/tmp -o ./report/report/report_" + times + " --clean")
