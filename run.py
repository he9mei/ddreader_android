# coding=UTF-8

import pytest
from common.dir_config import allure_result_dir

rerun = "2"
case_path = "./testCases/test_personal.py"

if __name__ == "__main__":
    # pytest.main(["-s", "-v"])
    pytest.main(["-s","-v",
                 case_path,
                 "--alluredir="+allure_result_dir,
                 "--clean-alluredir",
                 "--lf",
                 "--reruns",rerun])


'''
allure报告转换：
-->allure generate ./outputs/allure_results/ -c -o ./outputs/allure_report/
'''

'''
执行方法：
1.点击执行按钮，直接执行run.py文件
2.terminal执行：
(1)使用pytest命令执行测试用例文件
-->python3.8 -m pytest ./testCases/test_personal.py
（问题1: 直接使用pytest报错命令找不到）
（问题2：直接用python执行会报错没有pytest模块：可能是因为默认使用的python2.7版本)

（2）使用python命令执行run.py文件
-->python3.8 run.py
（问题1："--reruns",2这样写时还是会报错 TypeError: 'int' object is not subscriptable）
（---重跑次数不能是int，应该是string类型）
（问题2："--reruns","2"这样写时还是会报错 unrecognized arguments: --reruns 2）
 （可能是因为失败重跑的插件没有安装，重新安装一下）
--> pip3 install -U pytest-rerunfailures --trusted-host pypi.org --trusted-host files.pythonhosted.org
安装成功！重新执行成功！

'''