#!/usr/bin/python
__author__ = 'sdouglas'


import alfresco_sqt_testing_selenium
import geoserver_sqt_testing_selenium
import liferay_sqt_testing_selenium
import openam_sqt_testing_selenium
import owf_sqt_testing_selenium
import rails_sqt_testing_selenium
import getpass
import optparse
import pxssh
import time


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


def rails_test(hostname, password):
    rails_webapp = "Alias /rails /var/lib/rails-app/public\n" \
               "<Directory /var/lib/rails-app/public>\n" \
               "Allow from all\n" \
               "PassengerAppRoot \"/var/lib/rails-app/public\"\n" \
               "</Directory>"
    create_file_command = "echo -e '%s' > /etc/httpd/conf.d/rails.webapp" % rails_webapp
    try:
        s = connect(hostname, "devel", password)
        s.sendline("sudo su")
        s.expect("assword")
        s.prompt()
        s.sendline(password)
        s.prompt()
        s.sendline("rails new /var/lib/rails-app && chown -R apache:apache /var/lib/rails-app")
        s.prompt()
        s.sendline(create_file_command)
        s.prompt()
        print "Restarting httpd..."
        s.sendline("/sbin/service httpd restart")
        s.close()
    except Exception, e:
        print "Error executing ssh commands on " + hostname + ": \n\n" + str(e) + "\n\n"

    time.sleep(3)
    rails = rails_sqt_testing_selenium.RailsSeleniumTest('setUp')
    try:
        rails.setUp(hostname)
        rails.test_rails()
        rails.tearDown()
        return "[+] Rails Webapp: Success"
    except Exception, e:
        return "[-] Rails Webapp: Failure\n\n" + str(e) + "\n\n"


def connect(host, username, password):
    try:
        c = pxssh.pxssh()
        c.login(host, username, password)
        return c
    except Exception, e:
        print "Error Connecting: \n" + str(e)


def verify_password(text):
    tmp_pass1 = getpass.getpass(text)
    tmp_pass2 = getpass.getpass("One more time: ")
    if tmp_pass1 == tmp_pass2:
        return tmp_pass1
    else:
        print "Password's don't match."
        exit()


def tear_down(results, hostname, devel_pass):
    if results[-1][0:3] == "[+]":
        try:
            s = connect(hostname, "devel", devel_pass)
            s.sendline("sudo su")
            s.expect("assword")
            s.prompt()
            s.sendline(devel_pass)
            s.prompt()
            s.sendline("rm -rf /var/lib/rails-app /etc/httpd/conf.d/rails.webapp")
            s.prompt()
            s.sendline("/sbin/service httpd restart")
        except Exception, e:
            print "Exception thrown:\n\n" + str(e) + "\n\n"
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
        alfresco_test(domain, fileName),
        geoserver_test(domain),
        liferay_test(domain),
        openam_test(domain, amadmin_password),
        owf_test(domain),
        rails_test(domain, devel_pass)
    ]
    for result in results:
        print result
    tear_down(results, domain, devel_pass)


if __name__ == "__main__":
    main()
