#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestGeoserver(unittest.TestCase):
    def setUp(self, hostname="my.c2s2.local"):
        self.driver = webdriver.Chrome()
        self.base_url = "https://"+hostname+"/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_geoserver(self):
        driver = self.driver
        driver.set_window_size(1800,900)
        driver.get(self.base_url + "geoserver/wms?request=GetCapabilities")
        driver.find_element_by_link_text("OK").click()
        time.sleep(3)
        driver.get(self.base_url + "geoserver/wfs?request=GetCapabilities")
        time.sleep(3)
        driver.get(self.base_url + "geoserver/wcs?request=GetCapabilities")
        time.sleep(3)
        driver.get(self.base_url + "geoserver")
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("C2S2-SAE-default!")
        driver.find_element_by_class_name("button-login").click()
        time.sleep(2)
        driver.find_element_by_class_name("button-logout").click()
    
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