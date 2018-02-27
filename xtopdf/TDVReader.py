
# Filename: TDVReader.py
# Author: Vasudev Ram - http://www.dancingbison.com
# Copyright 2012-2012 Vasudev Ram, http://www.dancingbison.com
# This is open source code, released under the New BSD License -
# see http://www.opensource.org/licenses/bsd-license.php .

# Description: Defines a class, TDVReader, that lets its user open a 
# TDV (Tab Delimited Values) file, read its values row by row, and 
# close it. Implements the uniform interface consisting of the following 
# methods:

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

#------------------------- imports --------------------------

import sys
import os
import os.path
import string

#------------------------- debug ----------------------------

def debug(msg, *args):

	global DEBUG_FLAG
	if not DEBUG_FLAG:
		return
	something_was_printed = False
	if msg:
		print msg,
		something_was_printed = True
	if args:
		print args
		something_was_printed = True
	# Add a last newline if something was printed above. Otherwise
	# next non-debug output comes on same line as debug output, in
	# the case when args is None.
	if something_was_printed:
		print

# ------------------------- class TDVReader -----------------

class TDVReader:

	def __init__(self, tdv_filename):
		"""
		Constructor for TDVReader class.
		"""
		self.__tdv_filename = tdv_filename

	def get_description(self):
		"""
		Return a description of the TDVReader that is meaningful 
		to humans
		"""
		return "TDV file: " + self.__tdv_filename

	def open(self):
		"""
		TDVReader.open() method.
		Opens the tdv_filename for reading.
		Saves the open file object as a member variable of the instance.
		"""

		# open input TDV file and save the file object as an instance field.
		try:
			self.__tdv_fil = open(self.__tdv_filename, "rb")
		except IOError:
			sys.stderr.write(sys.argv[0] + ": Could not open input TDV file " + \
			self.__tdv_filename + ". Check filename for existence, spelling or permissions. Terminating.\n")
			sys.exit(1)
		#debug("self.tdv_filename = " + self.__tdv_filename)
		print"self.tdv_filename = %s" % self.__tdv_filename

	def next_row(self):
		"""
		TDV.next_row() method.
		Reads the next line from the TDV file.
		Throws a StopIteration if at EOF of the TDV file.
		Else (if not EOF):
		[ Removes the trailing newline if present.
		Splits the line by tab delimiter and returns a list of
		tab-delimited values from the line.
		]
		"""
		lin = self.__tdv_fil.readline()
		if len(lin) == 0:
			raise StopIteration
		# Remove the trailing newline (\n = ASCII 10 decimal)
		if lin[-1] == '\n':
			lin = lin[:-1]
		# This is needed if (and only) on Windows due to it's CR+LF newline 
		# convention: if there is still a trailing carriage return 
		# (\r = ASCII 13 decimal), remove it.
		if len(lin) > 0:
			if lin[-1] == '\r':
				lin = lin[:-1]
		lis = lin.split("\t")
		return lis

	def print_rows(self):
		"""
		TDV.print_rows() method. Utility method for debugging.
		Prints all rows of the TDV file, by calling self.next_row(). 
		Returns when next_row() throws a StopIteration.
		"""
		try:
			while True:
				row = self.next_row()
				#debug("row", row)
				print "row = %r" % row
				s = ""
				for item in row:
					s = s + item + " "
				#debug("s", s)
				print "s = %s" % s
		except StopIteration:
			return

	def close(self):
		"""
		TDV.close() method.
		Closes the underlying TDV file object.
		"""
		try:
			self.__tdv_fil.close()
		except IOError:
			sys.stderr.write(sys.argv[0] + ": Could not close input TDV file " + \
			self.__tdv_filename + ". Terminating.\n")
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
	if len(sys.argv) != 2:
		usage()
		debug("Incorrect # of args, exiting.")
		sys.exit(1)

	# get input TDV filename
	tdv_filename = sys.argv[1]
	debug("TDV filename = ", tdv_filename)

	# Create a TDVReader instance using the input TDV filename
	tdv_reader = TDVReader(tdv_filename)
	debug("tdv_reader.__dict__ = ", tdv_reader.__dict__)

	# Open the TDVReader instance
	tdv_reader.open()
	# Print all its rows
	debug("Before loop to read rows from " + tdv_reader.get_description())
	tdv_reader.print_rows()
	debug("After loop to read rows")
	# Close the TDVReader instance
	tdv_reader.close()

	sys.exit(0)


#------------------------- usage ----------------------------

def usage():
	
	global prog_name
	sys.stderr.write("Usage: " + prog_name + " tdv_filename\n")

#------------------------- call main ------------------------

if __name__ == "__main__":
	main()

#------------------------- EOF: TDVReader.py ---------------

