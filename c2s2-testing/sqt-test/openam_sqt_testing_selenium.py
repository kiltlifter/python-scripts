#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestOpenAM(unittest.TestCase):
    def setUp(self, hostname):
        self.driver = webdriver.Chrome()
        self.base_url = "https://my.c2s2.local/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_openam(self, amadmin_pass="password"):
        driver = self.driver
        driver.set_window_size(1800,900)
        driver.get(self.base_url + "openam")
        driver.find_element_by_link_text("OK").click()
        driver.find_element_by_name("IDToken1").clear()
        driver.find_element_by_name("IDToken1").send_keys("amadmin")
        driver.find_element_by_name("IDToken2").clear()
        driver.find_element_by_name("IDToken2").send_keys(amadmin_pass)
        driver.find_element_by_name("Login.Submit").click()
        time.sleep(2)
        driver.find_element_by_name("Home.mhCommon.LogOutHREF").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()