#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class BCDTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = "https://brsandbox:8443/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_bcd(self):
        driver = self.driver
        driver.set_window_size(1800,900)
        driver.get(self.base_url + "owf/")
        driver.find_element_by_name("IDToken1").clear()
        driver.find_element_by_name("IDToken1").send_keys("sdouglas")
        driver.find_element_by_name("IDToken2").clear()
        driver.find_element_by_name("IDToken2").send_keys("password")
        driver.find_element_by_name("Login.Submit").click()
        driver.find_element_by_id("accessAlertOKButton").click()
        #driver.find_element_by_id("launchMenuBtn-btnIconEl").click()
        #time.sleep(5)
        #driver.find_element_by_xpath("//img[@src='../BRVT/images/battlerhythm_launchmenu_icon.gif']").click()
        #driver.find_element_by_xpath("(//div[@class='x-box-inner' and @role='presentation']/div/div/div/em/button/span[1])[last()]").click()
        time.sleep(20)
        #driver.find_element_by_xpath("//div[@class='ui-dialog-buttonset']/button[1]/span")
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        time.sleep(3)
        driver.find_element_by_xpath("//div[@class='ui-dialog-buttonset']/button[1]").click()

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
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()