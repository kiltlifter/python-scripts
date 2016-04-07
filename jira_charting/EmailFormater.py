class Email():
	def __init__(self, data):
		self.data = data
	
	def format_message(self):
		for list in self.data:
			for row in list:
				formated = ""
				for a in xrange(len(row)):
					if len(formated) > 0:
						formated = formated + "\t|\t" + str(row[a])
					else:
						formated = str(row[a]) + "\t"
				print formated
			print ""

