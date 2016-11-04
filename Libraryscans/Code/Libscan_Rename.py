# exec(open("D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Code\\Libscan_Rename.py").read()) 
import os, shutil, datetime, csv
import xlrd
import ghostscript
from wand.image import Image

one_slice = .4
two_slice = .6

input_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Input\\Scans_via_Library_copy"
excel_path_1 = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Input\\Scans_via_Library_copy\\Batch_1\\Jeremy rolls.xlsx"
excel_path_2 = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\raw_data_copies\\Scans_via_Library\\Batch 2 PDF Files\\Inventory List Invoice 5297.xls"
output_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Output"
temp_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Temp"

test_input = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Input\\Scans_via_Library_copy\\Batch_1\\batch 1 pdf"

states = {'california': 'CA', 'alabama': 'AL', 'colorado': 'CO','connecticut': 'CT', 'delaware': 'DE', 'dc': 'dc', 'florida': 'FL', 'georgia':'GA', 'kentucky': 'KY', 
'illinois': 'IL', 'indiana': 'IN', 'iowa': 'IA', 'kansas':'KS', 'louisiana': 'LA', 'maine': 'ME', 'maryland': 'MD', 'massachusetts': 'MA', 'michigan': 'MI', 
'minnesota': 'MN', 'mississippi': 'MS', 'nebraska':'NE', 'new hampshire': 'NH', 'new jersey': 'NJ', 'new york':'NY', 'north carolina':'NC', 'ohio':'OH', 
'pennsylvania' : 'PA', 'south carolina': 'SC', 'tennessee': 'TN', 'texas': 'TX', 'vermont': 'VT', 'virginia': 'VA', 'washington': 'WA', 'west virginia': 'WV', 
'wisconsin': 'WI'}

remove = ['.dropbox', 'desktop.ini']
no_excel = ['.xls', '.xlsx']
not_for_dir = ['?']

def collect(input_path):
	#base case
	if os.path.isdir(input_path) == False:
		x = 'root'
		#print(x)
		return x
	#recursive case
	else:
		folder_contents = os.listdir(input_path)
		if remove[0] in folder_contents:
			folder_contents = [folder_contents.remove(x) for x in remove]
		#print(folder_contents)
		current_dictionary = {}
		for element in folder_contents:
			#print(element)
			element_strip, element_type = os.path.splitext(input_path + "\\" + element)
			
			if element_type not in no_excel:
				current_path = input_path + "\\" + element
				lower_dictionary = collect(current_path)
				#print(current_path)
				#if lower_dictionary == 'root':
				current_dictionary[element] = lower_dictionary
					#print(element)
		return current_dictionary


def get_info(old_dictionary, current_path, new_dictionary):
	keys = list(old_dictionary.keys())
	#print(keys)
	if 'root' in list(old_dictionary.values()):
		for key in keys:
			#Roll 17 PDF folder in rework batch folder - not sure why it exists; that's why the line is needed
			#if os.path.isdir(current_path + "\\" + key) == False:
				#print(key, 'path:', current_path + "\\" + key)
			old_path = current_path + "\\" + key
			if os.path.isdir(old_path):
				print(old_path)
				next_path = old_path
				get_info(old_dictionary[key], next_path, new_dictionary)
				continue
				#take out Roll from file name
			if "Roll" in key:
				decomp = key.split('Roll', 1)[1]
			else:
				if key == 'DSI Invoice 5301 Inventory.pdf':
					continue
				decomp = key.split('Reel', 1)[1]
			decomp2 = decomp.split('_')
				#print(decomp2)
			roll_num = decomp2[0]
				#take out the type of file from the file number
				#file_num = decomp2[1].split(".")[0]
			file_num = decomp2[1]
				#print(file_num)
			if roll_num not in new_dictionary:
				new_dictionary[roll_num] = {}
			new_dictionary[roll_num][file_num] = old_path    
	else:
		for key in keys:
			next_path = current_path + "\\" + key
			get_info(old_dictionary[key], next_path, new_dictionary)
		return new_dictionary


def populate(new_dictionary, excel_path, csv_sheet, skip_line):
	

	workbook = xlrd.open_workbook(excel_path)
	sheet = workbook.sheet_by_name(csv_sheet)
	#csv_file = open(temp_path + "\\" + 'Sheet1.csv', "w", newline = "") #originally wt, no newline para #apparently py 2.7 doesnt like this
	csv_file = open(temp_path + "\\" + csv_sheet + '.csv', "wb") #originally wt, no newline para
	writer = csv.writer(csv_file)

	for row in list(range(sheet.nrows)):
		#print(sheet.row_values(row))
		writer.writerow(sheet.row_values(row))
	csv_file.close()

	with open(temp_path + "\\" + csv_sheet + '.csv', 'rt') as f:
		file = csv.reader(f)
		#file.__next__() #apparently Py 2.7 doesnt like this
		for x in range(skip_line):
			#print('skipped')
			file.next()
		for row in file:
			#print(row)
			#print(row)
			if row[0] == '':
				print('Process Complete')
				return
			roll_num, State, County, Date = int(float(row[0])), row[2].lower(), row[3], row[4]
			if State == 'kansas territory':
				State = 'kansas'
			Date = Date.split(".")[0]

			dir_list = [State, Date, County]
			for i in range(len(dir_list)):
				for j in not_for_dir:
					if dir_list[i].endswith(j):
						#print(j)
						dir_list[i] = 'Unknown'
			#new_dir = output_path
			
			#for i in dir_list:
				#new_dir = new_dir + "\\" + i 
				
				#if os.path.isdir(new_dir) == False:
					#try:
						#os.makedirs(new_dir)
					#except FileNotFoundError:
						#print("\nOh man, you have a file not found error (race condition)\n")
			
			if str(roll_num) in list(new_dictionary.keys()):
				#print(keys)
				keys = list(new_dictionary[str(roll_num)].keys())
				new_dir = output_path
				for i in dir_list:
					new_dir = new_dir + "\\" + i 
				
					if os.path.isdir(new_dir) == False:
						try:
							os.makedirs(new_dir)
						except FileNotFoundError:
							print("\nOh man, you have a file not found error (race condition)\n")
				for key in keys:
					old_path = new_dictionary[str(roll_num)][key]
					#print(old_path)
					new_path = new_dir + "\\" + "_".join([states[State], Date, key])
					#print('old path:\n', old_path, 'new_path\n', new_path)
					
					#shutil.copy(old_path, new_path)
					format_img(old_path, new_path)


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
			writer.writerow(['County', 'File Number', 'Current Location'])
			for row in csv_list:
				#with open(filename, 'w', newline = '') as f: # Python 2.7 complains with new line arg
				#writer.writerow(['File Name', 'Current path', 'County (if given)'])
				writer.writerow(row)


def csv_dict(current_path, package_path, dictionary):
	if os.path.isdir(current_path) == False: 
		rel_path = os.path.relpath(current_path, output_path) # output_path is a global variable 
		split = rel_path.split("\\")
		state, year, county, file_num = split[0], split[1], split[2], split[3]
		meta = [county, file_num, current_path]

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

######################################################################
if __name__ == '__main__':
	dictionary = collect(input_path)
	new_dictionary = get_info(dictionary, input_path, {})
	#print(dictionary, new_dictionary)
	#populate(new_dictionary, excel_path_1, 'Sheet1', 1)
	populate(new_dictionary, excel_path_2, 'Sheet1', 3)



