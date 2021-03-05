#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

base_dir = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
caps_dir = os.path.join(base_dir, "caps")    # C:\Users\lipan\PycharmProjects\python_lemon\app\app_po_v1\conf_data
screenshot_dir = os.path.join(base_dir, "outputs/screenshots")
log_dir = os.path.join(base_dir, "outputs/logs")
allure_result_dir = os.path.join(base_dir, "outputs/allure_result")
allure_report_dir = os.path.join(base_dir, "outputs/allure_report")  # 不确定是否会用到
fail_capture_dir = os.path.join(base_dir, "outputs/fail_capture")
outputs_dir = os.path.join(base_dir, "outputs")
