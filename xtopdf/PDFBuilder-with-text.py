
# Filename: PDFBuilder-with-text.py
# Description: To create composite PDF files containing the content from 
# a variety of input sources, such as CSV files, TDV (Tab Delimited 
# Values) files, XLS files, etc.

# Author: Vasudev Ram - http://www.dancingbison.com
# Copyright 2009-2009 Vasudev Ram, http://www.dancingbison.com

# This is open source code, released under the New BSD License -
# see http://www.opensource.org/licenses/bsd-license.php .

# THIS IS ALPHA CODE FOR DEMO PURPOSES ONLY - USE AT YOUR OWN RISK!

# ------------------------- imports -------------------------

import sys
import os
import os.path
import string
import csv
from  CSVReader import CSVReader
from  TDVReader import TDVReader
from  PDFWriter import PDFWriter

# ------------------------- main() --------------------------

def main():

	# global variables
	global prog_name # program name for error messages
	global DEBUG_FLAG # debug flag - if true, print debug messages, else don't
	
	# Set the debug flag based on environment variable
	DEBUG_FLAG = os.getenv("DEBUG_FLAG")
	if DEBUG_FLAG == None:
		DEBUG_FLAG = 0

	# Save program filename for error messages
	prog_name = sys.argv[0]
	debug("Entered " + prog_name + ":main")

	# check for right args
	debug("len(sys.argv) = ", len(sys.argv))
	if len(sys.argv) != 2:
		usage()
		debug("Incorrect # of args, exiting.")
		sys.exit(1)

	# get output PDF filename
	pdf_filename = sys.argv[1]
	debug("PDF filename = ", pdf_filename)

	# Create a PDFWriter instance
	pw = PDFWriter(pdf_filename)
	# Set its font
	pw.setFont("Courier", 10)
	debug("Created a PDFWriter instance")

	# Set the header and footer for the PDFWriter instance
	pw.setHeader("PDFBuilder.py: Composite PDF creation: " + pdf_filename)
	pw.setFooter("PDFBuilder.py: Composite PDF creation: " + pdf_filename)
	
	# Create the CSVReader instances which are input sources for
	# the composite PDF output.
	csv_reader3 = CSVReader("file3.csv")
	debug("Created a CSVReader from file3.csv")
	csv_reader4 = CSVReader("file4.csv")
	debug("Created a CSVReader from file4.csv")

	# Create the TDVReader instances which are input sources for
	# the composite PDF output.
	tdv_reader2 = TDVReader("file2.tdv")
	debug("Created a TDVReader from file2.tdv")
	tdv_reader3 = TDVReader("file3.tdv")
	debug("Created a TDVReader from file3.tdv")

	for input_source in (csv_reader3, tdv_reader2, csv_reader4, tdv_reader3):
		debug("Using input from %r" % input_source.get_description())
		hdr_str = "Data from input source: " + input_source.get_description()
		pw.writeLine(hdr_str)
		pw.writeLine('-' * len(hdr_str))
		input_source.open()
		try:
			while True:
				row = input_source.next_row()
				debug("row", row)
				s = ""
				for item in row:
					s = s + item + " "
				debug("s", s)
				pw.writeLine(s)
		except StopIteration:
			# Close this input source, save this PDF page and start a 
			# new one for next input source, and continue with next 
			# input source
			input_source.close()
			pw.savePage()
			continue

	# Close the PDFWriter after all input sources are used up.
	pw.close()

	sys.exit(0)

#------------------------- debug ----------------------------

def debug(msg, *args):

	global DEBUG_FLAG
	if not DEBUG_FLAG:
		return
	print msg,
	print args

#------------------------- usage ----------------------------

def usage():
	
	global prog_name
	sys.stderr.write("Usage: python " + prog_name + " pdf_filename\n")

#------------------------- call main ------------------------

if __name__ == "__main__":
	main()

#------------------------- EOF: PDFBuilder-with-text.py -----------------

