#!/usr/bin/python

import DataMaker
import TeamData


def main():
	team_data = TeamData.DataStore()

### Single File Feature testing	###
	# When using the test method you must specify a storage location directory below:
	team_data.storage_location = "JiraData-2016-04-18-1527"
	# Then instantiate the Data Maker with the storage location override
	maker = DataMaker.Make(team_data)
	# and then call the testing method with the xml file you would like to use in the above directory.
	maker.testing("Tiger Team - Created and Resolved This Month.xml")

### Testing a complete data set ###
	# Override to used a defined directory for testing
	# If you want to use canned data from a directory specify it here:
	#team_data.storage_location = ""
	# Then call the make_data method with the canned data flag set to true.
	#maker.make_data(canned=True)

### Production ###
	# To run in production just call:
	#maker.make_data(canned=False)


if __name__ == "__main__":
	main()
