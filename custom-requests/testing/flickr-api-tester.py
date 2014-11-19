#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests, os, time, json, sys
from datetime import date

method = sys.argv[1]

url = "https://api.flickr.com/services/rest/?method=" + str(method) + "&api_key=895c6a33781e702e22a6bb958539f099&format=rest"
r = requests.get(url)
print r.text