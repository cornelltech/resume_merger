
# Filename: CSVReader.py
# Author: Vasudev Ram - http://www.dancingbison.com
# Copyright 2012-2012 Vasudev Ram, http://www.dancingbison.com
# This is open source code, released under the New BSD License -
# see http://www.opensource.org/licenses/bsd-license.php .

# Description: Defines a class, CSVReader, that lets its user open a 
# CSV file, read its values row by row, and close it. Implements the 
# uniform interface consisting of the following methods:

# - open()
# - next_row()
# - close()

# This uniform interface is meant to be implemented by various
# classes such as CSVReader, TDVReader, XLSReader, etc., that represent 
# input sources that can be used to create composite PDFs.
# The reason for implementing this uniform interface is that it allows
# these classes to be used polymorphically, using the same
# sequence of open(), next_row() (called in a loop), and close(),
# to simplify and make uniform, the code needed to create a 
# composite PDF from a disparate collection of input sources.

# ------------------------- imports -------------------------

import sys
import os
import os.path
import string
import csv

#------------------------- debug ----------------------------

def debug(msg, *args):

	global DEBUG_FLAG
	if not DEBUG_FLAG:
		return
	print msg,
	print args

# ------------------------- class VR_Excel  -----------------

class VR_Excel:
	"""
	VR_Excel class. Defines the dialect settings that I want 
	for reading CSV files. Has some values changed from the 
	default 'class excel' example given in the csv module docs.
	See http://docs.python.org/library/csv.html#csv.excel
	and the output from:
	    import csv
		print csv.__doc__
	(look under the section "DIALECT REGISTRATION:")
	Changes:
	 - I use skipinitialspaces = True
	 - I use quoting = csv.QUOTE_MINIMAL
	 Was getting extra layer of quotes and some extra whitespace
	 without the above settings.
	"""
	delimiter = ','
	quotechar = '"'
	escapechar = None
	doublequote = True
	skipinitialspace = True
	lineterminator = '\r\n'
	quoting = csv.QUOTE_MINIMAL

# ------------------------- class CSVReader -----------------

class CSVReader:

	def __init__(self, csv_filename):
		"""
		Constructor for CSVReader class.
		"""
		self.__csv_filename = csv_filename

	def get_description(self):
		"""
		Return a description of the CSVReader that is meaningful 
		to humans
		"""
		return "CSV file: " + self.__csv_filename

	def open(self):
		"""
		CSVReader.open() method.
		Opens the csv_filename for reading.
		Creates a csv.reader from the open file object,
		and saves it as a member variable of the instance.
		"""

		# open input CSV file and save the file object.
		try:
			self.__csv_fil = open(self.__csv_filename, "rb")
		except IOError:
			sys.stderr.write(sys.argv[0] + ": Could not open input CSV file " + \
			self.__csv_filename + ". Check filename for existence, spelling or permissions. Terminating.\n")
			sys.exit(1)
		#debug("self.csv_filename = " + self.__csv_filename)
		print"self.csv_filename = %s" % self.__csv_filename

		# Create instance of class VR_Excel to specify the CSV 
		# dialect to use for the reader.
		vr_excel = VR_Excel()
		# Create csv.reader object from the file object.
		self.__csv_reader = csv.reader(self.__csv_fil, vr_excel)
		#debug("Created a csv.reader instance")
		print "Created a csv.reader instance"

	def next_row(self):
		"""
		CSVReader.next_row() method.
		Returns the result of calling the csv.reader's next() method.
		Throws a StopIteration when the csv.reader's next() does.
		"""
		return self.__csv_reader.next()

	def print_rows(self):
		"""
		CSVReader.print_rows() method. Utility method for debugging.
		Prints all rows of the csv.reader instance. Returns when 
		that instance throws a StopIteration.
		"""
		try:
			for row in self.__csv_reader:
				#debug("row", row)
				#print "row = %r" % row
				s = ""
				for item in row:
					s = s + item + " "
				#debug("s", s)
				print "s = %s" % s
		except StopIteration:
			return

	def close(self):
		"""
		CSVReader.close() method.
		Closes the underlying CSV file object.
		"""
		try:
			self.__csv_fil.close()
		except IOError:
			sys.stderr.write(sys.argv[0] + ": Could not close input CSV file " + \
			self.__csv_filename + ". Terminating.\n")
			sys.exit(1)

# ------------------------- main() --------------------------

def main():

	# global variables
	global prog_name # program name for error messages
	global DEBUG_FLAG # debug flag - if true, print debug messages, else don't
	
	# Set the debug flag based on environment variable named DEBUG_FLAG.
	# (Set DEBUG_FLAG=1 at the command prompt before running this program
	# if you want debug output. Use:
	# SET DEBUG_FLAG=1
	# on Windows, and:
	# export DEBUG_FLAG=1
	# on Linux (if using bash shell)
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

	# get input CSV filename
	csv_filename = sys.argv[1]
	debug("CSV filename = ", csv_filename)

	# Create a CSVReader instance using the input CSV filename
	csv_reader = CSVReader(csv_filename)
	debug("csv_reader.__dict__ = ", csv_reader.__dict__)

	# Open the CSVReader instance
	csv_reader.open()
	# Print all its rows
	debug("Before loop to read rows from " + csv_reader.get_description())
	csv_reader.print_rows()
	debug("After loop to read rows")
	# Close the CSVReader instance
	csv_reader.close()

	sys.exit(0)

#------------------------- usage ----------------------------

def usage():
	
	global prog_name
	sys.stderr.write("Usage: python " + prog_name + " csv_filename\n")

#------------------------- call main ------------------------

if __name__ == "__main__":
	main()

#------------------------- EOF: CSVReader.py -----------------

