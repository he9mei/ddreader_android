#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pageObjects.personal_page import PersonalPage

# log相关导入
from common.logger import Log
from pathlib import Path
# Log实例化时传入当前py文件名
log = Log(Path(__file__).name)
logger = log.get_logger()


class TestPersonal:
    def test_personal_1_goto_personal_tab(self, driver):
        logger.info("---个人中心-我的tab----")
        pp = PersonalPage(driver, logger)
        pp.goto_personal_tab()
        # assert pp.get_element()
