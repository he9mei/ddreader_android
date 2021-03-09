#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pytest
from appium import webdriver
import yaml
from time import sleep
from common.dir_config import caps_dir


@pytest.fixture(scope="session", autouse=True)
def driver():
    # 打开yaml文件
    fs = open(f"{caps_dir}/desired_caps.yaml")
    # 加载成python对象
    desired_caps = yaml.load(fs, yaml.FullLoader)
    fs.close()

    driver = webdriver.Remote("http://0.0.0.0:4723/wd/hub", desired_caps)
    driver.implicitly_wait(10)
    yield driver
    sleep(5)
    driver.quit()