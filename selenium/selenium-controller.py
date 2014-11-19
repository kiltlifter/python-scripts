__author__ = 'sdouglas'


import configure_liferay_selenium
import configure_openam_selenium


def setup_liferay():
    liferay = configure_liferay_selenium.ConfigureLiferaySelenium('setUp')
    try:
        liferay.setUp()
        liferay.test_configure_liferay_selenium()
        liferay.tearDown()
        return "[+] Liferay: Success"
    except Exception, e:
        print "Error configuring Liferay: \n" + str(e)
        return "[-] Liferay: Failure"


def setup_openam():
    openam = configure_openam_selenium.ConfigureOpenamSelenium2('setUp')
    try:
        openam.setUp()
        openam.test_configure_openam_selenium2()
        openam.tearDown()
        return "[+] OpenAM: Success"
    except Exception, e:
        print "Error configuring OpenAM: \n" + str(e)
        return "[-] OpenAM: Failure"


def main():
    results = [
        setup_liferay(),
        setup_openam()
    ]

    for result in results:
        print result

if __name__ == '__main__':
    main()
