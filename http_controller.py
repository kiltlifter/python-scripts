#!/bin/bash
__author__ = 'blackglas'


import re
from scapy.all import *


def find_requests(pkt):
    try:
        raw = pkt.sprintf('%Raw.load%')
        get_request = re.findall('GET\s(.*)\sHTTP', raw)
        host = re.findall(r'Host: (.*)\\r\\nConnection:', raw)
        cookie = re.findall('Cookie:\s(.*)\\\\r\\\\n', raw)
        post_request = re.findall('POST\s(.*)\sHTTP', raw)
        if get_request and host:
            print "\nGET: http://%s%s" % (host[0], get_request[0])
            print "Cookie: %s" % cookie[0].rstrip('\\r\\n')
        if post_request and host:
            print "\nPOST: http://%s%s" % (host[0], post_request[0])
            print "Cookie: %s" % cookie[0].rstrip('\\r\\n')
    except Exception, e:
        print None


def main():
    sniff(prn=find_requests, filter='tcp port 80')


if __name__ == '__main__':
    main()
