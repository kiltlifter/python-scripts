#!/usr/bin/python


import DataMaker
import TeamData


def main():
	team_data = TeamData.DataStore()
	maker = DataMaker.Make(team_data)
	# Override to used a defined directory for testing
	team_data.storage_location = "JiraData-2016-04-07-1305"
	# Specify true in order to use canned data
	maker.make_data(canned=True)

if __name__ == "__main__":
	main()
