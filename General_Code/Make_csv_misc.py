import os, shutil, datetime, sys
import csv, wand

#from wand.image import Image 
from PIL import Image

shrink_factor = .2
quality_factor = 65

ancestry_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Output"
ancestry_output_final = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Output_final"

MO_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Output"
MO_output_final = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Output_final"

lib_scan_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Output"
lib_scan_output_final = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Output_final"
lib_scan_output_tiff = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Output_tiff"
#MN_1850 = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Output_pdf_incomplete\\minnesota"
NH_rename_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Output_tiff\\new hampshire\\1870_rename"
Famsearch_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\Familysearch\\Output_final"
Nara_texas_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\Nara_texas\\Output"

test = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\General\\Make_csv_rename_test"
package_test = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Output_tiff\\alabama"

package_folder = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\General\\metadata_collection"

remove = ['desktop.ini', '.dropbox']
output_path_list = [ancestry_output, MO_output, lib_scan_output]
output_path_final_list = [ancestry_output_final, MO_output_final, lib_scan_output_final]
package_list = ['Ancestry', 'MO', 'Library_Scans']
file_stamp = ['A', 'S', 'L']

states = {'california': 'CA', 'alabama': 'AL', 'arkansas': 'AR', 'colorado': 'CO','connecticut': 'CT', 'delaware': 'DE', 'dc': 'dc', 'florida': 'FL', 'georgia':'GA', 'kentucky': 'KY', 
'illinois': 'IL', 'indiana': 'IN', 'iowa': 'IA', 'kansas':'KS', 'louisiana': 'LA', 'maine': 'ME', 'maryland': 'MD', 'massachusetts': 'MA', 'michigan': 'MI', 
'minnesota': 'MN', 'mississippi': 'MS', 'montana': 'MT','nebraska':'NE', 'new hampshire': 'NH', 'new jersey': 'NJ', 'new york':'NY', 'north carolina':'NC', 'ohio':'OH', 
'pennsylvania' : 'PA', 'south carolina': 'SC', 'tennessee': 'TN', 'texas': 'TX', 'vermont': 'VT', 'virginia': 'VA', 'washington': 'WA', 'west virginia': 'WV', 
'wisconsin': 'WI'}

csv_header = ['State', 'Year', 'File', 'County', 'RA_name', 'bad_cut', 'empty', 'Schedule', 'page_no', 'estab_count', 'legibility', 'totals_incl', 'Notes']



def csv_write(dictionary, package_folder, stamp):
	'''
	This function takes a dictionary from csv_dict function, a desired output
	folder in the metadata collection folder, and a stamp, which is a letter code indicating
	the source of the files
	'''

	keys = list(dictionary.keys())
	#print(keys)
	for tup in keys:
		state, year = tup[0], tup[1]
		#print(state, year)
		csv_list = dictionary[tup]
		csv_folder = package_folder + "\\" + 'Csv_Folder'
		
		if os.path.isdir(csv_folder) == False:
			os.makedirs(csv_folder)
		csv_file = csv_folder + "\\" + "_".join([state, year, stamp, 'metadata.csv'])
		#print('hey!',csv_folder)
		#print(csv_file, state)
		if os.path.isfile(csv_file):
			os.remove(csv_file)
		with open(csv_file, 'wb') as f:
			writer = csv.writer(f)
			writer.writerow(csv_header)
			for row in csv_list:
				#print(row)
				#with open(filename, 'w', newline = '') as f: # Python 2.7 complains with new line arg
				#writer.writerow(['File Name', 'Current path', 'County (if given)'])
				writer.writerow(row)


def csv_dict(current_path, output_path, dictionary):
	'''
	This function takes a year-state folder with files, which is intended to be
	packaged into the metadata collection folder. Note that current path and output path are the same folder,
	when the function is called initially. Dictionary is an empty dictionary
	'''
	

	if os.path.isdir(current_path) == False: 
		#print(current_path)
		#just Nara
		#rel_path = os.path.relpath(current_path, output_path) # output_path is a global variable 
		#state = 'TX'
		#year = '8'
		#meta = [state, year, rel_path]
			#
		#if state != 'Csv':
			#if (state, year) not in dictionary:
				#dictionary[(state, year)] = []
			#dictionary[(state, year)].append(meta)
		#just Nara
		
		#print(rel_path)
		split = rel_path.split("_")
		#print(split)
		if len(split) <= 2:
			pass
		else:
			if len(split) == 3:
				state, year, file_num = split[0], split[1], split[2]
				meta = [state, year, file_num]
				#print(meta)
			elif len(split) >= 4:
				state, year, county = split[0], split[1], split[2]
				meta = [state, year, rel_path, county]

				#print(meta)
			
			
			if state != 'Csv':
				if (state, year) not in dictionary:
					dictionary[(state, year)] = []
				dictionary[(state, year)].append(meta)
				
	else:
		folder_contents = os.listdir(current_path)
		for element in folder_contents:
			next_path = current_path + "\\" + element
			csv_dict(next_path, output_path, dictionary)
		return dictionary


def rename(output_path, stamp):
	'''
	This function will "stamp" every file in the folder that is passed in as the output_path parameter.
	By stamp, I mean append a one letter code indicating the source of the file to the filename of every file
	'''

	if '.dropbox' in output_path or 'desktop.ini' in output_path:
		pass
	elif os.path.isdir(output_path) == False:
		filename, filetype = os.path.splitext(output_path)
		new_name = filename + "_" + stamp + filetype
		if os.path.isfile(new_name) and os.path.isfile(output_path):
			os.remove(output_path)
		elif filename.endswith("_" + stamp) == False:
			print('old: %s new: %s', output_path, new_name)
			os.rename(output_path, new_name)
	else: 
		folder_contents = os.listdir(output_path)
		for element in folder_contents:
			next_path = output_path + "\\" + element
			rename(next_path, stamp)

def rename_NH(input_path, county, year):
	files = os.listdir(input_path)
	for file in files:
		old_dir = input_path + "\\" + file
		#print(old_dir)
		meta = file.split("_")
		#print(meta)
		if len(meta) == 6:
			new_file = "_".join(['NH', year, county, meta[-3], meta[-2], meta[-1]])
		else:
			new_file = "_".join(['NH', year, county, meta[-2], meta[-1]])
		new_dir = input_path + "\\" + new_file
		#print(old_dir, new_dir, '\n')
		if old_dir != new_dir:
			os.rename(old_dir, new_dir)


# :( :( :(
def no_county_folder(current_path, input_path, output_path_final):
	if '.dropbox' in current_path or 'desktop' in current_path:
		pass
	elif os.path.isdir(current_path) == False:
		rel_path = os.path.relpath(current_path, input_path)
		meta = rel_path.split("\\")
		#print(meta)
		state, year, file = meta[0], meta[1], meta[-1]

		new_path = output_path_final
		for i in [state, year]:
			new_path = new_path + "\\" + i
			if os.path.isdir(new_path) == False:
					os.makedirs(new_path)

		new_path = new_path + "\\" + file
		if os.path.isfile(new_path) == False:
			#print(current_path)
			shutil.copy(current_path, new_path)
	else:
		folder_contents = os.listdir(current_path)
		for x in remove:
			if x in folder_contents:
				folder_contents.remove(x)
		for element in folder_contents:
			next_path = current_path + "\\" + element
			no_county_folder(next_path, input_path, output_path_final)

def package(input_path, current_path, output_path, stamp):
	'''
	This function is intended to take a general output folder for some file source as input, 
	and output a prepared package into the metadata collection folder. Usually, input_path will be an output folder
	in one of the source folders in manuscript database folder, like output_tiff or output_final. Input_path=current_path when func is called
	Output_path is usally the metadata collection folder
	'''
	if os.path.isdir(current_path) == False:
		rel_path = os.path.relpath(current_path, input_path) 
		
		file = rel_path.split("\\")
		
		meta = file[1].split("_")
		state, year = meta[0], meta[1]
		#just for NARA
		#state = 'TX'
		#year = '1880'
		package_folder = output_path + "\\" + state + year + "_" + stamp
		if os.path.isdir(package_folder) == False:
			os.makedirs(package_folder)
		
		new_path = package_folder + "\\" + file[1]
		#for Nara
		#new_path = package_folder + "\\" + file[0]
		if os.path.isfile(new_path) == False:
			file_obj = Image.open(current_path)
			width, height = file_obj.width, file_obj.height
			#print(current_path)
			file_obj = file_obj.resize((int(width * shrink_factor), int(height * shrink_factor)), Image.ANTIALIAS)
			file_obj.save(package_folder + "\\" + file[1], optimize = True, quality = quality_factor)
			#for NARA
			#file_obj.save(package_folder + "\\" + file[0], optimize = True, quality = quality_factor)
	else: 
		folder_contents = os.listdir(current_path)
		#print(current_path)
		for key in folder_contents:
			next_path = current_path + "\\" + key
			package(input_path, next_path, output_path, stamp)
		#dictionario = csv_dict(input_path, input_path, {})
		#csv_write(dictionario, output_path, stamp)





######################################################################
if __name__ == '__main__':
	
	package(Famsearch_output, Famsearch_output, package_folder, 'F')

	folder_list = os.listdir(package_folder)
	for i in range(len(folder_list)):
		if folder_list[i].endswith('F'):
			input_path = package_folder + "\\" + folder_list[i]
			dictionario = csv_dict(input_path, input_path, {})
			csv_write(dictionario, input_path, 'F')
	

		

	
