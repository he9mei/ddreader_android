#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pageObjects.personal_page import PersonalPage

# log相关导入
from common.logger import Log
from pathlib import Path

# logger = Logger().logger(Path(__file__).name) #创建logger的方法从logger()改写到init方法
log = Log(Path(__file__).name)
logger = log.get_logger()

class TestPersonal:
    def test_personal_1_goto_personal_tab(self, driver):
        logger.info("---测试用例---")
        pp = PersonalPage(driver)
        pp.goto_personal_tab()
        # assert pp.get_element()