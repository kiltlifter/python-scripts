#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests, os, time, json
from datetime import date

today = date.today()
url = "https://secure.flickr.com/explore?data=1&day="+ str(today) +"&view=ju&start=50&count=100&append=1&magic_cookie=7973d5676566ff2077beed4f5636d248"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'}

session = requests.session()
r = session.get(url, headers=headers)
json_content = json.loads(r.text, encoding='utf-8')

s = json.dumps(json_content, sort_keys=True, indent=4)
print '\n'.join([l.rstrip() for l in  s.splitlines()])

"""

GET /explore?data=1&day=2014-09-09&view=ju&start=50&count=100&append=1&magic_cookie=7973d5676566ff2077beed4f5636d248 HTTP/1.1
Host: secure.flickr.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36
X-Requested-With: XMLHttpRequest
Accept: */*
DNT: 1
Referer: https://secure.flickr.com/explore/
Accept-Encoding: gzip,deflate,sdch
Accept-Language: en-US,en;q=0.8
Cookie: BX=29bpjt99t2c1c&b=3&s=d1; xb=076508; fvmgj=ju; ywandp=10001561398679%3A1131580641%3B10001109650879%3A3118493462; flrbp=1410384725-49d875eae1f8d694300bce668fd592b41304636f; flrbs=1410384725-8cc68eac6fbc51bc204bcae5aea39b6be692d34f; flrbgrp=1410384725-8342b09249ac92888ca657b78c6f9af878aa6f07; flrb=31; localization=en-us%3Bus%3Bus; liqpw=1897; liqph=273

API Key:
a36a8c74f4cbd563e8c7f4739cb5bc6a

API Secret:
c97a61e27a337fd1

"""