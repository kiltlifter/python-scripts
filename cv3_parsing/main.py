#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from os.path import normpath
import ParseExcel
import Analyzer
import Writer

__author__ = "sean douglas"


def main():
	filename = normpath("C:/Users/blackglas/Documents/work/reverse-cv3-with-priorities_merged_with_Standards.xlsx")
	parser = ParseExcel.Parser(filename)
	parser.features_sheet = "features"
	parser.groups_sheet = "groups"

	stats = parser.stats()

	# Collect data for the CD3 tab
	#cd3_requirements_with_priority = parser.prioritized_requirements()
	#cd3_enriched_group_data = parser.groups_with_added_data()
	#cd3_uids_in_groups = parser.requirements_in_cd3()
	#cd3_sheet_data = Analyzer.build_sheet_data(enriched_group_data=cd3_enriched_group_data,
	#						  requirements_with_priority=cd3_requirements_with_priority,
	#						  uids_in_groups=cd3_uids_in_groups)

	# Collect data for the CD2 and CD3 tab
	#requirements_with_priority = parser.prioritized_requirements_cd2_and_cd3()
	#enriched_group_data = parser.cd2_and_cd3_groups_with_added_data()
	#uids_in_groups = parser.requirements_in_cd2_and_3()
	#cd2_and_cd3_sheet_data = Analyzer.build_sheet_data_cd2_and_cd3(enriched_group_data=enriched_group_data,
	#						  requirements_with_priority=requirements_with_priority,
	#						  uids_in_groups=uids_in_groups)

	# Instantiate a writer and write data to the CD3 tab
	#writer = Writer.Write(filename, "CD3 Requirements")
	#writer.write_sheet(cd3_sheet_data)
	#writer.write_sheet_data()

	# Instantiate a writer and write data to the CD2 and CD3 tab
	#writer2 = Writer.Write(filename, "CD2 and CD3 Requirements")
	#writer2.write_cd2_and_cd3_sheet(cd2_and_cd3_sheet_data)
	#writer2.write_sheet_data()

	# Instantiate a writer and highlight CD2 UIDs not in CD3
	#writer3 = Writer.Write(filename, "CD2 and CD3 Requirements")
	#writer3.highlight_cd2_in_cd3_requirements(parser.uids_in_cd3())
	print("----------\n\n")
	#writer3.highlight_cd2_not_in_cd3_requirements(parser.uids_in_cd3())
	#writer3.write_sheet_data()

if __name__ == "__main__":
	main()

