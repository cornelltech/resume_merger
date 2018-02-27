
# Filename: PDFBuilder.py
# Description: To create composite PDF files containing the content from 
# a variety of input sources, such as CSV files, TDV (Tab Delimited 
# Values) files, XLS files, etc.

# Author: Vasudev Ram - http://www.dancingbison.com
# Copyright 2012 Vasudev Ram, http://www.dancingbison.com

# This is open source code, released under the New BSD License -
# see http://www.opensource.org/licenses/bsd-license.php .

# ------------------------- imports -------------------------

import sys
import os
import os.path
import string
import csv
from  CSVReader import CSVReader
from  TDVReader import TDVReader
from  PDFWriter import PDFWriter

# ------------------------ class PDFBuilder ----------------

class PDFBuilder:
	"""
	Class to build a composite PDF out of multiple input sources.
	"""

	def __init__(self, pdf_filename, font, font_size, 
				header, footer, input_filenames):
		"""
		PDFBuilder __init__ method.
		"""
		self._pdf_filename = pdf_filename
		self._input_filenames = input_filenames

		# Create a PDFWriter instance
		self._pw = PDFWriter(pdf_filename)
		debug("PDFBuilder.__init__(): Created PDFWriter instance")

		# Set its font
		self._pw.setFont(font, font_size)

		# Set the header and footer for the PDFWriter instance
		self._pw.setHeader(header)
		self._pw.setFooter(footer)
		
	def build_pdf(self, input_filenames):
		"""
		PDFBuilder.build_pdf method.
		Builds the PDF using contents of the given input_filenames.
		"""
		for input_filename in input_filenames:
			# Check if name ends in ".csv", ignoring upper/lower case
			if input_filename[-4:].lower() == ".csv":
				reader = CSVReader(input_filename)
				debug("Created a CSVReader from " + input_filename)
			# Check if name ends in ".csv", ignoring upper/lower case
			elif input_filename[-4:].lower() == ".tdv":
				reader = TDVReader(input_filename)
				debug("Created a TDVReader from " + input_filename)
			else:
				sys.stderr.write("Error: Invalid input file. Exiting\n")
				sys.exit(0)

			debug("Reading from %r" % reader.get_description())
			hdr_str = "Data from reader: " + \
				reader.get_description()
			self._pw.writeLine(hdr_str)
			self._pw.writeLine('-' * len(hdr_str))

			reader.open()
			try:
				while True:
					row = reader.next_row()
					debug("row", row)
					s = ""
					for item in row:
						s = s + item + " "
					debug("s", s)
					self._pw.writeLine(s)
			except StopIteration:
				# Close this reader, save this PDF page, and 
				# start a new one for next reader.
				reader.close()
				self._pw.savePage()
				#continue

	def close(self):
		self._pw.close()

# ------------------------- main() --------------------------

def main():

	# global variables

	# program name for error messages
	global prog_name
	# debug flag - if true, print debug messages, else don't
	global DEBUGGING
	
	# Set the debug flag based on environment variable
	debug_env_var = os.getenv("DEBUG")
	if debug_env_var == "1":
		DEBUGGING = True

	sysargv = sys.argv
	lsa = len(sysargv)

	# Save program filename for error messages
	prog_name = sysargv[0]
	debug("Entered " + prog_name + ":main()")

	# check for right args
	debug("lsa =", lsa)
	if lsa < 2:
		usage()
		debug(prog_name + ": Incorrect number of args, exiting.")
		sys.exit(1)

	# Get output PDF filename from the command line.
	pdf_filename = sys.argv[1]
	debug("PDF filename = ", pdf_filename)

	# Check if -f option given
	if sysargv[2] == '-f' and lsa == 4: 
		# If so, read the input filenames from the file given as 
		# sysargv[3] (the input filenames list)
		input_filenames = []
		with open(sysargv[3], "r") as ifl:
			for fn in ifl:
				input_filenames.append(fn.strip('\n'))
	else:
		# Get the input filenames from the command line.
		input_filenames = sys.argv[2:]

	# Create a PDFBuilder instance.
	pdf_builder = PDFBuilder(pdf_filename, "Courier", 10, 
		"Composite PDF", "Composite PDF", input_filenames)

	# Build the PDF using the inputs.
	pdf_builder.build_pdf(input_filenames)

	pdf_builder.close()

	sys.exit(0)

#------------------------- debug ----------------------------

def debug(msg, *args):

	global DEBUGGING
	if not DEBUGGING:
		return
	sys.stderr.write(msg + ": ")
	sys.stderr.write(repr(args) + "\n")

#------------------------- usage ----------------------------

def usage():
	
	global prog_name
	sys.stderr.write("Usage: python " + prog_name + \
		" pdf_filename input_filename(s)\n" + \
		" OR python " + prog_name + " pdf_filename -f input_filename_list\n" + \
		" where input_filename_list is a file containing input filenames\n")

#------------------------- call main ------------------------

if __name__ == "__main__":
	# Set default value for DEBUGGING, override later in main() 
	# based on value of env. var. DEBUG.
	try:
		DEBUGGING = False
		main()
	except Exception, e:
		sys.stderr.write("Caught an exception: " + e)
		sys.exit(1)


#------------------------- EOF: PDFBuilder.py -----------------

