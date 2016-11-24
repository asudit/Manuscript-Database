input_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\raw_data_copies\\firm_level\\NARA\\NARA_Texas"
output_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\Nara_texas\\Output"

import os, shutil, datetime, csv
import xlrd
#import ghostscript
#from wand.image import Image
from PIL import Image

one_slice = .4
two_slice = .6
threshold = .08

def rename(input_path, output_path):
	if os.path.isdir(input_path) == False:
		new_path = output_path
		meta = input_path.split("\\")
		orig_folder = meta[-2]
		folder_num = orig_folder.split("-", 2)
		file_num = folder_num[-1] + "_" + meta[-1]
		file, filetype = os.path.splitext(file_num)
		file = 'TX' + "_" + "8" + "_" + file
		new_path = new_path + "\\" + file + "_N" + filetype
		#print(new_path)
		shutil.copy(input_path, new_path)
	else:
		folder_list = os.listdir(input_path)
		for element in folder_list:
			next_path = input_path + "\\" + element
			rename(next_path, output_path)


#####################################################################################

if __name__ == '__main__':
	rename(input_path, output_path)


