# This python file will take ancestry files and incorporate their meta-data into their file names. 
# The new files are outputed to the "out" folder in ancestry

# exec(open("D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Code\\Rename_File_Prelim.py").read())
# my execute: exec(open("./filename").read())
#One issue in the ancestry data is California - it is iiregular in its org - it has an industry foler, and a not stated folder for some counties (Los Angeles). 
#it might be easier to fix this manually

#Run time: < 1 s



import os, shutil, datetime, sys
import csv, wand
#sys.path.insert(0, "C:\\Program Files\\ImageMagick-7.0.3-Q16")
from wand.image import Image #once Wand is installed on both computers


one_slice = .4
two_slice = .6

input_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\Input\\ancestry_downloads_copy"
output_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Output"

test_input = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Input\\ancestry_downloads_copy\\california\\industry\\1850\\el dorado"
test_input_2 = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Input\\ancestry_downloads_copy\\iowa\\1850\\Appanoose"
package_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\General\\Packages"
#my_path = "\\Users\\Adam\\Pictures\\rho_0.9.png"
states = {'california': 'CA', 'iowa': 'IA', 'maine':  'ME', 'massachusetts': 'MA', 'nebraska': 'NE', 'new york': 'NY', 'south carolina': 'SC', 'virginia': 'VA'}
remove = ['coding_example', 'renamed_copies', 'rename_CA - (not working copy)', 'rename_CA', 'rename_IA', 'rename_template', 'readme.rtf', '_checks']

#a recursive stratregy is best
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
		#print(folder_contents)
		#return
		if remove[-1] in folder_contents:
			#print(folder_contents)
			for x in remove:
				if x in folder_contents:
					folder_contents.remove(x)
		current_dictionary = {}
		for element in folder_contents:
			current_path = input_path + "\\" + element
			lower_dictionary = collect(current_path)
			current_dictionary[element] = lower_dictionary
		return current_dictionary
			

def populate(dictionary, current_path):
	keys = list(dictionary.keys())
	#print(keys)
	#print('current path:\n', current_path)
	#for key in keys:
	if 'root' in list(dictionary.values()):
		for key in keys:
			rel_path = os.path.relpath(current_path, input_path)
			old_path = current_path + "\\" + key
			if os.path.isdir(old_path):
				print(old_path)
				next_path = old_path
				populate(dictionary[key], next_path)
				continue
			file_list = rel_path.split("\\")
			file_list.append(key)
			
			#print(file_list)
			#California exception - eliminate township and Industry folder for consistency
			state = file_list[0].lower()
			if state == 'california':
				file_list.pop(1)
				file_list.pop(3)
			
			county = file_list[2]
			year = file_list[1][2]		
			file_num = file_list[3]

			new_dir = output_path 
			for i in [state, file_list[1], county]:
				new_dir = new_dir + "\\" + i
				if os.path.isdir(new_dir) == False:
					os.makedirs(new_dir)

			#Maine also has quirks
			if state == 'maine':
				file_num = file_list[-1]

			#another maine idiosyncracy -- see 1880 sagadohoc, 
			if '-' in file_num:
				file_num_final = file_num.split("-")
			else:
				file_num_final = file_num
			#try:
			file = "_".join([states[state], year, county, file_num_final[1]])
			#except IndexError:
				#print(file_list)
				#return
			#print(file)
			
			new_path = new_dir + "\\" + file


			#other normal: "D:\Dropbox (Hornbeck Research)\MFG Project\manuscript_database\ancestry\Input\ancestry_downloads_copy\massachusetts\1870\Bristol\Acushnet_31644_217903-00085.jpg"
			# when time, add a line preventing duplicated from being transferred twice e.g if already there, don't shutil
			#print(old_path, '\n', new_path)
			format_img(old_path, new_path)
			#shutil.copy(old_path, new_path)
	else:
		for key in keys:
			next_path = current_path + "\\" + key
			rel_path = os.path.relpath(next_path, input_path)
			new_dir = output_path + "\\" + rel_path
			#if os.path.isdir(next_path) and os.path.isdir(new_dir) == False:
			#	os.makedirs(new_dir)
			if os.path.isdir(next_path):
				populate(dictionary[key], next_path)




def format_img(old_path, new_path):
	with Image(filename = old_path) as img:
		width = img.width
		height = img.height
		if width > height: #this is just a baseline criteria for determining if doc has two pages
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
			img.format = 'jpeg'
			file_path, filetype = os.path.splitext(new_path)
			img.save(filename = file_path + '.jpg')
			#shutil.copy(old_path, new_path)

####################################################csv_write and csv_dict have been moved to general code###################################################################

'''
def csv_write(dictionary, package_path):
	keys = list(dictionary.keys())
	for tup in keys:
		csv_list = dictionary[tup]
		filename = package_path + "\\" + 'Ancestry' + "\\" + tup[0] + "\\" + tup[1]
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
def csv_package(current_path, package_path):
	if os.path.isdir(current_path) == False: 
		rel_path = os.path.relpath(current_path, output_path) # output_path is a global variable 
		split = rel_path.split("\\")
		state, year, county, file_num = split[0], split[1], split[2], split[3]
		meta = [state, year, county, file_num, current_path]

		package_output_path = package_path
		for x in ['Ancestry', state, year]:
			package_output_path = package_output_path + "\\" + x
			if os.path.isdir(package_output_path) == False:
				os.makedirs(package_output_path)
		
		package_output_path = package_output_path + ".csv"
		csv_write(meta, package_output_path)



	else:
		folder_contents = os.listdir(current_path)
		for element in folder_contents:
			next_path = current_path + "\\" + element
			csv_package(next_path, package_path)


'''

######################################################################
if __name__ == '__main__':
	#dictionary = collect(input_path)
	#populate(dictionary, input_path)
	dictionario = csv_dict(output_path, package_path, {})
	csv_write(dictionario, package_path)





