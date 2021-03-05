# -*- coding: utf-8 -*-
# 验证conftest.py中yaml数据的读取是否正确

from time import sleep
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def test_demo(driver):
    driver.find_element_by_xpath("//*[contains(@text,'我的')]").click()
    sleep(2)
    # driver.find_element_by_xpath("//*[contains(@text,'任务')]").click()  # flutter,用text能找到
    # driver.find_element_by_xpath("//*[contains(@text,'资产')]").click()
    driver.find_element_by_xpath("//*[contains(@text,'悦读')]").click()
    loc_reading = (MobileBy.ID,'com.dangdang.reader:id/book_iv')
    WebDriverWait(driver,10).until(EC.visibility_of_element_located(loc_reading))
    driver.find_element(*loc_reading).click()
    driver.press_keycode(4)

