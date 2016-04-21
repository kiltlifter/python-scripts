import logging
import re


class Parser:
	def __init__(self, issue):
		self.issue = issue

	# When passed a single issue, return the amount of story points as a float
	def get_story_points(self):
		for field in self.issue['customfields']['customfield']:
			try:
				if field['customfieldname'] == "Story Points":
					value = float(field['customfieldvalues']['customfieldvalue'])
					return value
			except:
				logging.info("Could not parse story points for %s" % self.issue['key']['#text'])
				exit()

	def get_severity(self):
		for field in self.issue['customfields']['customfield']:
			try:
				if field['customfieldname'] == "IEEE Severity":
					severity_mapping = {
						'13641': 'Severity 1',
						'13642': 'Severity 2',
						'13643': 'Severity 3',
						'13644': 'Severity 4',
						'13645': 'Severity 5',
					}
					severity = severity_mapping[field['customfieldvalues']['customfieldvalue']['@key']]
					return severity
			except:
				logging.info("Could not parse severity for %s" % self.issue['key']['#text'])
				exit()

	def get_key(self):
		try:
			if self.issue['key']['#text']:
				key = self.issue['key']['#text']
				return key
			else:
				logging.info("Couldn't parse the self.issue key, using regular expressions on the title.")
				key = re.findall(r'^\[(\w+-\d+)\]', self.issue['title'])[0]
				return key
		except:
			logging.info("Could not parse key for item.")
			logging.info(self.issue)
			exit()

	def get_title(self):
		try:
			if self.issue['title']:
				title = self.issue['title']
				return title
			else:
				logging.info("Couldn't parse the self.issue title, reverting to the self.issue key.")
				return self.issue['key']['#text']
		except:
			logging.info("Could not parse title for %s" % self.issue['key']['#text'])

	def get_link(self):
		try:
			if self.issue['link']:
				link = self.issue['link']
				return link
			else:
				logging.info("Couldn't parse the self.issue link, constructing a link the best I can.")
				likely_url = "http://rite.sd.spawar.navy.mil/jira/browse/%s" % self.issue['key']['#text']
				return likely_url
		except:
			logging.info("Could not parse link for %s" % self.issue['key']['#text'])

	def get_labels(self):
		try:
			labels = self.issue['labels']['label']
			return labels
		except:
			logging.info("Could not parse labels for %s" % self.issue['key']['#text'])

	def get_components(self):
		try:
			components = self.issue['component']
			return components
		except:
			logging.info("Could not parse components for %s" % self.issue['key']['#text'])

	def get_created(self):
		try:
			created = self.issue['created']
			return created
		except:
			logging.info("Could not parse created field for %s" % self.issue['key']['#text'])

	def get_updated(self):
		try:
			updated = self.issue['updated']
			return updated
		except:
			logging.info("Could not parse updated field for %s" % self.issue['key']['#text'])

	def get_resolution(self):
		try:
			resolution = self.issue['resolution']['#text']
			return resolution
		except:
			logging.info("Could not parse resolution field for %s" % self.issue['key']['#text'])

	def get_status(self):
		try:
			status = self.issue['status']['#text']
			return status
		except:
			logging.info("Could not parse status field for %s" % self.issue['key']['#text'])

	@staticmethod
	def replace_null_values(formatted_issue_dictionary):
		if formatted_issue_dictionary['story points'] is None:
			formatted_issue_dictionary['story points'] = float(0.00)
		if formatted_issue_dictionary['severity'] is None:
			formatted_issue_dictionary['severity'] = "Not Defined"
		return formatted_issue_dictionary

	def get_all(self):
		try:
			issue_results = {
				'story points': self.get_story_points(),
				'severity': self.get_severity(),
				'key': self.get_key(),
				'title': self.get_title(),
				'link': self.get_link(),
				'labels': self.get_labels(),
				'components': self.get_components(),
				'created': self.get_created(),
				'updated': self.get_updated(),
				'resolution': self.get_resolution(),
				'status': self.get_status()
			}
			return self.replace_null_values(issue_results)
		except:
			logging.info("Could not parse and retrieve all data from issue.")
			logging.error(Exception)