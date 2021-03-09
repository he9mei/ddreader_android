#!/usr/bin/python3
# -*- coding: utf-8 -*-
import allure
import pytest
from appium import webdriver
import yaml
from time import sleep
from common.dir_config import caps_dir
import os
import time
from common.dir_config import fail_capture_dir, outputs_dir

app_driver = None


@pytest.fixture(scope="session", autouse=True)
def driver():
    # 打开yaml文件
    fs = open(f"{caps_dir}/desired_caps.yaml")
    # 加载成python对象
    desired_caps = yaml.load(fs, yaml.FullLoader)
    fs.close()

    driver = webdriver.Remote("http://0.0.0.0:4723/wd/hub", desired_caps)
    driver.implicitly_wait(10)

    global app_driver
    app_driver = driver
    # return app_driver


@pytest.fixture(scope="session", autouse=True)
def driver_end():
    yield driver
    sleep(5)
    driver.quit()


# 失败监听+失败截图
# 参考：
# https://blog.csdn.net/ezreal_tao/article/details/100148446
# https://www.cnblogs.com/xiaogongjin/p/11705914.html
# https://blog.csdn.net/weixin_30915275/article/details/94862440
# https://blog.csdn.net/liyacai_20120512/article/details/102797042


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    '''
    hook pytest失败
    :param item:
    :param call:
    :return:
    '''
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:

        path = outputs_dir # 我自己添加的failures文件的路径,默认放在主路径
        if not os.path.exists(path):
            os.makedirs(path)

        mode = "a" if os.path.exists(f"{path}/failures") else "w"
        with open(f"{path}/failures", mode) as f:
            # let's also access a fixture for the fun of it
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(rep.nodeid + extra + "\n")

        # 调取失败截图方法
        fail_capture()  # 方式1：调用失败截图并加入allure的方法

        # 方式2：直接使用以下方式也可以，直接把失败截图添加到allure（但是图片不会保存到本地）
        # with allure.step('添加失败截图'):
        #     allure.attach(app_driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)


# 失败截图方法---与basepage中的save_page方法一样，只是文件名和图片名有改动，且没有logger
def fail_capture():
    # now = time.strftime("%Y-%m-%d_%H_%M_%S",time.localtime(time.time()))  #图片文件名加上日期和时间
    dt = time.strftime("%Y-%m-%d",time.localtime(time.time()))
    tm = time.strftime("%H-%M-%S",time.localtime(time.time()))  #由于文件夹是以日期命名的，文件名省去日期
    path = f"{fail_capture_dir}/{dt}"
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        # filename=path+"/"+"fail_"+tm+".png"
        filename=f"{path}/fail_capture_{tm}.png"
        # print(f"失败截图方法中的driver是:{app_driver}")  # 确认此处的driver就是setup的driver
        # driver.get_screenshot_as_file(filename)  # 调用driver的截图方法
        # 此处如何获得driver?
        app_driver.get_screenshot_as_file(filename)   #还是不行, 这个之后再研究，ddreader_appium中可用

        # 把失败截图放到allure中
        with allure.step("添加失败截图"):
            with open(filename, mode="rb") as f:
                file = f.read()
            allure.attach(file, "fail_capture_{tm}", allure.attachment_type.PNG)
            # 此处图片名字待改进，否则多张图时，不好区分

    except Exception as e:
        print(e)


'''
# 截图、获取toast
# 注意点：
# 1、给定截图的名称为中文，则需添加u，如：get_screenShot(u"个人主页")，否则截图保存的文件名称乱；---貌似不写也没问题
# 2、若给定的截图名称为英文，则不需添加U
def save_png(self, doc="", name="", wait=1):    # 普通截图和失败截图都用这个截图方法
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
        self.logger.exception(f"截图失败:{doc}_{name}")
    else:
        self.logger.info(f"截图成功！保存为:{filename}")

        try:
            # 如果需要加入报告，可以添加到allure-可以加，也可以不加
            with allure.step("添加截图"):
                with open(filename, mode="rb") as f:
                    file = f.read()
                allure.attach(file, f"screenshot_{doc}_{name}_{tm}", allure.attachment_type.PNG)
        except:
            self.logger.exception("allure添加截图失败！")

'''