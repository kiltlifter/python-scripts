#!/usr/bin/python
__author__ = 'sdouglas'


import sys
from subprocess import *


def check_for_rpm(rpm_name):
    command = "/bin/rpm -q %s" % rpm_name
    output = Popen(command.split(), shell=False, stdout=PIPE).stdout.read().rstrip("\n")
    if output == "package %s is not installed" % rpm_name:
        print "[-] %s is absent." % rpm_name
        exit()
    else:
        print "[+] %s is installed" % rpm_name
        exit()


def main():
    arg = sys.argv[1]
    if arg is None:
        print "usage: rpm-exists.py <rpm-name>"
        exit()
    check_for_rpm(arg)


if __name__ == '__main__':
    main()
