#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pytest
from common.dir_config import allure_result_dir

rerun = 0
case_path = "test_personal.py"

if __name__ == "__main__":
    # pytest.main(["-s", "-v"])
    pytest.main(["-s","-v",case_path,"--alluredir="+allure_result_dir])
                 # ,"--clean-alluredir","--reruns",rerun])


'''
allure报告转换：
-->allure generate ./outputs/allure_results/ -c -o ./outputs/allure_report/
'''