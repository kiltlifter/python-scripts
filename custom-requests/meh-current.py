#!/usr/bin/python

import requests
from bs4 import BeautifulSoup as bs
import re

r = requests.get("http://www.meh.com")
if r.status_code == 200:
	soup = bs(r.text)
else:
	print "Couldn't get the requested url"
	exit()

features = soup.find("section", class_="features")
print features
