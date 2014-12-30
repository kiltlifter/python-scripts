#!/usr/bin/python
__author__ = 'blackglas'

from subprocess import *
import optparse
import getpass
import re


def wpa_supplicant_connect(interface, ssid, password, log_file):
    command = '/sbin/wpa_supplicant -i %s -D wext -c <(/usr/bin/wpa_passphrase "%s" %s) -d' % (interface, ssid, password)
    return Popen(command, shell=True, executable="/bin/bash", stderr=log_file, stdout=log_file)


def dhcp_request(interface):
    command = 'dhclient %s' % interface
    Popen(command, shell=True, executable="/bin/bash")


def execute_functions(interface, ssid, password):
    with open("wpa_supplicant.log", "w") as log_file:
        check = ""
        connection = wpa_supplicant_connect(interface, ssid, password, log_file)
        connection_pids = [connection.pid, connection.pid + 1]
        dhcp_request(interface)
        while check != re.match("[S|s]top", check):
            Popen("clear")
            print "Interface %s connected to SSID %s." % (interface, ssid)
            check = raw_input("Enter 'stop' to disconnect")
        command = "kill %s %s" % (connection_pids[0], connection_pids[1])
        Popen(command, shell=True, stderr=PIPE).stderr.read()


def main():
    parser = optparse.OptionParser("wifi-connect.py -i <iface> -s <ssid>")
    parser.add_option("-i", dest="iface", type="string", help="enter an interface")
    parser.add_option("-s", dest="ssid", type="string", help="enter ssid")
    (options, args) = parser.parse_args()
    if (options.iface is None) or (options.ssid is None):
        print parser.usage
        exit()
    else:
        password = getpass.getpass("Network Password: ")
        execute_functions(options.iface, options.ssid, password)

if __name__ == '__main__':
    main()
