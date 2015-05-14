#!/usr/bin/python
__author__ = 'sdouglas'


import urllib2
import re

host = "alice.sd.spawar.navy.mil"
request_string = "http://alice.sd.spawar.navy.mil/artifactory/api/search/artifact?name=PPExtension-*.eaz&repos=usmc-snapshot"
user = 'user'
passwd = 'AP6wjZvxYHCvqbJ8tWofzLRxjJq3zCEg7GaCT3'


def urllib_request_helper(target_url, uri, user, password):
    auth_handler = urllib2.HTTPPasswordMgrWithDefaultRealm()
    auth_handler.add_password(
        None,
        uri=uri,
        user=user,
        passwd=password
    )
    handler = urllib2.HTTPBasicAuthHandler(auth_handler)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)

    response = urllib2.urlopen(target_url)
    return response


def find_latest_eaz():
    r = urllib_request_helper(request_string, host, user, passwd)
    find_ext = re.compile('\"uri\"\s:\s\"(.*PPExtension-\d\d\d\d-\d\d-\d\d_.*\.eaz)\"')
    urls = find_ext.findall(r.read())
    last_build = urls[-1:]
    target_eaz = "".join(last_build)
    r.close()
    return target_eaz


def find_download_url():
    eaz_target = find_latest_eaz()
    eaz_request = urllib_request_helper(eaz_target, host, user, passwd)
    eaz_data = eaz_request.read()
    dl_regex = re.compile('\"downloadUri\"\s:\s\"(.*)\",')
    download_url = "".join(dl_regex.findall(eaz_data)[0])
    return download_url


def download_latest():
    target_url = find_download_url()
    print target_url
    final_request = urllib_request_helper(target_url, host, user, passwd)
    BLOCK = 16 * 1024
    fp = open("C:\Users\devel\AppData\Roaming\ESRI\ArcGIS Explorer\AddIns\PPExtension.eaz", "wb")
    while True:
        chunk = final_request.read(BLOCK)
        if not chunk: break
        fp.write(chunk)
    fp.close()
    print "Finished."

download_latest()
