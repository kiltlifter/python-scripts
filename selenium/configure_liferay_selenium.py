#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class ConfigureLiferaySelenium(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://my.c2s2.local/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_configure_liferay_selenium(self):
        driver = self.driver
        driver.get(self.base_url + "liferay/")
        driver.find_element_by_link_text("OK").click()
        ## Section for initial liferay config
        driver.find_element_by_id("finishButton").click()
        time.sleep(8)
        driver.find_element_by_xpath("//input[@type='submit']").click()
        time.sleep(5)
        driver.find_element_by_xpath("//input[@value='I Agree']").click()
        driver.find_element_by_id("password1").clear()
        driver.find_element_by_id("password1").send_keys("test")
        driver.find_element_by_id("password2").clear()
        driver.find_element_by_id("password2").send_keys("test")
        driver.find_element_by_xpath("//input[@value='Save']").click()
        Select(driver.find_element_by_id("reminderQueryQuestion")).select_by_visible_text("Write my own question.")
        driver.find_element_by_id("reminderQueryCustomQuestion").clear()
        driver.find_element_by_id("reminderQueryCustomQuestion").send_keys("test")
        driver.find_element_by_id("reminderQueryAnswer").clear()
        driver.find_element_by_id("reminderQueryAnswer").send_keys("test")
        driver.find_element_by_xpath("//input[@value='Save']").click()
        time.sleep(1)
        ### Use if the above section has already been run
        #driver.find_element_by_id("_58_login").clear()
        #driver.find_element_by_id("_58_login").send_keys("test@liferay.com")
        #driver.find_element_by_id("_58_password").clear()
        #driver.find_element_by_id("_58_password").send_keys("test")
        #driver.find_element_by_xpath("//input[@value='Sign In']").click()

        driver.find_element_by_xpath("//div[@class='portlet-body']/div/ul[2]/li/a").send_keys(Keys.RETURN)
        driver.find_element_by_xpath("//div[@class='portlet-body']/div/ul[2]/li/a").click()
        driver.find_element_by_xpath("//ul[@class='taglib-my-sites']/li[1]/a").click()
        driver.find_element_by_id("_160_portlet_130").click()
        driver.find_element_by_id("_130_virtualHostname").clear()
        driver.find_element_by_id("_130_virtualHostname").send_keys("my.c2s2.local")
        driver.find_element_by_xpath("//input[@value='Save']").click()
        time.sleep(2)
        driver.find_element_by_link_text("Sign Out").click()
    
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
