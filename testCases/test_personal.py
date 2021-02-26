#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pageObjects.personal_page import PersonalPage

class TestPersonal:
    def test_personal_1_goto_personal_tab(self, driver):
        pp = PersonalPage(driver)
        pp.goto_personal_tab()
        # assert pp.get_element()