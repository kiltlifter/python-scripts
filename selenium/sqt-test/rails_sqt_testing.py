#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, sys

key_file = str(sys.argv[1])
class BaseSeleniumScript(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = "http://my.c2s2.local/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_base_selenium_script(self):
        #if sys.argv[1]:
        #    key_file = str(sys.argv[1])
        #else:
        #    self.driver.quit()
        ssh_command = "ssh -i %s root@my.c2s2.local" % key_file
        command_list = []
        command_list.append(ssh_command + " 'rails new /var/lib/rails-app; chown -R apache:apache /var/lib/rails-app'")
        command_list.append("scp -i %s rails.webapp root@my.c2s2.local:/etc/httpd/conf.d/" % key_file)
        command_list.append(ssh_command + " '/etc/init.d/httpd restart'")
        for item in command_list:
            os.popen(item)
            print item
        driver = self.driver
        driver.set_window_size(1800,900)
        driver.get(self.base_url + "rails")
        time.sleep(5)
    
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