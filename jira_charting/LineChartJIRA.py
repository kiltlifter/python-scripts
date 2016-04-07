from datetime import date
from openpyxl import Workbook
from openpyxl.chart import (
    LineChart,
    Reference,
)
from openpyxl.chart.axis import DateAxis

class Graph():
	def init(self):
		None

	def date_axis_line_chart(self, save_file_name, formatted_data):
		wb = Workbook()
		ws = wb.active
	
		# Sample of what the format should be.
		"""
		rows = [
		    ['Date', 'Batch 1', 'Batch 2', 'Batch 3'],
		    [date(2015,9, 1), 40, 30, 25],
		    [date(2015,9, 2), 40, 25, 30],
		    [date(2015,9, 3), 50, 30, 45],
		    [date(2015,9, 4), 30, 25, 40],
		    [date(2015,9, 5), 25, 35, 30],
		    [date(2015,9, 6), 20, 40, 35],
		]
		"""
		rows = formatted_data
	
		for row in rows:
		    ws.append(row)
		
		# Chart with date axis
		c2 = LineChart()
		c2.title = "Tiger Team - Bug Severity"
		c2.style = 12
		c2.y_axis.title = "Story Points"
		c2.y_axis.crossAx = 500
		c2.x_axis = DateAxis(crossAx=100)
		c2.x_axis.number_format = 'd-mmm'
		c2.x_axis.majorTimeUnit = "days"
		c2.x_axis.title = "Date"
		
		c2.add_data(data, titles_from_data=True)
		dates = Reference(ws, min_col=1, min_row=2, max_row=7)
		c2.set_categories(dates)
		
		ws.add_chart(c2, "G1")
		
		wb.save(save_file_name)
