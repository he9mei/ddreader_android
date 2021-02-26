#!/usr/bin/python3
# -*- coding: utf-8 -*-

from appium.webdriver.common.mobileby import MobileBy


class PersonalPageLocator:
    # 我的tab
    loc_personal_tab = (MobileBy.XPATH, "//*[contains(@text,'我的')]")
    