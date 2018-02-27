
#---------------------------------------------------------------------

# XlsToPdf.py


# Author: Vasudev Ram - http://www.dancingbison.com
# Copyright 2006-2006 Vasudev Ram, http://www.dancingbison.com

# This is open source code, released under the New BSD License -
# see http://www.opensource.org/licenses/bsd-license.php .

# THIS IS ALPHA CODE FOR DEMO PURPOSES ONLY - USE AT YOUR OWN RISK!


#---------------------------------------------------------------------

# From Python Standard Library
import sys
import os
import os.path
import string

#---------------------------------------------------------------------

# From xlrd module
import xlrd

#---------------------------------------------------------------------

# From xtopdf module
from file_utils import change_file_ext
from PDFWriter import PDFWriter

#---------------------------------------------------------------------

# appends the given string lin to the list lis
def save(lis, lin):
	#print lin
	lis.append(lin)

#---------------------------------------------------------------------

def usage():
	sys.stderr.write( \
		"Copyright 2006-2006 Vasudev Ram - http://www.dancingbison.com\n")
	sys.stderr.write("Usage: " + sys.argv[0] + "xls_filename\n")
	sys.stderr.write("This converts contents of xls_filename to PDF\n")
	sys.stderr.write("in a file with same basename and extension .pdf\n")

#---------------------------------------------------------------------

def main():

	if len(sys.argv) != 2:
		usage()
		sys.exit(0)

	lis = []
	xls_fn = sys.argv[1]
	book = xlrd.open_workbook(xls_fn)
	save(lis, \
			"The XLS file " + xls_fn + " has %d worksheets" % book.nsheets)
	save(lis, "Worksheet name(s): " + ", ".join(book.sheet_names()))
	sheet = book.sheet_by_index(0)
	save(lis, sheet.name + ":")
	save(lis, "%8s%8s" % ("Rows", "Cols"))
	save(lis, "%8s%8s" % (str(sheet.nrows), str(sheet.ncols)))
	save(lis, "Cell A0 is " + sheet.cell_value(rowx=0, colx=0))
	save(lis, "Rows:")
	row_num = 0
	for rx in range(sheet.nrows):
		#row1 = sheet.row(rx) # this line gave probs, replaced with line below.
		row1 = sheet.row_values(rx)
		save(lis, "Row # %s:" % str(row_num))
		#row2 = [ repr(ite) for ite in row1 ]
		row2 = []
		# next few lines including the for loop are a workaround to
		# make both unicode strings and regular strings show properly
		# in the output
		unicode_str = u'Dummy'
		for ite in row1:
			ite2 = ite
			if type(ite) == type(unicode_str):
				ite2 = str(ite)
			else:
				ite2 = repr(ite)
			row2.append(ite2)
		#for ite in row2:
			#print "type(ite:lis2) = ", type(ite)
		save(lis, ", ".join(row2))
		row_num += 1
	print "Output:"
	print "\n".join(lis)

	pdf_fn = change_file_ext(xls_fn, '.xls', '.pdf')
	pw = PDFWriter(pdf_fn)
	pw.setFont("Courier", 10)
	header_str = sys.argv[0] + ": " + xls_fn + " => " + pdf_fn
	footer_str = header_str
	pw.setHeader(header_str)
	pw.setFooter(footer_str)
	
	for lin in lis:
		pw.writeLine(lin)

	pw.close()

if __name__ == "__main__":
	main()

#-------------------------------- EOF: XlsToPdf.py -------------------
