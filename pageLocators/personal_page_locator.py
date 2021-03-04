#!/usr/bin/python3
# -*- coding: utf-8 -*-

from appium.webdriver.common.mobileby import MobileBy


class PersonalPageLocator:
    # 我的tab
    loc_personal_tab = (MobileBy.XPATH, "//*[contains(@text,'我的')]")
    # 我的tab-点击进入个人中心
    loc_home_page = (MobileBy.XPATH, "//*[contains(@text,'何九妹')]")
    # 我的tab-未登录
    loc_login_enter = (MobileBy.XPATH, "//*[contains(@text,'点击登录/注册')]")

    # 个人中心-最近在读
    loc_reading = (MobileBy.ID,'com.dangdang.reader:id/book_iv')
