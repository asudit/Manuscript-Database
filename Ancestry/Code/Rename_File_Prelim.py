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
from PIL import Image

one_slice = .4
two_slice = .6
threshold = .08

input_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\Input\\ancestry_downloads_copy"
output_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Output_final"
regenerate_output_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Regenerate_output"
metadata_csv = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Temp\\NE_7_A_metadata.csv"
#"D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Temp\\IA_8_A_metadata.csv"

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
			

def populate(dictionary, current_path, regenerate, bad_cut_list, empty_list):
	keys = list(dictionary.keys())

	if 'root' in list(dictionary.values()):
		for key in keys:
			rel_path = os.path.relpath(current_path, input_path)
			old_path = current_path + "\\" + key
			if os.path.isdir(old_path):
				#print(old_path)
				next_path = old_path
				populate(dictionary[key], next_path, regenerate, bad_cut_list, empty_list)
				continue
			file_list = rel_path.split("\\")
			file_list.append(key)
			#print(file_list)
			
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
			for i in [state, file_list[1]]:
				new_dir = new_dir + "\\" + i
				if os.path.isdir(new_dir) == False:
					os.makedirs(new_dir)

			#Maine also has quirks
			if state == 'maine':
				file_num = file_list[-1]

			#This is important -- all the file numbers are the same for a county, year file, only the number after - is different
			if '-' in file_num:
				file_num_final = file_num.split("-")
			else:
				file_num_final = file_num
			
			file = "_".join([states[state], year, county, file_num_final[1]])
			new_path = new_dir + "\\" + file

			#this is to do regeneration as needed
			if regenerate:
				#print('regenerating')
				bad_cut(old_path, new_path, file, state, file_list[1], bad_cut_list, empty_list, "_A")
				continue


			#11/21/16 Just want NE 1880; adding if statement:
			#if states[state] == 'NE' and year == '8':
				#img = Image.open(old_path)
				#file_path, filetype = os.path.splitext(new_path)
				#if os.path.isfile(file_path + "_A" + '.jpg') == False:
				#img.save(file_path + "_A" + '.jpg')
			#11/21/16 Just want NE 1880; commenting out format_img
			format_img(old_path, new_path)
			
	else:
		for key in keys:
			next_path = current_path + "\\" + key
			rel_path = os.path.relpath(next_path, input_path)
			new_dir = output_path + "\\" + rel_path
			#if os.path.isdir(next_path) and os.path.isdir(new_dir) == False:
			#	os.makedirs(new_dir)
			if os.path.isdir(next_path):
				populate(dictionary[key], next_path, regenerate, bad_cut_list, empty_list)


def read_metadata(metadata_csv):
	bad_cut_list = []
	empty_list = []
	bad_cut = 5
	empty = 6
	file = 2
	with open(metadata_csv, 'rt') as f:
		rows = csv.reader(f)
		rows.next()
		for row in rows:
			if row[bad_cut] == '1':
				bad_cut_list.append(row[file])
			if row[empty] != "":
				empty_list.append(row[file])
	return bad_cut_list, empty_list




def bad_cut(old_path, new_path, filename, state, year, bad_cut_list, empty_list, underscore_stamp):
	transfer_path = new_path.rsplit("\\", 1)
	#for two halfs, in case of splitting 
	filename, filetype = os.path.splitext(transfer_path[1])
	regenerate_path = regenerate_output_path + "\\" + state + "\\" + year + "\\" + transfer_path[1]
	if os.path.isdir(regenerate_output_path + "\\" + state + "\\" + year) == False:
		os.makedirs(regenerate_output_path + "\\" + state + "\\" + year)
	
	#why two of everything? because the files in the csv have no stamp, but the actuall file
	#in the output folder does
	new_file0_stamped = filename + underscore_stamp + '.jpg'
	new_file0 = filename + '.jpg'
	new_file1_stamped = filename + "_" + '1half' + underscore_stamp + '.jpg'
	new_file1 = filename + "_" + '1half' + '.jpg'
	new_file2_stamped = filename + "_" + '2half' + underscore_stamp + '.jpg'
	new_file2 = filename + "_" + '2half' + '.jpg'
	#if 'IA' in filename and '8' in filename:
	#print(new_file1)

	for i in [(new_file1, new_file1_stamped), (new_file2, new_file2_stamped)]:
		if i[0] in bad_cut_list:
			#make list of bad files shorter once processes
			
			bad_cut_list.remove(i[0])
			#delete file from output folder
			if os.path.isfile(transfer_path[0] + "\\" + i[1]):
				os.remove(transfer_path[0] + "\\" + i[1])
			#print('Delete bad cuts file:\n\n',transfer_path[0] + "\\" + i[1])
		#regenerate in main output folder
		
		format_img(old_path, new_path)
		
		#regenerate in regenerate output folder to make packaging easier
		
		format_img(old_path, regenerate_path)
		#print('New output folder too:\n\n', regenerate_path)
	if new_file1 in empty_list:  
		for i in [new_file1_stamped, new_file2_stamped]:
			file, filetype = os.path.splitext(i)
			if os.path.isfile(transfer_path[0] + "\\" + i):
				os.rename(transfer_path[0] + "\\" + i, transfer_path[0] + "\\" + file + "_" + 'W' + filetype)
			#print('Chnaging empty half from:\n', transfer_path[0] + "\\" + i, 'to:\n', transfer_path[0] + "\\" + file + "_" + 'W' + filetype)

	if new_file0 in empty_list:
		file, filetype = os.path.splitext(new_file0_stamped)
		print(transfer_path[0] + "\\" + new_file0_stamped)
		if os.path.isfile(transfer_path[0] + "\\" + new_file0_stamped):
			os.rename(transfer_path[0] + "\\" + new_file0_stamped, transfer_path[0] + "\\" + file + "_" + 'W' + filetype)
		#print('Changing empty sheet name from :\n\n', transfer_path[0] + "\\" + new_file0_stamped, 'to blank label:', transfer_path[0] + "\\" + file + "_" + 'W' + filetype)
		#complex because could be all three empty

		#note --  you also want to regenerate a copy into a separate folder so that they can easily go through it e.g. regenerate one
		#for output final or whatever and one for a folder next to it called regenerate or whatever


def format_img(old_path, new_path):
	img = Image.open(old_path)
	width, height  = img.size
	if width > height and abs(float(width - height))/float(height) > threshold:
		transfer_path = new_path.rsplit("\\", 1)
		filename, filetype = os.path.splitext(transfer_path[1])

		width_one = one_slice * width
		width_two = two_slice * width
		image_one, image_two = img, img
		if os.path.isfile(transfer_path[0] + "\\" + filename + '_' + '2half' + '.jpg') == False:
			image_one.crop((int(width_one), 0, width, height)).save(transfer_path[0] + "\\" + filename + '_' + '2half' + "_A" + '.jpg')
			image_two.crop((0, 0, int(width_two), height)).save(transfer_path[0] + "\\" + filename + '_' + '1half' + "_A" + '.jpg')
	else: 
		file_path, filetype = os.path.splitext(new_path)
		if os.path.isfile(file_path + "_A" + '.jpg') == False:
			img.save(file_path + "_A" + '.jpg')

####################################################csv_write and csv_dict have been moved to general code###################################################################


######################################################################
if __name__ == '__main__':
	dictionary = collect(input_path)
	print(list(dictionary.keys()))
	bad_cut_list, empty_list = read_metadata(metadata_csv)
	print(bad_cut_list)
	print(empty_list)
	populate(dictionary, input_path, True, bad_cut_list, empty_list)
	#dictionario = csv_dict(output_path, package_path, {})
	#csv_write(dictionario, package_path)





