import os, shutil, datetime, sys
import csv, wand

from wand.image import Image 

ancestry_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Output"
ancestry_output_final = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\ancestry\\Output_final"

MO_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Output"
MO_output_final = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\MO\\Output_final"

lib_scan_output = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Output"
lib_scan_output_final = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\LibraryScans\\Output_final"

test = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\General\\Make_csv_rename_test"

package_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\General\\Packages"

remove = ['desktop.ini', '.dropbox']
output_path_list = [ancestry_output, MO_output, lib_scan_output]
output_path_final_list = [ancestry_output_final, MO_output_final, lib_scan_output_final]
package_list = ['Ancestry', 'MO', 'Library_Scans']
file_stamp = ['A', 'S', 'L']

csv_header = ['State', 'Year', 'File', 'County', 'RA_name', 'bad_cut', 'empty', 'Schedule', 'page_no', 'estab_count', 'line_count', 'legibility', 'totals_incl', 'Notes']



def csv_write(dictionary, package_path, source):
	keys = list(dictionary.keys())
	for tup in keys:
		csv_list = dictionary[tup]
		filename = package_path + "\\" + source + "\\" + tup[0] + "\\" + tup[1]
		os.makedirs(filename)
		with open(filename + "\\" + 'Package.csv', 'wb') as f:
			writer = csv.writer(f)
			writer.writerow(csv_header)
			for row in csv_list:
				#with open(filename, 'w', newline = '') as f: # Python 2.7 complains with new line arg
				#writer.writerow(['File Name', 'Current path', 'County (if given)'])
				writer.writerow(row)


def csv_dict(current_path, output_path, dictionary):
	if os.path.isdir(current_path) == False: 
		rel_path = os.path.relpath(current_path, output_path) # output_path is a global variable 
		split = rel_path.split("\\")
		#print(split)
		if len(split) <= 2:
			pass
		else:
			if len(split) == 3:
				state, year, file_num = split[0], split[1], split[2]
				meta = [state, year, file_num]
			elif len(split) ==4:
				state, year, county, file_num = split[0], split[1], split[2], split[3]
				meta = [state, year, file_num, county]

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
	if '.dropbox' in output_path or 'desktop.ini' in output_path:
		pass
	elif os.path.isdir(output_path) == False:
		filename, filetype = os.path.splitext(output_path)
		new_name = filename + "_" + stamp + filetype
		if filename.endswith("_" + stamp) == False:
			#print(output_path)
			os.rename(output_path, new_name)
	else: 
		folder_contents = os.listdir(output_path)
		for element in folder_contents:
			next_path = output_path + "\\" + element
			rename(next_path, stamp)

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



######################################################################
if __name__ == '__main__':
	#dictionario = csv_dict(test, test, {})
	#csv_write(dictionario, package_path, 'test')
	#rename(test, 'T')	
	
	for i in range(len(package_list)):
		#dictionario = csv_dict(output_path_list[i], output_path_list[i], {})
		#csv_write(dictionario, package_path, package_list[i])
		#rename(output_path_list[i], file_stamp[i])
		no_county_folder(output_path_list[i], output_path_list[i], output_path_final_list[i])
		print(package_list[i], 'complete')
	
