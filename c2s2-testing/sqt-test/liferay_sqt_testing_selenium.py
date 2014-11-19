#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class TestLiferay(unittest.TestCase):
    def setUp(self, hostname="my.c2s2.local"):
        self.driver = webdriver.Chrome()
        self.base_url = "https://"+hostname+"/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_liferay(self):
        driver = self.driver
        driver.set_window_size(1800,900)
        driver.get(self.base_url + "liferay")
        driver.find_element_by_link_text("OK").click()
        driver.find_element_by_link_text("Sign In").click()
        driver.find_element_by_id("_58_login").clear()
        driver.find_element_by_id("_58_login").send_keys("test@liferay.com")
        driver.find_element_by_id("_58_password").clear()
        driver.find_element_by_id("_58_password").send_keys("test")
        driver.find_element_by_xpath("//input[@value='Sign In']").click()
        try:
            driver.find_element_by_xpath("//input[@value='I Agree']").click()
        except Exception as e:
            print "Though there might be a warning banner, move along..."
        time.sleep(3)
        driver.find_element_by_xpath("//div[@class='dockbar']/ul/li[2]/a").send_keys(Keys.RETURN)
        driver.find_element_by_xpath("//div[@class='dockbar']/ul/li[2]/a").send_keys(Keys.TAB)
        driver.find_element_by_xpath("//div[@class='dockbar']/ul/li[2]/a").send_keys(Keys.SHIFT + Keys.TAB)
        driver.find_element_by_id("_145_addApplication").click()
        time.sleep(2)
        driver.find_element_by_id("_87_portletCategory5").click()
        time.sleep(2)
        try:
            driver.find_element_by_xpath("//div[@id='_87_portletCategory5']/div/div[2]/p/a").click()
        except:
            print "Finding the add button is finicky"
            driver.find_element_by_xpath("//div[@id='_87_portletCategory5']/div/div[2]/p/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("//div[@id='column-1']/div/div[1]/div/section/header/menu/span[4]/a").click()
        alert_box = driver.switch_to_alert()
        alert_box.accept()
        driver.find_element_by_xpath("(//li[@aria-controls])[last()]/a").click()
        driver.find_element_by_xpath("//div/div/ul[@class='taglib-my-sites']/li[1]/a/span").click()
        time.sleep(1)
        driver.find_element_by_xpath("(//div[@class='lfr-panel-content'])[3]/ul/li[11]/a").click()
        Select(driver.find_element_by_xpath("(//span[@class='aui-field-content'])[2]/span/select")).select_by_visible_text("75")
        time.sleep(1)
        driver.find_element_by_xpath("//div[@id='_132_ocerSearchContainer']/div/table/tbody/tr[28]/td/a").click()
        driver.find_element_by_xpath("//input[@type='checkbox' and @value='true']").click()
        driver.find_element_by_xpath("//input[@value='Save']").click()
    
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
