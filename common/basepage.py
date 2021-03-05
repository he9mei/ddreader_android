#!/usr/bin/python3
# -*- coding: utf-8 -*-
import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import MobileBy
import logging
import time
import os

from common.dir_config import screenshot_dir

# log相关导入
# from common.logger import Log
# from pathlib import Path
# Log实例化时传入当前py文件名
# log = Log(Path(__file__).name)
# logger = log.get_logger()
# 优化：basepage的logger从测试用例py文件中，做页面实例化时传入，利于相应的调用log放在测试用例的py文件log下
# 否则所有调用basepage的方法的log都会放在basepage.log下

# 目标：任务一个步骤都能实现-异常捕获、日志输出、失败截图
class BasePage:   # 页面对象类需要继承BasePage
    def __init__(self, driver: WebDriver, logger):
        self.driver = driver
        self.logger = logger

    # 等待元素可见/出现
    def wait_eleVisible(self, loc, timeout=10, frequncy=0.5, doc=""):
        start = time.time()
        try:
            WebDriverWait(self.driver, timeout, frequncy).until(EC.visibility_of_element_located(loc))
        except:
            self.logger.error("等待元素{}出现，超时！".format(loc))   # 关于日志---之前在接口测试讲过了，这里只是简单输出
            # self.sava_png(doc="等待元素超时")  # 这里doc也可以继续从外层传入
            self.save_png(doc)
            raise   # 异常抛出---这里是一定要抛出的，因为这里捕获后自己处理了，如果不抛出，就不会报错，代码会继续执行。
        else:
            end = time.time()
            duration = end - start  # 这里需要再转化为s，未写完整
            self.logger.info("等待元素{}出现，等待时间为{}秒。".format(loc, duration))

    # 等待元素存在
    def wait_elePresence(self, loc, timeout=10, frequncy=0.5, doc=""):
        start = time.time()
        try:
            WebDriverWait(self.driver, timeout, frequncy).until(EC.presence_of_element_located(loc))
        except:
            logging.error("等待元素{}存在，超时！".format(loc))
            self.save_png(doc)
            raise
        else:
            end = time.time()
            duration = end - start  # 这里需要再转化为s，未写完整
            logging.info("等待元素{}存在，等待时间为{}秒。".format(loc, duration))

    # 截图、获取toast
    # 注意点：
    # 1、给定截图的名称为中文，则需添加u，如：get_screenShot(u"个人主页")，否则截图保存的文件名称乱；---貌似不写也没问题
    # 2、若给定的截图名称为英文，则不需添加U
    def save_png(self, doc="", name="", wait=1):
        dt = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        # tm=time.strftime("%Y-%m-%d_%H_%M_%S",time.localtime(time.time()))  #图片文件名加上日期和时间
        tm = time.strftime("%H-%M-%S", time.localtime(time.time()))  # 由于文件夹是以日期命名的，文件名省去日期
        # path = f"./test_result/screenshot/{dt}"  # 文件位置替换为可配置的screenshot_dir
        path = f"{screenshot_dir}/{dt}"

        if not os.path.exists(path):   # 判断文件是否存在，可以单独写在一个函数中
            os.makedirs(path)
        filename = f"{path}/{doc}_{name}_{tm}.png"

        try:
            time.sleep(wait)
            self.driver.get_screenshot_as_file(filename)  # driver的截图方法
        except:
            self.logger.error(f"截图失败:{doc}_{name}")
        else:
            self.logger.info(f"截图成功！保存为:{filename}")

            try:
                # 如果需要加入报告，可以添加到allure-可以加，也可以不加
                with allure.step("添加截图"):
                    with open(filename, mode="rb") as f:
                        file = f.read()
                    allure.attach(file, f"screenshot_{doc}_{name}_{tm}", allure.attachment_type.PNG)
            except:
                self.logger.error("allure添加截图失败！")


    # 查找元素
    def get_element(self, loc, doc=""):
        try:
            ele = self.driver.find_element(*loc)
        except:
            self.logger.error("查找[{}]相关元素{}失败！".format(doc, loc))
            self.save_png(doc)
            raise
        else:
            self.logger.info("查找元素{}成功！".format(loc)) # 也可以通过doc具体到哪个页面的哪个元素
            return ele

    # 输入文本
    def input_text(self, loc, text, timeout=10, frequncy=0.5, doc=""):
        # 前提1：元素可见
        # 前提2：找到它
        self.wait_eleVisible(loc, timeout, frequncy, doc)
        ele = self.get_element(loc, doc)
        try:
            ele.send_keys(text)
        except:
            logging.error("向元素{}输入:'{}'失败！".format(loc, text))
            self.save_png(doc)
            raise
        else:
            logging.info("向元素{}输入:'{}'成功！".format(loc, text))

    # 点击元素
    def click(self, loc, timeout=10, frequncy=0.5, doc=""):
        self.wait_eleVisible(loc, timeout, frequncy, doc)
        ele = self.get_element(loc, doc)
        try:
            ele.click()
        except:
            self.logger.error("点击元素{}失败！".format(loc))
            self.save_png(doc)
            raise
        else:
            self.logger.info("点击元素{}成功！".format(loc))

    # 获取元素文本
    def get_element_text(self, loc, timeout=10, frequncy=0.5, doc=""):
        # 前提1：元素存在（不一定可见，建议这里改成存在-再写一个等待存在的方法；如果没有元素隐藏的情况，两种都可以）
        # 前提2：找到它
        self.wait_eleVisible(loc, timeout, frequncy, doc)
        # self.wait_elePresence(loc, timeout, frequncy, doc)
        ele = self.get_element(loc, doc)
        try:
            text = ele.text
        except:
            logging.error("获取元素{}文本失败！".format(loc))
            self.save_png(doc)
            raise
        else:
            logging.info("获取元素{}文本成功！".format(loc))
            return text

    # 获取元素属性
    def get_element_attr(self):
        pass

    # 不一定要把所有方法封装，可以需要的时候再封装；
    # 之后学习robotframework的时候，这块已经封装好了,可以再借鉴一下。

    # 切换window  #new #main #index
    def switch_to_window(self, index):
        # 获取一次窗口列表、触发新窗口、获取所有窗口、再切换 （前2个步骤可以在函数之前实现，然后再调用函数）
        if index  == "new":  # 代表切换到新窗口
            pass
        elif index == "main":  # 代表切换到第一个窗口
            pass
        else:
            pass




# 以上copy自web_po_v5
# 以下再补充APP端操作
    def get_screen_size(self):
        '''
        获取屏幕大小
        :return:
        '''
        try:
            size=self.driver.get_window_size()
        except:
            pass
        else:
            return size

    def swipe_screen(self, derection):
        '''
        左滑、右滑、上滑、下滑
        :return:
        '''
        size=self.get_screen_size()
        if derection.lower == "up":
            pass
        if derection.lower == "down":
            pass
        if derection.lower == "left":
            pass
        if derection.lower == "right":
            pass

    def get_toast_msg(self, str):
        '''
        获取toast文本
        :param str:
        :return:
        '''
        xpath = '//*[contains(@text,{})]'.format(str)
        loc = (MobileBy.XPATH, xpath)
        try:
            WebDriverWait(self.driver,10,0.1).until(EC.presence_of_element_located(loc))
            toast = self.driver.find_element(*loc).text
        except:
            pass
        else:
            logging.info("找到toast，文本是：{}".format(toast))
            return toast

    def swipe_to_element(self, loc):
        '''
        滑动列表一直到找到某个元素
        :param loc:
        :return:
        '''
        pass

# common层不需要做别的改动，主要就是新增app端的一些方法封装

