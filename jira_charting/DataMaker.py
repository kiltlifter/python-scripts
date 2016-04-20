import ParseXMLJIRA
import BarChartJIRA
import ExtractDataJIRA
import PieChartData
import ExtractFromXML
import LineChartJIRA
import RequestXML
import datetime
import os
import logging

# This is added to saved file names
date_stamp = str(datetime.date.today())


class Make():
	def __init__(self, team_data):
		self.team_data = team_data
		self.logfile_path = "%s/%s" % (self.team_data.storage_location, self.team_data.logfile_name)
		try:
			logging.basicConfig(filename=self.logfile_path, level=logging.INFO)
			logging.info("%s: Starting Execution...", str(datetime.datetime.today()))
			print "running"
		except Exception as e:
			print str(e)
			exit()

	def url_is_in(self, url):
		for k in self.team_data.team_naming_data:
			for i in self.team_data.team_naming_data[k]['xml urls']:
				if url in i:
					return k

	def query_is_in(self, path):
		for p in self.team_data.team_naming_data:
			for a in self.team_data.team_naming_data[p]['xml urls']:
				if path.split("/")[-1:][0][:-4] in a:
					return p

	def graph_handler(self, save_as, graph_type, result_set, chart_title):
		if graph_type == "bar":
			try:
				graph = BarChartJIRA.Graph()
				graph.bar_chart(
					save_as,
					result_set,
					chart_title
				)
			except Exception as e:
				print "Error creating graph type: %s" % (graph_type)
				print str(e)

		elif graph_type == "pie":
			try:
				pie = PieChartData.PieGraph()
				pie.chart(
					save_as,
					result_set,
					chart_title
				)
			except Exception as e:
				print "Error creating graph type: %s" % (graph_type)
				print str(e)
		elif graph_type == "line":
			try:
				line = LineChartJIRA.Graph()
				line.date_axis_line_chart(
					save_as,
					result_set,
					chart_title
				)
			except Exception as e:
				print "Error creating graph type: %s" % (graph_type)
				print str(e)

	def process_team(self, path, team_name):
		try:
			parse = ParseXMLJIRA.Parser()
			issue_dict = parse.parse_xml(path)
			extraction = ExtractDataJIRA.Extract(issue_dict)

			results = {}
			line_charts = {}
			bar_charts = {}
			if team_name == "Tiger Team":
				results = {
					"Status by Points": extraction.get_total_story_points_by_status(["Status", "Total Points"]),
					"Status by Issue Count": extraction.get_total_issues_by_status(["Status", "Total Issues"]),
					"Open/Closed Progress": extraction.get_total_resolved_story_points(["Progress", "Total Points"]),
					"Severity by Points": extraction.get_total_story_points_by_severity(["Severity", "Total Points"]),
					"Severity by Issue Count": extraction.get_total_issues_by_severity(["Severity", "Total Issues"])
				}
				bar_charts['Status Title'] = extraction.combine_similar_lists(results['Status by Points'], results['Status by Issue Count'])
				bar_charts['Severity Title'] = extraction.combine_similar_lists(results['Severity by Points'], results['Severity by Issue Count'])
				line_charts['Line Title'] = bar_charts['Severity Title']
			else:
				results = {
					"Status by Points": extraction.get_total_story_points_by_status(["Status", "Total Points"]),
					"Status by Issue Count": extraction.get_total_issues_by_status(["Status", "Total Issues"]),
					"Open/Closed Progress": extraction.get_total_resolved_story_points(["Progress", "Total Points"]),
				}
				bar_charts['Status Title'] = extraction.combine_similar_lists(results['Status by Points'], results['Status by Issue Count'])

			pie_charts = {
				'Progress Title': results['Open/Closed Progress']
			}


			try:
				for index, bar in enumerate(bar_charts):
					chart_title = self.team_data.team_naming_data[team_name][bar_charts.keys()[index]]
					save_as = "%s - %s" % (path[:-4], chart_title)
					self.graph_handler(save_as, "bar", bar_charts[bar], chart_title)
			except Exception as e:
				print "Failed to pass the bar chart data to the graph handler."
				print str(e)

			try:
				for index, pie in enumerate(pie_charts):
					chart_title = self.team_data.team_naming_data[team_name][pie_charts.keys()[index]]
					save_as = "%s - %s" % (path[:-4], chart_title)
					self.graph_handler(save_as, "pie", pie_charts[pie], chart_title)
			except Exception as e:
				print "Failed to pass the pie chart data to the graph handler."
				print str(e)

			try:
				for index, line in enumerate(line_charts):
					chart_title = self.team_data.team_naming_data[team_name][line_charts.keys()[index]]
					save_as = "%s - %s" % (path[:-4], chart_title)
					self.graph_handler(save_as, "line", line_charts[line], chart_title)
			except Exception as e:
				print "Failed to pass the line chart data to the graph handler."
				print str(e)

		except Exception as e:
			print "Failed to process team data."
			print str(e)

	def write_xml_files(self):
		request = RequestXML.Request(self.team_data)
		return request.retrieve()

	def canned_data_testing(self):
		file_paths = []
		for file_name in os.listdir(self.team_data.storage_location):
			file_paths.append("%s/%s" %(self.team_data.storage_location, file_name))
		return file_paths

	def make_data(self, canned=False):
		print "Canned Data: %s" % str(canned)
		try:
			if canned:
				path_to_files = self.canned_data_testing()
			else:
				path_to_files = self.write_xml_files()

			result_set = []
			for path in path_to_files:
				team_name = self.query_is_in(path)
				result_data = self.process_team(path, team_name)
				result_set.append([team_name, result_data])
			return result_set
		except Exception as e:
			print "Error running initial make data."
			print str(e)

	def testing(self, filename):
		self.team_data.filename = "%s/%s" % (self.team_data.storage_location, filename)
		parser = ExtractFromXML.Parse(self.team_data.filename)
		print parser.run()
