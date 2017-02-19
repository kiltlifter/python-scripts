#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from openpyxl import load_workbook

__author__ = "sean douglas"


class Write:
	def __init__(self, filename, cd3_requirements_sheet=None):
		self.filename = filename
		self.wb = load_workbook(filename)
		self.cd3_requirements_sheet = cd3_requirements_sheet

	def write_sheet(self, data):
		requirements_sheet = self.wb.create_sheet("CD3 Requirements")
		header = ("REQUIREMENT", "PARENT", "DESCRIPTION", "PRIORITY", "GROUP", "GROUP IN FEATURE(s)", "OWNER")

		requirements_sheet.append(header)
		for row in data:
			requirements_sheet.append(row)
		self.wb.save(self.filename)
