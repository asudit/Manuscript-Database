# This python file will take ancestry files and incorporate their meta-data into their file names. 
# The new files are outputed to the "out" folder in ancestry

#execute command: exec(open("D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\Familysearch\\Code\\Rename_Famsearch.py").read()) 
#final_path_test = os.path.isdir("D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\Familysearch\\Input\\microfilm_copy")

#Run time: < 1 s

import os, shutil, datetime, csv
import xlrd
import ghostscript
#from wand.image import Image
from PIL import Image

one_slice = .4
two_slice = .6
threshold = .08

#input_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\Familysearch\\Input\\microfilm_copy"
input_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\raw_data_copies\\Familysearch_scans\\microfilm"
output_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\Familysearch\\Output_final"
temp_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\Familysearch\\Temp"

test_input = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\Familysearch\\Input\\microfilm_copy\\arkansas_1549733_item2.tif"
remove = ['.dropbox', 'desktop.ini', 'Ohio_1602417.pdf', 'Ohio_1602422.pdf']
state_abbrev = {'ohio' :'OH', 'pennsylvania' : 'PA', 'arkansas' : 'AR'}
# someone inconsistently named the files for these counties
county_exception = ['trumbull', 'tuscarawas', 'vinton', 'richland']

def collect(input_path):
	#print("Current path is:", input_path)

	#base case
	if os.path.isdir(input_path) == False:
		#return {'root' : input_path}
		x = 'root'
		return x
	#recursive case
	else:
		folder_contents = os.listdir(input_path)
		#the original folder is open(so dropbox is in there etc), 
		#but the copied one is not. hence remove[2], not remove[0]
		if remove[2] in folder_contents: 
			for x in remove:
				if x in folder_contents:
					folder_contents.remove(x) 
		current_dictionary = {}
		for element in folder_contents:
			current_path = input_path + "\\" + element
			lower_dictionary = collect(current_path)
			#if lower_dictionary == 'root':
				#file = element.split('_')
				#element = file[0]
				#file.remove(element)
				#for y in range(len(file)):
				#element = element + "\\" + file[y]
			current_dictionary[element] = lower_dictionary
		return current_dictionary
			

def populate(dictionary, current_path):
	keys = list(dictionary.keys())
	#print(keys)
	if 'root' in list(dictionary.values()):
		for key in keys:
			old_path = current_path + "\\" + key
			if os.path.isdir(old_path):
				#print(old_path)
				next_path = old_path
				populate(dictionary[key], next_path)
				continue

			meta = key.split('_')
			#print(decomp)
			if len(meta) == 4:
				state, year, county, file_num = meta[0].lower(), meta[1], meta[2], meta[3]
			if len(meta) == 3:
				for x in ['trumbull', 'tuscarawas']:
					if x in meta[2]:
						meta[2].split(x)[1]
						meta[2] = x
						meta.append(file_num)
						state, year, county, file_num = meta[0].lower(), meta[1], meta[2], meta[3]
						
			if year == '1879':
				year = '1880'
				
			meta_list = [state, year, county, file_num]	
			for exception in county_exception:
				if exception in meta_list[2]:
					meta_list[2] = exception
					break
			#if 'trumbull' in decomp[2]:
				#decomp[2] = 'trumbull'
			#if 'tuscarawas' in decomp[2]:
				#decomp[2] = 'tuscarawas'
			new_path = output_path
			for piece in [state, year]:
				new_path = new_path + "\\" + piece
				if os.path.isdir(new_path) == False:
					os.makedirs(new_path)
			num = file_num.split('.')
			#print(num)
			file_num_final = '0' * ( 5 - len(num[0])) + file_num
			#print(file_num_final)
			file = "_".join([state_abbrev[state],year, county, file_num_final])
			new_path = new_path + "\\" + file
			#shutil.copy(old_path, new_path)
			format_img(old_path, new_path)
	else:
		for key in keys:
			next_path = current_path + "\\" + key
			if os.path.isdir(next_path):
				populate(dictionary[key], next_path)


def format_img(old_path, new_path):
	img = Image.open(old_path)
	width, height  = img.size
	#in two folders, the images are oriented the wrong way
	if 'ohio_1602337.tif' in old_path or 'ohio_16024422.tif' in old_path:
		img2 = img.rotate(90, expand = True) #expand prevents cropping of rotated image
		img = img2
		width, height = img.size
	if width > height and abs(float(width - height))/float(height) > threshold:
		transfer_path = new_path.rsplit("\\", 1)
		filename, filetype = os.path.splitext(transfer_path[1])

		width_one = one_slice * width
		width_two = two_slice * width
		image_one, image_two = img, img
		if os.path.isfile(transfer_path[0] + "\\" + filename + '_' + '2half' + '.jpg') == False:
			image_one.crop((int(width_one), 0, width, height)).save(transfer_path[0] + "\\" + filename + '_' + '2half' + "_F" + '.jpg')
			image_two.crop((0, 0, int(width_two), height)).save(transfer_path[0] + "\\" + filename + '_' + '1half' + "_F" + '.jpg')
	else: 
		file_path, filetype = os.path.splitext(new_path)
		if os.path.isfile(file_path + "_F" + '.jpg') == False:
			img.save(file_path + "_F" + '.jpg')


def check(dictionario, check_path):
	check_dict = {}
	#counties = set([])
	layer1 = list(dictionario.keys())
	for key in layer1:
		#print(key, dictionario[key])
		layer2 = list(dictionario[key].keys())
		for key2 in layer2:
			meta = key2.split("_")
			#print(meta)
			state = meta[0].lower()
			year = meta[1].lower()
			county = meta[2].lower()
			for exception in county_exception:
				if exception in county:
					county = exception
					break
			if state_abbrev[state] not in check_dict:
				check_dict[state_abbrev[state]] = set([])
			check_dict[state_abbrev[state]].add(county)
	#print(check_dict)

	missing_counties = {}
	with open(check_path, 'rt') as f:
		file = csv.reader(f)
		file.__next__()
		for row in f:
			row_list = row.split(',')
			county_csv = row_list[2].lower()
			state_csv = row_list[1]
			if state_csv in list(check_dict.keys()) and county_csv not in check_dict[state_csv]:
				if state_csv not in missing_counties:
					missing_counties[state_csv] = set([])
				missing_counties[state_csv].add(county_csv)

	return missing_counties


def missing_csv(filename, missing_counties):
	with open(filename, 'w', newline = '') as f:
            writer = csv.writer(f)
            writer.writerow(['State', 'Missing County'])
            states = list(missing_counties.keys())
            for state in states:
            	for county in missing_counties[state]:
                	writer.writerow([state, county])







######################################################################
if __name__ == '__main__':
	dictionary = collect(input_path)
	#missing_counties = check(dictionary, temp_path + "\\" + 'year_state_county_list.csv')
	#missing_csv(temp_path + "\\" + 'Family_Scan_MissingCounties.csv', missing_counties)
	populate(dictionary, input_path)











