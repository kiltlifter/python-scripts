import ParseXMLJIRA
import BarChartJIRA
import ExtractDataJIRA
import PieChartData
import EmailFormater
import datetime

# This is added to saved file names
date_stamp = str(datetime.date.today())

class Make():
	def __init__(self):
		# Store all naming data for graphs in a dictionary for ease of use.
		# In the future a implementing this in json, csv, or something else
		# might be a better option
		self.team_naming_data = {
			# This is the team name passed to self.process_team
			# You should add error checking to that...
			'Tiger Team': {
				# This names are intended to be idiot proof, but the name length
				# kind of bugs me.
				'file name one': "Tiger Team Status by Severity %s" % date_stamp,
				'file name two': "Tiger Team Status by Issue Type %s" % date_stamp,
				'file name three': "Tiger Team Progress %s" % date_stamp,
				'chart one title': 'Tiger Team Status by Severity',
				'chart two title': 'Tiger Team Status by Issue Type',
				'chart three title': 'Tiger Team Progress'
			},
			'Integration': {
				'file name one': "Integration Status by Severity %s" % date_stamp,
				'file name two': "Integration Status by Issue Type %s" % date_stamp,
				'file name three': "Integration Progress %s" % date_stamp,
				'chart one title': 'Integration Status by Severity',
				'chart two title': 'Integration Status by Issue Type',
				'chart three title': 'Integration Progress'
			},
			'Test Team': {
				'file name one': "Test Team Status by Severity %s" % date_stamp,
				'file name two': "Test Team Status by Issue Type %s" % date_stamp,
				'file name three': "Test Team Progress %s" % date_stamp,
				'chart one title': 'Test Team Status by Severity',
				'chart two title': 'Test Team Status by Issue Type',
				'chart three title': 'Test Team Progress'
			},
			'User Facing Services': {
				'file name one': "User Facing Services Status by Severity %s" % date_stamp,
				'file name two': "User Facing Services Status by Issue Type %s" % date_stamp,
				'file name three': "User Facing Services Progress %s" % date_stamp,
				'chart one title': 'User Facing Services Status by Severity',
				'chart two title': 'User Facing Services Status by Issue Type',
				'chart three title': 'User Facing Services Progress'
			},
			'Data Management': {
				'file name one': "Data Management Status by Severity %s" % date_stamp,
				'file name two': "Data Management Status by Issue Type %s" % date_stamp,
				'file name three': "Data Management Progress %s" % date_stamp,
				'chart one title': 'Data Management Status by Severity',
				'chart two title': 'Data Management Status by Issue Type',
				'chart three title': 'Data Management Progress'
			}
		}

	def process_team(self, filename, team_name):
		parse = ParseXMLJIRA.Parser()
		issue_dict = parse.parse_tiger_team_xml(filename)

		extraction = ExtractDataJIRA.Extract(issue_dict)
		results = []
		results.append(extraction.get_total_story_points_by_status(["Status", "Total Points"]))
		results.append(extraction.get_total_story_points_by_severity(["Severity", "Total Points"]))
		results.append(extraction.get_total_issues_by_status(["Status", "Total Issues"]))
		results.append(extraction.get_total_issues_by_severity(["Severity", "Total Issues"]))
		results.append(extraction.get_total_resolved_story_points(["Progress", "Total Points"]))
		results.append(extraction.combine_similar_lists(results[1], results[3]))
		results.append(extraction.combine_similar_lists(results[0], results[2]))
	
		graph = BarChartJIRA.Graph()
		graph.bar_chart(
			self.team_naming_data[team_name]['file name one'],
			results[5],
			self.team_naming_data[team_name]['chart one title']
		)
		graph.bar_chart(
			self.team_naming_data[team_name]['file name two'],
			results[6],
			self.team_naming_data[team_name]['chart two title']
		)
	
		pie = PieChartData.PieGraph()
		# TODO: Standardize the format for passing data to ALL charting classes
		pie.chart(
			results[4],
			self.team_naming_data[team_name]['file name three'], 
			self.team_naming_data[team_name]['chart three title'],
			point_total=None
		)	
		# TODO: Add the previous work with pie charts
		# TODO: Combine all this into one exel file, not multiple...

	def testing(self, filename):
		parse = ParseXMLJIRA.Parser()
		issue_dict = parse.parse_tiger_team_xml(filename)

		extraction = ExtractDataJIRA.Extract(issue_dict)
		results = []
		results.append(extraction.get_total_story_points_by_status(["Status", "Total Points"]))
		results.append(extraction.get_total_story_points_by_severity(["Severity", "Total Points"]))
		results.append(extraction.get_total_issues_by_status(["Status", "Total Issues"]))
		results.append(extraction.get_total_issues_by_severity(["Severity", "Total Issues"]))
		results.append(extraction.get_total_resolved_story_points(["Progress", "Total Points"]))
		results.append(extraction.combine_similar_lists(results[1], results[3]))
		results.append(extraction.combine_similar_lists(results[0], results[2]))

		email = EmailFormater.Email(results)
		email.format_message()