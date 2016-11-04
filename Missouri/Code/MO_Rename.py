# exec(open("D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Code\\MO_Rename.py").read()) 

import os, shutil, datetime, csv
import xlrd
from wand.image import Image 


one_slice = .4
two_slice = .6

input_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Input\\Missouri_copy"
output_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Output"
temp_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Temp"
test_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Input\\Missouri_copy\\1860 Social Statistics Schedule"
package_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\General\\Packages"

remove = ['1860 Social Statistics Schedule', 'Title Targets', 'Thumbs.db']


def collect(input_path):
	#base case
	if os.path.isdir(input_path) == False:
		x = 'root'
		return x
	#recursive case
	else:
		folder_contents = os.listdir(input_path)
		#print(folder_contents)
		for x in remove:
			if x in folder_contents:
				folder_contents.remove(x)
		current_dictionary = {}
		for element in folder_contents:
			#print(element)
			current_path = input_path + "\\" + element
			lower_dictionary = collect(current_path)
			current_dictionary[element] = lower_dictionary
		return current_dictionary


def populate(old_dictionary, current_path, output_path):
	#print(current_path)
	keys = list(old_dictionary.keys())
	#print(keys)
	if old_dictionary[keys[0]] == 'root':
		for key in keys:
			old_path = current_path + "\\" + key
			meta = key.split("_")
			#a strange exception when meta = ['0000000.tif']
			if len(meta) == 1:
				continue
			state = "MO"
			#print(meta)
			year = meta[2]
			county = meta[-2]
			file_num_and_type = meta[-1].split(".")
			
			#these counties are named incorrectly in the raw files
			if county == '0Ray':
				county = 'Ray'
			if county == '1870' and 'Ripley' in old_path:
				county = 'Ripley'
			if county == '1860' and 'StLouis' in old_path:
				county = 'StLouis'
			if county == '1860' and 'Callaway' in old_path:
				county == 'Callaway'
			if county == 'VOL1':
				continue
			
			#print(meta)

			file_num = file_num_and_type[0]
			file_type = file_num_and_type[1]
			file_num_length = len(file_num)
			file_num_4 = '0' * (5 - file_num_length) + file_num
			filename = "_".join([state, year[2], county, file_num_4])

			new_path = output_path
			for x in [state, year, county]:
				new_path = new_path + "\\" + x
				if os.path.isdir(new_path) == False:
					os.makedirs(new_path)
			new_path = new_path + "\\"+ filename + "." + file_type
			#shutil.copy(old_path, new_path + "\\"+ filename + "." + file_type)
			format_img(old_path, new_path)
  
	else:
		for key in keys:
			next_path = current_path + "\\" + key
			populate(old_dictionary[key], next_path, output_path)
		#return new_dictionary



def format_img(old_path, new_path):
	with Image(filename = old_path) as img:
		width = img.width
		height = img.height
		if width > height: #this is just a baseline criteria for determining if doc has two pages
			#img.format actually increases bit size
			#img.alpha_channel = False
			img.format = 'jpeg'
			width_one = one_slice * width
			width_two = two_slice * width
			image_one = img[int(width_one):width, 0:height]
			image_two = img[0:int(width_two), 0:height]
			transfer_path = new_path.rsplit("\\", 1)
			#extract file extension
			filename, filetype = os.path.splitext(transfer_path[1])
			image_one.save(filename = transfer_path[0] + "\\" + filename + '_' + '2half' + '.jpg') #we need to check save also take path, not just filename
			image_two.save(filename = transfer_path[0] + "\\" + filename + '_' + '1half' + '.jpg')
		else:
			#img.format actually increases bit size of image
			#img.alpha_channel = False
			img.format = 'jpeg'
			#img.strip()
			#with img.convert('jpeg') as converted:
			file_path, filetype = os.path.splitext(new_path)
			img.save(filename = file_path + ".jpg")
			#shutil.copy(old_path, new_path)


####################################################csv_write and csv_dict have been moved to general code###################################################################
'''
def csv_write(dictionary, package_path):
	keys = list(dictionary.keys())
	for tup in keys:
		csv_list = dictionary[tup]
		filename = package_path + "\\" + 'Missouri' + "\\" + tup[0] + "\\" + tup[1]
		os.makedirs(filename)
		with open(filename + "\\" + 'Package.csv', 'wb') as f:
			writer = csv.writer(f)
			writer.writerow(['State', 'Year', 'File', 'County', 'RA_name', 'bad_cut', 'empty', 'Schedule', 'page_no', 'estab_count', 'line_count', 'legibility', 'totals_incl', 'Notes'])
			for row in csv_list:
				#with open(filename, 'w', newline = '') as f: # Python 2.7 complains with new line arg
				#writer.writerow(['File Name', 'Current path', 'County (if given)'])
				writer.writerow(row)


def csv_dict(current_path, package_path, dictionary):
	if os.path.isdir(current_path) == False: 
		rel_path = os.path.relpath(current_path, output_path) # output_path is a global variable 
		split = rel_path.split("\\")
		state, year, county, file_num = split[0], split[1], split[2], split[3]
		meta = [state, year, file_num, county]

		if (state, year) not in dictionary:
			dictionary[(state, year)] = []
		dictionary[(state, year)].append(meta)
	else:
		folder_contents = os.listdir(current_path)
		for element in folder_contents:
			next_path = current_path + "\\" + element
			csv_dict(next_path, package_path, dictionary)
		return dictionary
'''


'''
#editing this from family scan code
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

'''






######################################################################
if __name__ == '__main__':
	#dictionary = collect(input_path)
	#populate(dictionary, input_path, output_path)
	dictionario = csv_dict(output_path, package_path, {})
	csv_write(dictionario, package_path)
	