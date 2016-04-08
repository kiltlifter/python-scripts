#!/usr/bin/python


import requests
import os


class Request():
	def __init__(self, team_data):
		self.team_data = team_data

	def request_url(self, url):
		try:
			cookie_monster = {
			}
			headers = {
			}
			r = requests.get(url, headers=headers, cookies=cookie_monster)
			return r
		except Exception as e:
			print "Failed request for:\n%s" % url
			print str(e)

	def write_xml_file(self, file_path, xml_data):
		try:
			with open(file_path, 'w') as xml_file:
				xml_file.write(xml_data)
		except Exception as e:
			print "Failed to write xml file."
			print str(e)


	def get_team_urls(self):
		url_list = []
		for key in self.team_data.team_naming_data:
			for val in self.team_data.team_naming_data[key]['xml urls']:
				url_list.append(val)
		return url_list

	def retrieve(self):
		try:
			team_url_list = self.get_team_urls()
		except Exception as e:
			print "Extracting team urls failed."
			print "Have a look at the get_team_urls function."
			print str(e)
			exit()

		try:
			os.mkdir(self.team_data.storage_location)
		except Exception as e:
			print "Failed to make directory: %s" % self.team_data.storage_location
			print str(e)

		try:
			query_download_path = []
			for query in team_url_list:
				request_data = self.request_url(query[1])
				if request_data.status_code == 200:
					file_path = "%s/%s.xml" % (self.team_data.storage_location, query[0])
					self.write_xml_file(file_path, request_data.text)
					query_download_path.append(file_path)
				else:
					print "Status Code: %i" % request_data.status_code
					print "Query %s\nprovided a status code != 200." % query[0]
			return query_download_path
		except Exception as e:
			print "Failed to loop through team_url_list and process request/write to file."
			print str(e)
