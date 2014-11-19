#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class ConfigureOpenamSelenium2(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://my.c2s2.local"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_configure_openam_selenium2(self):
        driver = self.driver
        driver.get(self.base_url + "/openam")
        driver.find_element_by_link_text("OK").click()
        time.sleep(3)
        driver.find_element_by_id("CreateNewConf").click()
        time.sleep(1)
        driver.find_element_by_id("adminPassword").clear()
        driver.find_element_by_id("adminPassword").send_keys("password")
        driver.find_element_by_id("adminConfirm").clear()
        driver.find_element_by_id("adminConfirm").send_keys("password")
        # Wait for the next key to show up and spam with enter and click
        time.sleep(1)
        driver.find_element_by_id("nextTabButton").send_keys("Keys.RETURN")
        driver.find_element_by_id("nextTabButton").send_keys("Keys.RETURN")
        driver.find_element_by_id("nextTabButton").click()

        driver.find_element_by_id("cookieDomain").clear()
        driver.find_element_by_id("cookieDomain").send_keys(".c2s2.local")
        driver.find_element_by_id("serverURL").clear()
        driver.find_element_by_id("serverURL").send_keys("http://my.c2s2.local:8080")
        time.sleep(1)
        driver.find_element_by_id("nextTabButton").click()
        driver.find_element_by_id("nextTabButton").click()
        driver.find_element_by_id("userStoreHost").clear()
        driver.find_element_by_id("userStoreHost").send_keys("localhost")
        driver.find_element_by_id("ldapv3opends").click()
        driver.find_element_by_id("userStoreRootSuffix").clear()
        driver.find_element_by_id("userStoreRootSuffix").send_keys("dc=opensso,dc=my,dc=c2s2,dc=local")
        driver.find_element_by_id("userStoreLoginId").click()
        driver.find_element_by_id("userStoreLoginId").clear()
        driver.find_element_by_id("userStoreLoginId").send_keys("cn=amadmin,ou=people,dc=opensso,dc=my,dc=c2s2,dc=local")
        driver.find_element_by_id("userStorePassword").clear()
        driver.find_element_by_id("userStorePassword").send_keys("password")
        # Wait for the next tab button to apper then spam next with enter and click
        time.sleep(1)
        driver.find_element_by_id("nextTabButton").send_keys("Keys.RETURN")
        driver.find_element_by_id("nextTabButton").send_keys("Keys.RETURN")
        driver.find_element_by_id("nextTabButton").click()
        
        driver.find_element_by_id("nextTabButton").click()
        driver.find_element_by_id("agentPassword").clear()
        driver.implicitly_wait(1)
        driver.find_element_by_id("agentPassword").send_keys("password1")
        driver.find_element_by_id("agentConfirm").clear()
        driver.implicitly_wait(1)
        driver.find_element_by_id("agentConfirm").send_keys("password1")
        # Wait for the next tab button to apper then spam next with enter and click
        driver.find_element_by_id("wizardFooter")
        time.sleep(1)
        driver.find_element_by_id("nextTabButton").send_keys("Keys.RETURN")
        driver.find_element_by_id("nextTabButton").click()
        time.sleep(1)
        driver.find_element_by_id("wizardFooter")
        driver.find_element_by_id("writeConfigButton").click()
        driver.find_element_by_id("confComplete")
        time.sleep(5)
        driver.find_element_by_link_text("Proceed to Login").click()
    
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
