'''

#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 登录用例

from time import sleep
import pytest
from web.web_po.web_po_v5.PageObjects.login_page_2 import LoginPage
from web.web_po.web_po_v5.PageObjects.index_page import IndexPage
from web.web_po.web_po_v5.TestDatas import login_datas as ld


@pytest.mark.demo
@pytest.mark.usefixtures("access_web")  # 使用了access_web函数的前置和后置
# 这是fixture的第1种用法；第2种用法是把conftest.py的函数直接当做参数传入
# 目前因为需要返回值，所以需要第2种方式传值，只用第1种方式是不能接收返回值的。此时第1种方式可以写也可以不写。
@pytest.mark.usefixtures("refresh")
# refresh作用域是function，可以在class前装饰，也可以在测试用例前装饰。
# 在class前装饰，表示该class下的所有测试用例都需要使用refresh后置
class TestLogin:
    # 将fixture写在测试用例中
    @pytest.fixture(scope="function")
    def demo(self):
        print("==login独有前置==")

    @pytest.mark.usefixtures("demo")
    def test_login_1_noPWD(self,access_web, my_session):  # 密码为空
        # 前置条件：打开浏览器，进入登录页面
        # 步骤：登录页面-输入账号,不输入密码，点击登录
        # 断言：登录页面-错误信息:请输入密码
        # 测试数据：18684720553/空
        LoginPage(access_web).login(user="18684720553", pwd="")
        assert LoginPage(access_web).get_error_msg() == "请输入密码"
        # 账号名为空，""/"python" "请输入手机号"；
        # 账号格式错误，10位"1850000000"或者12位"185000000000"/"python" "请输入正确的手机号"；
        print("my_session的值是{}".format(my_session))

    # 对第1个测试用例进行改造，实现同类型数据的参数化===重要实例
    # @ddt.data(*ld.wrong_data_1)
    @pytest.mark.parametrize("data", ld.wrong_data_1)   # 这里直接把ld文件中的数据拿过来赋值给data，之后的使用与ddt一样
    def test_login_1_wrongData(self, data, access_web):
        # 密码为空
        # 前置条件：打开浏览器，进入登录页面
        # 步骤：登录页面-输入账号,不输入密码，点击登录
        # 断言：登录页面-错误信息:请输入密码
        # 测试数据：18684720553/空
        # 步骤相同，其他场景：
        # 账号名为空，""/"python" "请输入手机号"；
        # 账号格式错误，10位"1850000000"或者12位"185000000000"/"python" "请输入正确的手机号"；
        LoginPage(access_web).login(data["user"], data["pwd"])
        assert LoginPage(access_web).get_error_msg() == data["check"]

    def test_login_2_wrongPWD(self, access_web):  # 密码错误
        # 前置条件：打开浏览器，进入登录页面
        # 步骤：登录页面-输入账号,输入错误密码，点击登录
        # 断言：登录页面-错误信息:帐号或密码错误!
        # 测试数据：18684720553/111111
        LoginPage(access_web).login(user="18684720553", pwd="111111")
        assert LoginPage(access_web).get_error_toast() == "帐号或密码错误!"
        # 账号未注册，"18500000000"/"python" "此账号没有经过授权，请联系管理员!"

    def test_login_3_success(self, access_web):  # 这里去掉了实例化赋值self.login_page = LoginPage(access_web)
        # 前置条件：打开浏览器，进入登录页面
        # 步骤：登录页面-输入账号密码，点击登录
        # 断言：首页-登录账号信息存在
        # 测试数据：18684720553/python
        LoginPage(access_web).login(user="18684720553", pwd="python")
        assert IndexPage(access_web).check_user_ele_exists()  # 老师写法的断言 # 修改断言为assert+表达式的形式





# ===之前版本的记录
# 问题：为什么这里不用setUpClass和tearDownClass?
# ui自动化测试用例编写原则（稳定性优先级最高）：
# 1.保持用例的独立性！无论其他用例成功与否，不影响我的运行。
# 比如我的前一个用例在中间某个页面报错，如果使用同一个浏览器，下一个用例就可能找不到页面或元素。
#
# 自己的理解：
# 以上至少对于WEB自动化是合理的，
# 如果对于APP的话，我自己做的是使用一个driver，但是每次用例执行完毕后无论是否成功都会回到主tab。
# 然后每个用例的开始也是从主tab。这样可以避免，用例失败，导致下一个用例找不到页面和元素的问题。

'''
