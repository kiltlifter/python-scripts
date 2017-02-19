#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import re

__author__ = "sean douglas"


def sort_by_priority(requirements):
	return sorted(requirements, key=lambda x: x[3])


def build_sheet_data(enriched_group_data, requirements_with_priority, uids_in_groups):
	row_list = []
	for group in uids_in_groups:
		for req in uids_in_groups[group]['requirements']:
			uid = req
			requirement_data = requirements_with_priority[uid]
			row_list.append([uid, requirement_data[0], requirement_data[1], requirement_data[2], group]
							+ enriched_group_data[group])
	return sort_by_priority(row_list)


def atoi(text):
	try:
		return int(text)
	except:
		None


def natural_keys(text):
	return [atoi(c) for c in re.findall('(\d+)', text)]


def natural_sort(groups):
	sorted_groups = groups.sort(key=natural_keys)
	print(sorted_groups)
	for group in groups:
		print("Group{}".format(natural_keys(group)[0]))

