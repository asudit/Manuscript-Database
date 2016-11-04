#  exec(open("D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\Familysearch\\Code\\Check_Famsearch.py").read()) 

check_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\Familysearch\\Temp\\year_state_county_list.csv"
module_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\Familysearch\\Code\\Rename_Famsearch.py"

import sys
#sys.path.insert(0, module_path)
import os, shutil, datetime, csv, xlrd

input_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\Familysearch\\Input\\microfilm_copy"
output_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\Familysearch\\Output"

remove = ['.dropbox', 'desktop.ini', 'Ohio_1602417.pdf', 'Ohio_1602422.pdf']

dictionary = collect(input_path)


def check(dictionario, check_path):
	counties = set([])
	layer1 = list(dictionario.keys())
	for key in layer1:
		print(key, dictionario[key])
		layer2 = list(dictionario[key].keys())
		for key2 in layer2:
			meta = key2.split("_")
			year = meta[1]
			county = meta[2]
			counties.add(county)

	with open(check_path, 'rt') as f:
		file = csv.reader(f)
		file.__next__()
		for row in f:
			print(row)
	
