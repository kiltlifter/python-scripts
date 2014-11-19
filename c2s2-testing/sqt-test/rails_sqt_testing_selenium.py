#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, sys


class RailsSeleniumTest(unittest.TestCase):
    def setUp(self, hostname="my.c2s2.local"):
        self.driver = webdriver.Chrome()
        self.base_url = "http://"+hostname+"/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_rails(self):
        driver = self.driver
        driver.set_window_size(1800,900)
        driver.get(self.base_url + "rails")
        driver.find_element_by_link_text("OK").click()
        time.sleep(5)

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()