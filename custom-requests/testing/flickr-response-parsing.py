#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests, os, time, json

def open_file(file_name):
	with open(file_name, 'r') as json_content:
		return json_content.read()
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

def main():
	json_file = open_file("json_response.json")
	json_dict = json.loads(json_file)
	largest_photos = get_image_sizes(json_dict)
	for img in largest_photos:
		try:
			print img[0] + "\n" + img[1]
		except Exception as e:
			"#########!!!!!!!!!!Something went wrong!!!!!!!!!!!!!!!!###########"

if __name__ == '__main__':
	main()