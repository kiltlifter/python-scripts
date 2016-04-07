#!/usr/bin/python


import sys
import DataMaker 


def main():
	# Eventially a the class that makes a request for the xml data
	# should be used rather than having to base an xml file manually.
	# I think you should then be able to just supply the DataMaker
	# with the path to the directory.
	try:
		#filename = sys.argv[1]
		filename = "Tiger Team - Rollover - Sprint 16 2016-04-05.xml"
	except:
		print "No file supplied."
		exit()

	maker = DataMaker.Make()
	#maker.process_team(filename, "Tiger Team")
	maker.testing(filename)


if __name__ == "__main__":
	main()
