from PyPDF2 import PdfFileWriter, PdfFileReader
import os, shutil, sys

input_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\WY\\Input\\Manufacturers Schedule, Census of Wyoming 1880.pdf"
output_path = "D:\\Dropbox (Hornbeck Research)\\MFG Project\\manuscript_database\\WY\\Output"

def split_pdf(input_path, output_path):
	inputpdf = PdfFileReader(open(input_path, "rb"))
	for i in xrange(inputpdf.numPages):
		output = PdfFileWriter()
		output.addPage(inputpdf.getPage(i))
		with open(output_path + "\\" + "WY_8_%s.pdf" % i, "wb") as outputStream:
			output.write(outputStream)



######################################################################
if __name__ == '__main__':
	split_pdf(input_path, output_path)