import xmltodict
import json
import IssueUtil

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

	def parse_issues(self):
		data = self.remove_cruft()
		for issue in data['item']:
			print IssueUtil.Parser(issue).get_all()


	def run(self):
		self.parse_issues()
