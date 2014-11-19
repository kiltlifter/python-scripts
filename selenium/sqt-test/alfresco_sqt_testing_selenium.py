#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, os

class TestAlfresco(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = "https://my.c2s2.local/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_alfresco(self):

        driver = self.driver
        driver.set_window_size(1800,900)
        driver.get(self.base_url + "alfresco/")
        time.sleep(1)
        driver.find_element_by_link_text("OK").click()
        time.sleep(3)
        driver.find_element_by_link_text("Login (guest)").click()
        Select(driver.find_element_by_id("loginForm:language")).select_by_visible_text("English")
        driver.find_element_by_id("loginForm:user-name").clear()
        driver.find_element_by_id("loginForm:user-name").send_keys("admin")
        driver.find_element_by_id("loginForm:user-password").clear()
        driver.find_element_by_id("loginForm:user-password").send_keys("C2S2-SAE-default!")
        driver.find_element_by_id("loginForm:submit").click()
        time.sleep(1)
        driver.find_element_by_link_text("Add content to your home space").click()
        time.sleep(1)
        driver.find_element_by_id("dialog:dialog-body:file-input").send_keys("/home/sdouglas/documents/C2S2-SAE-1.0.0.1.2-Build-Plan_additional_artifacts.xls")
        # Breaks with firefox
        driver.find_element_by_id("dialog:finish-button").click()
        driver.find_element_by_id("dialog:finish-button").click()
        # Uncomment in production
        driver.find_element_by_link_text("C2S2-SAE-1.0.0.1.2-Build-Plan_additional_artifacts.xls").click()
        # ^^^ Open the file later to make sure the download has completed

        # Show details of item
        driver.find_element_by_xpath("(//table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/span/a/img[@title='View Details'])[last()]").click()
        driver.find_element_by_link_text("Run Action").click()
        Select(driver.find_element_by_xpath("//select[@name='wizard:wizard-body:action']")).select_by_visible_text("Transform and copy content ")
        driver.find_element_by_id("wizard:wizard-body:set-add-button").click()
        Select(driver.find_element_by_xpath("//select[@name]")).select_by_visible_text("Adobe PDF Document")
        driver.find_element_by_link_text("Click here to select the destination").click()
        time.sleep(1)
        driver.find_element_by_xpath("//div[@id='spaceSelector-selector']/div/div/div/span/a/img[@class='pickerActionButton']").click()
        driver.find_element_by_id("transform-action:finish-button").click()
        driver.find_element_by_id("wizard:finish-button").click()
        driver.find_element_by_link_text("My Home").click()

        # Now we'll open the file
        os.popen("gnome-open /home/sdouglas/downloads/C2S2-SAE-1.0.0.1.2-Build-Plan_additional_artifacts.xls")
        # Go to the alfresco share portal
        driver.get("http://my.c2s2.local/share/")
        time.sleep(1)
        driver.find_element_by_xpath("//input[@name='username']").clear()
        driver.find_element_by_xpath("//input[@name='username']").send_keys("admin")
        time.sleep(1)
        driver.find_element_by_xpath("//input[@name='password']").clear()
        driver.find_element_by_xpath("//input[@name='password']").send_keys("C2S2-SAE-default!")
        driver.find_element_by_xpath("//button[@type='button']").click()

        # Once inside the share portal...
        driver.find_element_by_id("HEADER_MY_FILES_text").click()
        time.sleep(4)
        driver.find_element_by_link_text("C2S2-SAE-1.0.0.1.2-Build-Plan_additional_artifacts.xls").click()
        time.sleep(8)
        driver.find_element_by_xpath("//a[@title='Delete Document']").click()
        driver.find_element_by_xpath("//span[@class='button-group']/span[1]/span/button").click()
        time.sleep(4)
        driver.find_element_by_link_text("C2S2-SAE-1.0.0.1.2-Build-Plan_additional_artifacts.pdf").click()
        time.sleep(8)
        driver.find_element_by_xpath("//a[@title='Delete Document']").click()
        driver.find_element_by_xpath("//span[@class='button-group']/span[1]/span/button").click()
    
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
