import xmltodict
import json
import IssueData

class Parse:
	def __init__(self, filename):
		self.xml_file = filename

	# Converts a xml file to a dictionary by leveraging the xmltodict module
	# https://github.com/martinblech/xmltodict
	def convert_to_dict(self):
		with open(self.xml_file, 'r') as f:
			return xmltodict.parse(f.read())

	# Removed the initial elements which are not needed
	def remove_cruft(self):
		data_dictionary = self.convert_to_dict()
		issues = data_dictionary['rss']['channel']
		return issues

	# In the future if you need to convert your xml representation of the data into json format, use this method.
	def dump_to_json(self, data):
		json_data = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
		with open(self.xml_file[:-4]+".json", "w") as f:
			f.write(json_data)

	# When passed a single issue, return the amount of story points as a float
	def get_story_points(self, issue):
		for field in issue['customfields']['customfield']:
			try:
				if field['customfieldname'] == "Story Points":
					print field['customfieldvalues']['customfieldvalue']
			except:
				pass


	def parse_issues(self):
		data = self.remove_cruft()
		issue_parser = IssueData.Parser()
		for issue in data['item']:
			print issue_parser.get_story_points(issue)



	def run(self):
		self.parse_issues()
