#!/usr/bin/python
import requests, sys, time, os, json

# This is the agrument provided when you run this script
url = "https://brkevin:8443/BRVT/rest/user/me"

# Add any custom headers you would like
headers = {"User-Agent": "None"}

# Add the cookies that are set when you make this request in the browser
#cookies = {"OZONELOGIN": "true", "amlbcookie": "01", "iPlanetDirectoryPro": "AQIC5wM2LY4SfcyXbk1BzflmJtjmpryQ1wVwhK8d_4jiSLo.*AAJTSQACMDEAAlNLABM1NTMxODAzNTU4MzUxNjAyOTM3*"}
cookies = {"JSESSIONID": "FEAA2DEABB41E82D6EE7ACE13F4884EA"}
# Number of requests to send
num_requests = 10000

s = requests.Session()

for i in range(num_requests):
	try:
		r = s.get(url, cookies=cookies, headers=headers, verify=False)
		message = json.loads(r.text)
		print "%s\n%s" % (message["userName"], message['ID'])

	except requests.exceptions.ConnectionError as e:
		print e

print "Finished, %s request to %s sent." % (num_requests, url)