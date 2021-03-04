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
    def test_personal_1_tab(self, driver):
        logger.info("----点击我的tab----")
        pp = PersonalPage(driver, logger)
        pp.click_personal_tab()
        # assert pp.get_element()

    def test_personal_2_home(self, driver):
        logger.info("---点击主页----")
        pp = PersonalPage(driver, logger)
        pp.click_personal_tab()
        pp.click_home_page()

    def test_personal_3_fail(self, driver):
        logger.info("---点击最近在读----")
        pp = PersonalPage(driver, logger)
        pp.click_personal_tab()
        # pp.click_home_page()
        pp.click_reading()
