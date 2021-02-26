#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pageLocators.personal_page_locator import PersonalPageLocator as loc
from common.basepage import BasePage


class PersonalPage(BasePage):
    def goto_personal_tab(self):
        self.click(loc.loc_personal_tab, doc="个人中心_点击我的tab")
