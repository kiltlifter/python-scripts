class Extract():
	def __init__(self, data):
		self.data = data
	
	def convert_to_list(self, dict_to_convert, header=None):
		new_list = []
		try:
			if type(header) == list and len(header) == 2:
				new_list.append(header)
		except Exception as e:
			print "Excluding provided header."
			print str(e)
		for key, val in dict.iteritems(dict_to_convert):
			temp = [key, val]
			new_list.append(temp)
		return new_list

	def get_total_story_points_by_status(self, header=None):
		temp = {}
		for index, value in enumerate(self.data):
			if self.data[value]['status'] in temp:
				temp[self.data[value]['status']] += self.data[value]['story points']
			else:
				temp[self.data[value]['status']] = self.data[value]['story points']
		return self.convert_to_list(temp, header)	
	
	def get_total_story_points_by_severity(self, header=None):
		temp = {}
		for index, value in enumerate(self.data):
			if self.data[value]['severity'] in temp:
				temp[self.data[value]['severity']] += self.data[value]['story points']
			else:
				temp[self.data[value]['severity']] = self.data[value]['story points']
		return self.convert_to_list(temp, header)

	def get_total_issues_by_status(self, header=None):
		temp = {}
		for index, value in enumerate(self.data):
			if self.data[value]['status'] in temp:
				temp[self.data[value]['status']] += 1
			else:
				temp[self.data[value]['status']] = 1
		return self.convert_to_list(temp, header)	

	def get_total_issues_by_severity(self, header=None):
		temp = {}
		for index, value in enumerate(self.data):
			if self.data[value]['severity'] in temp:
				temp[self.data[value]['severity']] += 1
			else:
				temp[self.data[value]['severity']] = 1
		return self.convert_to_list(temp, header)	

	def get_total_resolved_story_points(self, header=None):
		story_points_by_status = self.get_total_story_points_by_status()
		open_close_totals = {}
		for status in story_points_by_status:
			if status[0] == ("Resolved" or "Closed"):
				if 'Completed' in open_close_totals:
					open_close_totals['Completed'] += status[1]
				else:
					open_close_totals['Completed'] = status[1]
			else:
				if 'Open' in open_close_totals:
					open_close_totals['Open'] += status[1]
				else:
					open_close_totals['Open'] = status[1]
		return self.convert_to_list(open_close_totals, header)
				
	def combine_similar_lists(self, list1, list2):
		self.data = {}
		end_list = list1
		try:
			similar = False
			for row1 in list1:
				for row2 in list2:
					if row1 == row2:
						similar = True
		except Exception as e:	
			print "Lists are probally different"
			print str(e)
		new_list = []
		for a in list2:
			new_list.append(a[1])
		for index, value in enumerate(new_list):
			end_list[index].append(value)
		return end_list
						
