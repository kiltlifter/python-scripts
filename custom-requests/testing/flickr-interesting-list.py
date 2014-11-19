#!/usr/bin/python
import requests

url = "https://api.flickr.com/services/rest/?method=flickr.interestingness.getList&api_key=895c6a33781e702e22a6bb958539f099&format=json&nojsoncallback=1"

r = requests.get(url)
print r.text