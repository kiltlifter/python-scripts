#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests, os, time

url = "https://my.c2s2.local/owf/j_spring_security_check"
cookie = {'JSESSIONID': '349FC66E76C4AA3D175EFD37D87CA022', 'USGS_accept': 'OK'}
payload = dict(j_username='admin', j_password='C2S2-SAE-default!', submit='Submit')
#payload = {'j_username': 'admin', 'j_password': 'C2S2-SAE-default!', 'submit':'Submit'}

session = requests.Session()
r = session.post(url, cookies=cookie, data=payload, verify=False)
print r.status_code
print r.cookies
print r.text

"""
Request:

POST /owf/j_spring_security_check HTTP/1.1
Host: my.c2s2.local
Connection: keep-alive
Content-Length: 61
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Origin: https://my.c2s2.local
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36
Content-Type: application/x-www-form-urlencoded
DNT: 1
Referer: https://my.c2s2.local/owf/spring_security_login;jsessionid=349FC66E76C4AA3D175EFD37D87CA022
Accept-Encoding: gzip,deflate,sdch
Accept-Language: en-US,en;q=0.8
Cookie: JSESSIONID=349FC66E76C4AA3D175EFD37D87CA022; USGS_accept=OK

Response:

HTTP/1.1 302 Found
Date: Wed, 10 Sep 2014 14:25:06 GMT
Server: Apache-Coyote/1.1
Location: https://my.c2s2.local/owf/
Content-Length: 0
Set-Cookie: JSESSIONID=C690D5DE379E9576C7E521796BDC815C; Path=/owf/; Secure; HttpOnly
Keep-Alive: timeout=15, max=97
Connection: Keep-Alive
Content-Type: text/plain; charset=UTF-8

Form Data:

j_username=admin&j_password=C2S2-SAE-default%21&submit=Submit
"""