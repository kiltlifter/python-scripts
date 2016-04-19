import logging

class Parser:
	def __init__(self):
		None

	# When passed a single issue, return the amount of story points as a float
	def get_story_points(self, issue):
		for field in issue['customfields']['customfield']:
			try:
				if field['customfieldname'] == "Story Points":
					value = float(field['customfieldvalues']['customfieldvalue'])
					if value is None:
						return float(0.00)
					return value

			except:
				logging.error("Could not parse story points for %s" % field['key'])
				exit()

