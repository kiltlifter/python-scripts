import xml.etree.ElementTree as ET


severity_mapping = {
	'13641': 'Severity 1',
	'13642': 'Severity 2',
	'13643': 'Severity 3',
	'13644': 'Severity 4',
	'13645': 'Severity 5',
}

class Parser():
	def init(self):
		None
	
	def parse_xml(self, file_name):
		try:
			tree = ET.parse(file_name)
			root = tree.getroot()
		except Exception as e:
			print "Error opening %s" % file_name
			print "%s" % type(self).__name__
			print str(e)

		item_list = []
		for channel in root:
			for data in channel:
				if data.tag == "item":
					item_list.append(data)
	
		issue_data = {}
		ticket_num = ""
		for item in item_list:
			issue_dict = {'components': []}
			for field in item:
				if field.tag == "key":
					ticket_num = field.text
				if field.tag == "title":
					issue_dict["title"] = field.text
				if field.tag == "link":
					issue_dict["link"] = field.text
				if field.tag == "labels":
					labels = []
					for label in field:
						labels.append(label.text)
					issue_dict["labels"] = labels
				if field.tag == "component":
					issue_dict['components'].append(field.text)
				if field.tag == "customfields":
					for cust in field:
						if cust.attrib['id'] == "customfield_13322":
							issue_dict["severity"] = severity_mapping[cust[1][0].attrib['key']]
						if cust.attrib['id'] == "customfield_10023":
								issue_dict["story points"] = float(cust[1][0].text)
				if field.tag == "created":
					issue_dict["created"] = field.text
				if field.tag == "status":
					issue_dict["status"] = field.text
				#if field.tag == "":
				#	issue_dict[""] = field.
			if 'story points' not in issue_dict:	
				issue_dict['story points'] = float(0.00)
			if 'severity' not in issue_dict:
				issue_dict['severity'] = "Not Defined"
			issue_data[ticket_num] = issue_dict
		return issue_data
	
	
