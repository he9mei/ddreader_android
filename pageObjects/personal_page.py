#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pageLocators.personal_page_locator import PersonalPageLocator as loc
from common.basepage import BasePage


class PersonalPage(BasePage):
    def click_personal_tab(self):
        self.click(loc.loc_personal_tab, doc="app_点击我的")

    def click_home_page(self):
        self.click(loc.loc_home_page, doc="我的_点击主页")

    def click_reading(self):
        self.click(loc.loc_reading, doc="主页_点击最近在读的数据")
