#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests, os, json
from datetime import date

today = date.today()
url = "https://secure.flickr.com/explore?data=1&day=" + str(today) + "&view=ju&start=50&count=100&append=1&magic_cookie="
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'}

def query_flickr_api():
	print url
	session = requests.session()
	r = session.get(url, headers=headers)
	json_content = json.loads(r.text, encoding='utf-8')
	return json_content

def get_image_sizes(json_blob):
	picture_sizes = []
	for item in json_blob:
		pic_name = item["name"]
		pic_url = ""
		base_size = 0
		temp_var = ""
		for key, value in item['sizes'].items():	
			if int(value['width']) > base_size:
				temp_var = value['url']
				base_size = int(value['width'])
		pic_url = temp_var
		picture_sizes.append([pic_name, pic_url])
	return picture_sizes

def download_image(title, image_url):
	image_request = requests.get(image_url, stream=True)
	if image_request.status_code == 200:
		try:
			print "Saving image: " + str(title) + ".jpg\n"
			with open("/tmp/flickr/" + title + ".jpg", 'wb') as img:
				for block in image_request.iter_content(512):
					img.write(block)
		except:
			print "\n[ERROR]: Something went wrong with this picture\n"

def main():
	json_file = query_flickr_api()
	#json_dict = json.loads(json_file)
	largest_photos = get_image_sizes(json_file)
	for img in largest_photos:
		try:
			download_image(img[0], img[1])
		except Exception as e:
			"#########!!!!!!!!!!Something went wrong!!!!!!!!!!!!!!!!###########"

if __name__ == '__main__':
	main()
