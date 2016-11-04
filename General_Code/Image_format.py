# exceute: 

import os, shutil, csv
from wand.image import Image #once Wand is installed on both computers

one_slice = .4
two_slice = .6

test_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\manuscript_database\\ancestry\\Output\\california\\industry\\1850\\el dorado\\Matheney Creek\\california_industry_1850_el dorado_Matheney Creek_31560_204081-00067.jpg"

def format(current_path):
	with Image(filename = current_path) as img:
		width = img.width
		height = img.height
		if width > height: #this is just a baseline criteria for determining if doc has two pages
			img.format = 'jpeg'
			width_one = one_slice * width
			width_two = two_slice * width
			image_one = img[width_one:width, 0:height]
			image_two = img[0:width_two, 0:height]
			new_path = current_path.rsplit("\\", 1)
			filename, filetype = os.path.splittext(new_path[1])
			image_one.save(filename = new_path[0] + "\\" + 'filename' + '_' + 'two' + '.jpeg') #we need to check save also take path, not just filename
			image_two.save(filename = new_path[0] + "\\" + filename + '_' + '.jpeg')





