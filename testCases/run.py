#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pytest
from common.dir_config import allure_result_dir

if __name__ == "__main__":
    # pytest.main(["-s", "-v", "app_demo_reader.py"])
    pytest.main(["-s",
                 "-v",
                 "test_personal.py",
                 "--alluredir="+allure_result_dir,
                 "--clean-alluredir"])


'''
allure报告转换：
-->allure generate ./outputs/allure_results/ -c -o ./outputs/allure_report/
'''