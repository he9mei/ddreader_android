'''
#!/usr/bin/python3
# -*- coding: utf-8 -*-

from web.web_po.web_po_v4.PageLocators.login_page_locator import LoginPageLocator as loc
from web.web_po.web_po_v4.Common.basepage import BasePage


class LoginPage(BasePage):
    def login(self, user, pwd):
        self.input_text(loc.loc_input_user, user, doc="登录页_输入用户名")
        self.input_text(loc.loc_input_pwd, pwd, doc="登录页_输入密码")
        self.click(loc.loc_bn_login, doc="登录页_点击登录")

    def get_error_msg(self):
        return self.get_element_text(loc.loc_errorMsg, doc="登录页_获取错误信息的文本")

    def get_error_toast(self):
        return self.get_element_text(loc.loc_toast, frequncy=0.1, doc="登陆页_获取toast文本")

'''