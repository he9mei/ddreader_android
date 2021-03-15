import click
import pytest
import time
import os


case_path = "./test_case/test_01_login.py"
rerun = "1"  # 这里需要写出str格式，如果直接写成数字1，后面使用时需要str(rerun)


@click.command()   # 需要先安装click插件，并导入click
@click.option("-m", default=None, help="输入运行模式：run 或者 debug")
def run(m):
    if m is None or m == "run":
        print("回归模式，执行用例完成后，生成测试报告！")
        now_time = time.strftime("%Y-%m-%d_%H-%M-%S")
        # init_evn(now_time) 不太明白，初始化环境？不用这个也可以
        html_report=os.path.join("./test_result/report/html_report",now_time,"report.html")
        # xml_report=os.path.join("./test_result/report/xml_report",now_time,"junit-xml.xml")
        # allure_results=os.path.join("./test_result/report/allure_results",now_time)
        allure_results = os.path.join("./test_result/report/allure_results")
        # pytest.main(["-s","-v","--alluredir=./test_result/report/allure_results","--clean-alluredir"])
        pytest.main(["-s", "-v", case_path,
                     # "--html=./test_result/report/html_report/report.html",  # html报告会自动覆盖,不加时间也可以
                     "--html="+html_report,
                     # "--junit-xml="+xml_report,
                     "--alluredir="+allure_results,
                     "--clean-alluredir",
                     "--self-contained-html",
                     "--reruns", rerun])  # "--reruns"+rerun 这种写法错误 reruns 和 rerun要当成2个命令写
    elif m == "debug":
        print("debug模式执行用例！")
        pytest.main(["-s","-v",case_path])


if __name__ == "__main__":
    run()

# 该py文件直接运行是不可以的，只能在终端运行
# -->python run_test.py --help
# -->python run_test.py -m debug
# -->python run_test.py -m run
# -->python run_test.py  默认是run模式

# allure报告暂时不用时间了，因为generate的时候，如果带有时间会麻烦点
# allure generate ./test_result/report/allure_results/2020-07-15_19-50-18 -c -o  ./test_result/report/allure_report
# allure generate ./test_result/report/allure_results -c -o  ./test_result/report/allure_report