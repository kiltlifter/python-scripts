#!/usr/bin/python
__author__ = 'sdouglas'


import configure_liferay_selenium
import configure_openam_selenium
import optparse
import getpass


def setup_liferay(hostName):
    liferay = configure_liferay_selenium.ConfigureLiferaySelenium('setUp')
    try:
        liferay.setUp(hostname=hostName)
        liferay.test_configure_liferay_selenium(hostname=hostName)
        liferay.tearDown()
        return "[+] Liferay: Success"
    except Exception, e:
        print "Error configuring Liferay: \n" + str(e)
        return "[-] Liferay: Failure"


def setup_openam(hostName, amadmin_password):
    openam = configure_openam_selenium.ConfigureOpenamSelenium2('setUp')
    try:
        openam.setUp(hostname=hostName)
        openam.test_configure_openam_selenium2(hostname=hostName, amadmin_pass=str(amadmin_password))
        openam.tearDown()
        return "[+] OpenAM: Success"
    except Exception, e:
        print "Error configuring OpenAM: \n" + str(e)
        return "[-] OpenAM: Failure"


def verify_password(text):
    tmp_pass1 = getpass.getpass(text)
    tmp_pass2 = getpass.getpass("One more time: ")
    if tmp_pass1 == tmp_pass2:
        return tmp_pass1
    else:
        print "Password's don't match."
        exit()


def main():
    parser = optparse.OptionParser("selenium_configurator.py -d <domain>")
    parser.add_option('-d', dest='hostName', type='string', help='specify a domain name')
    (options, args) = parser.parse_args()
    host_name = options.hostName
    if host_name is None:
        print parser.usage
        exit()
    amadmin_password = verify_password("Enter amadmin Password: ")
    results = [
        #setup_openam(host_name, amadmin_password),
        setup_liferay(host_name)
    ]
    
    for result in results:
        print result

if __name__ == '__main__':
    main()
