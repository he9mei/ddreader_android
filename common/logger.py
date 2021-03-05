#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import time
import os.path
from common.dir_config import log_dir


class Log:
    # 也可以把获得logger的方法写在init方法中，实例化时就会调用
    def __init__(self,py_name="test.py"):  #def logger改写到init方法中，不改写也是可以的。
        '''
        class_name="Test"
        func_name="test"
        class_name和func_name获取稍微麻烦点，换成直接使用py_name
        '''
        py_name_str = py_name.split(".py")[0]  # 拿到py_name再以".py"分隔，取前面的字符串（不切割也能正常生成log）

        # now=time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime(time.time()))  # 可以用这个，也可以分开日期和时间
        dt=time.strftime("%Y-%m-%d",time.localtime(time.time()))  #用时间做一层文件夹，下一层只显示时间
        tm = time.strftime("%H-%M-%S", time.localtime(time.time()))
        # path=f"./test_result/log/{dt}/{tm}"   # 这个路径做成可配置，如下（在dir_config.py中配置）
        path = f"{log_dir}/{dt}/{tm}"
        # 可以不用具体到日期和时间，这里是为了区分每次跑用例的log分开,并且发现同批次跑的用例log文件夹的时间是都是一样的。
        # 因此，我这里用时间区分文件夹，然后在具体的log文件名去掉了时间显示。
        # path = "./log/" + class_name + "_" + now #一个class的log文件放入一个文件夹
        # filepath=os.path.dirname(os.getcwd())+"/log"  #python_appium/learning_log/log
        if not os.path.exists(path):  #如果文件路径不存在，需要先创建
            os.makedirs(path)

        #创建日志器
        # self.logger = logging.getLogger("logger")
        # 每个py文件实例化时，用py_name来获取不同名字的logger；这样每次实例化都会生成新的logger。
        # 问题：使用相同的logger，判断是否有handles的情况，应该也是可以的，
        # 但是第一次remove后，第二次实例化时，并不会生成新的handles？
        self.logger=logging.getLogger(py_name_str)
        self.logger.setLevel(logging.DEBUG)

        #判断是否已经存在处理器
        if not self.logger.handlers:
            #创建处理器
            print("不存在handles")
            self.sh=logging.StreamHandler()
            # sh=logging.StreamHandler(sys.stdout, )
            # self.fh=logging.FileHandler(filename="{}/{}_{}.log".format(path, py_name_str, tm), mode="a", encoding="utf-8")  #py_name换掉func_name
            self.fh = logging.FileHandler(filename="{}/{}.log".format(path, py_name_str),
                                          mode="a",
                                          encoding="utf-8")
            #注意：此处需要加上encoding="utf-8"，否则Windows上生成的log文件显示问号，打不开。

            #创建个格式器
            # self.fh_error=logging.FileHandler(filename="{}/{}_error_{}.log".format(path, py_name_str, now), mode="a", encoding="utf-8")
            self.fh_error = logging.FileHandler(filename="{}/{}_error.log".format(path, py_name_str),
                                                mode="a",
                                                encoding="utf-8")

            formatter = logging.Formatter(fmt="%(asctime)s-[%(filename)s-%(funcName)s]-%(levelname)s-[line:%(lineno)d]-%(message)s",
                                          datefmt="%Y/%m/%d/%X")

            self.sh.setFormatter(formatter)
            self.fh.setFormatter(formatter)
            self.fh_error.setFormatter(formatter)

            # sh.setLevel(logging.DEBUG)
            # fh.setLevel(logging.INFO)
            self.fh_error.setLevel(logging.ERROR)

            self.logger.addHandler(self.sh)
            self.logger.addHandler(self.fh)
            self.logger.addHandler(self.fh_error)

    def get_logger(self):  # 此处如果函数名为logger会与前面的变量名重复，会报错object is not callable
        return self.logger

    # 该方法暂时没有使用，
    # 会产生多个logger日志器和handles处理器，不移除不确定会不会影响性能？
    def remove_handler(self):
        # self.fh.close()
        self.logger.removeHandler(self.fh)
        self.logger.removeHandler(self.sh)

'''
# 我这里用到的python日志2种方式：
# 1.封装获得logger的方法，用的时候实例化，调用方法获得logger；（可以传参数）
# 2.用log.conf配置文件，文件的解析写在conftest.py中了，加上fixture装饰器，使用时直接当成参数传入。
（fixture的方式，目前不知道怎么传入参数）
还有一种py文件内的BasicConfig配置方式，用的比较少。
'''

# 目前的log还存在一个问题，如果文件没有写入任何内容，文件也会存在。
# 比如整个class都是跳过，但是该py文件的log文件还是会生成，是空的；
# 再比如error文件也可能是空的。
# 如果没有任何内容可以，删除这些文件吗？否则需要手动点击查看。
# 或者先根据测试报告查看失败的用例，再去查看error.log



