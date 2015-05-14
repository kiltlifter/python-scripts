#!/usr/bin/python
__author__ = 'sdouglas'


import alfresco_sqt_testing_selenium
import geoserver_sqt_testing_selenium
import liferay_sqt_testing_selenium
import openam_sqt_testing_selenium
import owf_sqt_testing_selenium
import rails_sqt_testing_selenium
from subprocess import Popen
import getpass
import optparse


def alfresco_test(hostname, document):
    alfresco = alfresco_sqt_testing_selenium.TestAlfresco('setUp')
    try:
        alfresco.setUp(hostname=hostname)
        alfresco.test_alfresco(hostname=hostname, document=document)
        alfresco.tearDown()
        return "[+] Alfresco: Success"
    except Exception, e:
        return "[-] Alfresco: Failure\n\n" + str(e) + "\n\n"


def geoserver_test(hostname):
    geoserver = geoserver_sqt_testing_selenium.TestGeoserver('setUp')
    try:
        geoserver.setUp(hostname=hostname)
        geoserver.test_geoserver()
        geoserver.tearDown()
        return "[+] Geoserver: Success"
    except Exception, e:
        return "[-] Geoserver: Failure\n\n" + str(e) + "\n\n"


def liferay_test(hostname):
    liferay = liferay_sqt_testing_selenium.TestLiferay('setUp')
    try:
        liferay.setUp(hostname=hostname)
        liferay.test_liferay()
        liferay.tearDown()
        return "[+] Liferay: Success"
    except Exception, e:
        return "[-] Liferay: Failure\n\n" + str(e) + "\n\n"


def openam_test(hostname, amadmin_password):
    openam = openam_sqt_testing_selenium.TestOpenAM('setUp')
    try:
        openam.setUp(hostname=hostname)
        openam.test_openam(amadmin_pass=amadmin_password)
        openam.tearDown()
        return "[+] OpenAM: Success"
    except Exception, e:
        return "[-] OpenAM: Failure\n\n" + str(e) + "\n\n"


def owf_test(hostname):
    owf = owf_sqt_testing_selenium.TestOWF('setUp')
    try:
        owf.setUp(hostname=hostname)
        owf.test_owf()
        owf.tearDown()
        return "[+] Ozone Widget Framework: Success"
    except Exception, e:
        return "[-] Ozone Widget Framework: Failure\n\n" + str(e) + "\n\n"


def rails_test(hostname, devel_pass):
    rails = rails_sqt_testing_selenium.RailsSeleniumTest('setUp')
    try:
        ssh_connection = "./ssh_connect.sh devel %s %s" % (hostname, devel_pass)
        Popen(ssh_connection, shell=True, stdout=PIPE).stdout.read()
        rails.setUp(hostname=hostname)
        rails.test_rails()
        rails.tearDown()
        return "[+] Rails Sample Application Success"
    except Exception, e:
        return "[-] Rails Sample Application: Failure\n\n" + str(e) + "\n\n"

 
def verify_password(text):
    tmp_pass1 = getpass.getpass(text)
    tmp_pass2 = getpass.getpass("One more time: ")
    if tmp_pass1 == tmp_pass2:
        return tmp_pass1
    else:
        print "Password's don't match."
        exit()


def main():
    parser = optparse.OptionParser("selenium_sqt_controller.py -d <domain> -f <filename>")
    parser.add_option('-d', dest='domain', type='string', help='specify a domain name')
    parser.add_option('-f', dest='fileName', type='string', help='specify a file to use')
    (options, args) = parser.parse_args()
    domain = options.domain
    fileName = options.fileName
    if (domain is None) or (fileName is None):
        print parser.usage
        exit()
    amadmin_password = verify_password("Enter password for amadmin: ")
    devel_pass = verify_password("Enter password for devel: ")
    results = [
        #alfresco_test(domain, fileName),
        #geoserver_test(domain),
        #liferay_test(domain),
        #openam_test(domain, amadmin_password),
        #owf_test(domain),
        rails_test(domain, devel_pass)
    ]
    for result in results:
        print result


if __name__ == "__main__":
    main()
