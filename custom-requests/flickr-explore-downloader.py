#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests, os, time, json, sys
from datetime import date

API_KEY = ""
USER_ID = ""

def query_api(url):
	r = requests.get(url)
	return json.loads(r.text)

def sanitize_title(title, item_id):
	file_name = ""
	if title == "":
		file_name = item_id + "_" + str(date.today())
	else:
		try:
			file_name = title.decode('ascii', 'ignore')
			file_name = file_name.encode('ascii', 'ignore')
		except:
			file_name = item_id + "_" + str(date.today())
	return file_name

def get_interesting_data(input_json):
	photos = input_json['photos']['photo']
	data_list = []
	for item in photos:
		file_name = sanitize_title(item['title'], item['id'])
		data_list.append({'title': file_name, 'id': item['id']})
	return data_list

def find_largest_size(size_list):
	photo_url = ""
	base_size = 0
	for size in size_list['sizes']['size']:
		width = int(size['width'])
		if width > base_size:
			photo_url = size['source']
			base_size = width
	return photo_url

def get_photo_links(title_and_id):
	photo_data = []
	for item in title_and_id:
		photo_id = item['id']
		photo_by_id_query = "https://api.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key="+API_KEY+"&user_id="+USER_ID+"&photo_id="+photo_id+"&format=json&nojsoncallback=1"
		image_sizes = query_api(photo_by_id_query)
		photo_url = find_largest_size(image_sizes)
		photo_data.append({'title': item['title'], 'id': photo_id, 'source': photo_url})
	return photo_data

def download_image(title, image_url):
	image_request = requests.get(image_url, stream=True)
	if image_request.status_code == 200:
		try:
			print "Saving image: " + str(title) + ".jpg"
			with open("/tmp/flickr/" + title + ".jpg", 'wb') as img:
				for block in image_request.iter_content(512):
					img.write(block)
		except:
			print "[ERROR]: Something went wrong with this picture"

def navigate_download_list(download_list):
	for image in download_list:
		download_image(image['title'], image['source'])

def create_file_list():
	os.popen("ls /tmp/flickr/ -1 | sort -R > /tmp/flickr/outfile.txt")

def main():
	interesting_list = "https://api.flickr.com/services/rest/?method=flickr.interestingness.getList&api_key="+API_KEY+"&user_id="+USER_ID+"&format=json&nojsoncallback=1"
	json_response = query_api(interesting_list)
	print "Retrieving flickr explore list..."
	title_and_id = get_interesting_data(json_response)
	print "Finding the highest quality images..."
	complete_list = get_photo_links(title_and_id)
	os.popen("rm -rf /tmp/flickr;mkdir -p /tmp/flickr")
	navigate_download_list(complete_list)
	create_file_list()

if __name__ == '__main__':
	main()
