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
    print("---启动driver---")

    global app_driver   # app_driver是为了给以下的失败截图使用，如果不写失败截图，这里则不需要写
    app_driver = driver

    yield driver
    sleep(5)
    driver.quit()
    print("---test end---")


# 失败监听
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

        fail_capture()  # 方式1：调用失败截图并加入allure的方法

        # 方式2：直接使用以下方式也可以，直接把失败截图添加到allure（但是图片不会保存到本地）
        # with allure.step('添加失败截图'):
        #     allure.attach(app_driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)


# 失败截图方法
# 与basepage中的save_page方法一样，只是文件名和图片名有改动，且没有加logger
def fail_capture():
    # now = time.strftime("%Y-%m-%d_%H_%M_%S",time.localtime(time.time()))  #图片文件名加上日期和时间
    dt = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    tm = time.strftime("%H-%M-%S", time.localtime(time.time()))  #由于文件夹是以日期命名的，文件名省去日期
    path = f"{fail_capture_dir}/{dt}"
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        filename = f"{path}/fail_capture_{tm}.png"

        app_driver.get_screenshot_as_file(filename)  # 调用driver自带截图方法

        # 把失败截图放到allure中
        with allure.step("添加失败截图"):
            with open(filename, mode="rb") as f:
                file = f.read()
            allure.attach(file, "fail_capture_{tm}", allure.attachment_type.PNG)

    except Exception as e:
        print(e)
