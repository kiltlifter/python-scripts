import datetime
import time


# This is added to saved file names
date_stamp = str(datetime.date.today())
time_stamp = time.strftime('%H%M')

class DataStore():
	def __init__(self):
		self.storage_location = "JiraData-%s-%s" % (date_stamp, time_stamp)
		self.logfile_name = "jira_charting.log"
		# Store all naming data for graphs in a dictionary for ease of use.
		# In the future a implementing this in json, csv, or something else
		# might be a better option
		self.team_naming_data = {
			# This is the team name passed to self.process_team
			# You should add error checking to that...
			'Tiger Team': {
				# This names are intended to be idiot proof, but the name length
				# kind of bugs me.
				'Severity Title': "Tiger Team Status by Severity %s" % date_stamp,
				'Status Title': "Tiger Team Status by Issue Type %s" % date_stamp,
				'Progress Title': "Tiger Team Progress %s" % date_stamp,
				'Line Title': "Tiger Team Series %s" % date_stamp,
				'xml urls': [
					['Tiger Team - All Created and Resolved', 'http://rite.sd.spawar.navy.mil/jira/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml?jqlQuery=project+%3D+DCGSNSAFE+AND+issuetype+%3D+Bug+AND+component+%3D+TigerTeam+AND+component+in+%28%22Data+Management%22%2C+%22User+Facing+Services%22%2C+%22User+Facing+Services+%22%29+ORDER+BY+status+DESC%2C+Rank+ASC&tempMax=10000'],
					['Tiger Team - Created and Resolved This Month', 'http://rite.sd.spawar.navy.mil/jira/sr/jira.issueviews:searchrequest-xml/19162/SearchRequest-19162.xml?tempMax=10000'],
					['Tiger Team All 30 Epics', 'http://rite.sd.spawar.navy.mil/jira/sr/jira.issueviews:searchrequest-xml/18606/SearchRequest-18606.xml?tempMax=10000']
				]
			},
			'Integration': {
				'Status Title': "Integration Status by Issue Type %s" % date_stamp,
				'Progress Title': "Integration Progress %s" % date_stamp,
				'xml urls': [
					['Integration Team - Remaining 20 - Sprint 16', 'http://rite.sd.spawar.navy.mil/jira/sr/jira.issueviews:searchrequest-xml/18900/SearchRequest-18900.xml?tempMax=10000'],
					['Integration Team - Last 10 - Sprint 16', 'http://rite.sd.spawar.navy.mil/jira/sr/jira.issueviews:searchrequest-xml/18899/SearchRequest-18899.xml?tempMax=10000']
				]
			},
			'Test Team': {
				'Status Title': "Test Team Status by Issue Type %s" % date_stamp,
				'Progress Title': "Test Team Progress %s" % date_stamp,
				'xml urls': [
					['Test Team - Performance Test - Sprint 16', 'http://rite.sd.spawar.navy.mil/jira/sr/jira.issueviews:searchrequest-xml/18907/SearchRequest-18907.xml?tempMax=10000'],
					['Test Team - Rollover - Sprint 16', 'http://rite.sd.spawar.navy.mil/jira/sr/jira.issueviews:searchrequest-xml/18903/SearchRequest-18903.xml?tempMax=10000']
				]
			},
			'User Facing Services': {
				'Status Title': "User Facing Services Status by Issue Type %s" % date_stamp,
				'Progress Title': "User Facing Services Progress %s" % date_stamp,
				'chart one title': 'User Facing Services Status by Issue Type',
				'chart two title': 'User Facing Services Progress',
				'xml urls': []
			},
			'Data Management': {
				'Status Title': "Data Management Status by Issue Type %s" % date_stamp,
				'Progress Title': "Data Management Progress %s" % date_stamp,
				'xml urls': []
			}
		}


