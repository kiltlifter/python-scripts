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

	parser.stats()
	#requirements_with_priority = parser.prioritized_requirements()
	#enriched_group_data = parser.groups_with_added_data()
	#uids_in_groups = parser.requirements_in_cd3()
	#sheet_data = Analyzer.build_sheet_data(enriched_group_data=enriched_group_data,
	#						  requirements_with_priority=requirements_with_priority,
	#						  uids_in_groups=uids_in_groups)

	#writer = Writer.Write(filename, "CD3 Requirements")
	#writer.write_sheet(sheet_data)
	print(Analyzer.natural_sort(parser.cd3_groups()))

if __name__ == "__main__":
	main()

