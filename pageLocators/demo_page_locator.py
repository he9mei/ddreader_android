'''
#!/usr/bin/python3
# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class LoginPageLocator:
    # 账号输入框
    loc_input_user = (By.NAME, "phone")
    # 密码输入框
    loc_input_pwd = (By.NAME, "password")
    # 登录按钮
    loc_bn_login = (By.XPATH, "//button[text()='登录']")
    # 账号、密码为空时的错误提示，相同类型的提示都用这一个定位就可以了
    loc_errorMsg = (By.XPATH, '//div[@class="form-error-info"]')
    # 账号密码错误时，给出了toast提示
    # 定位toast方式：toast弹出之后，调试页面从element切换到source,然后点击pause on debugger停止
    # 然后再切换到到element，查看元素定位值
    loc_toast = (By.XPATH, '//div[@class="layui-layer-content"]')


'''