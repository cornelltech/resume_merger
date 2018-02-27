
Description:

This package (xtopdf) contains tools to convert various file formats  (collectively called x) to PDF format. The PDF files created are viewable and printable by any PDF viewer/reader, such as Adobe Acrobat Reader, XPDF, GhostView, and KGhostView.

Currently supported input formats are:

1. Plain text (not including Postscript, which is also a kind of "text").

2. .DBF files (XBase files)

3. .CSV files (Comma Separated Values files)

4. .TDV files (Tab Delimited Values files)

Licensing:

The xtopdf package is Copyright (C) 2012, Vasudev Ram. It is released as open source under the BSD License. The license is in the files License.html and License.txt, which are part of the package.

Prerequisites:

1. Python 2.2 or later version. Get it from http://www.python.org and install it. Note: xtopdf is not tested with Python 3.x, though it may work with it. The latest version of xtopdf (this version) has been developed and tested (some) on Python 2.7.

2. The open source version of the ReportLab toolkit. Get it from here:
http://www.reportlab.com/ftp/reportlab-1.21.zip

Note: xtopdf is not tested with ReportLab v2.x series, though it may work with it.

Platforms:

1. Linux: xtopdf is developed and tested on Linux.

2. Windows: xtopdf has been tested some on Windows, and should work on it.

3. Mac OS X: xtopdf has not been tested on Mac OS X, but may work on it, since Mac OS X is based on UNIX.

Installation and usage:

To install the files, first make sure that you have downloaded and installed all the prerequisities mentioned above, including setup steps such as adding needed directories to your PYTHONPATH. Then, copy all the files in xtopdf.zip into a directory which is on your PYTHONPATH.

To use any of the Python programs, run the .py file as:

   python filename.py

This will give a usage message about the correct usage and arguments expected.

To run the shell script(s), do the same as above.

Developers can look at the source code for further information.

[ToDo: update this section to provide usage examples.]

Also look at the file descriptions below to get a better
idea about the software.

The following is the list of files in the xtodpf package:

Filename    Description
--------    --------------------------------------------------------

License files:

License.html
License.txt

Code files:

ReadDBF.py    Reads data and metadata from a DBF file - procedural version
WritePDF.py    Writes a text file to a PDF file - procedural version
DBFtoPDF.sh    Script to invoke ReadDBF.py and WritePDF.py in sequence,
with output of ReadDBF.py becoming input of WritePDF.py
DBFReader.py    Reads data and metadata from a DBF file - object-oriented
version
PDFWriter.py    Writes a text file to a PDF file - object-oriented version
DBFtoPDF.py    Makes use of DBFReader and PDFWriter to achieve same effect
as DBFtoPDF.sh
DBFDataOnly.py    Makes use of DBFReader.py to read only the data records
from a DBF file
PDFBook.py    Reads a series of text files representing chapters of a book
and generates a PDF file of the book's content
file_utils.py    Helper Python module for filename manipulation
CSVReader.py    Module to read data from .CSV files
TDVReader.py    Module to read data from .TDV files
PDFBuilder.py    Module to create composite PDFs from different types of files

Data / other files:

test1.dbf    Sample input file for the DBF-reading programs
test2.dbf    Sample input file for the DBF-reading programs
test3.dbf    Sample input file for the DBF-reading programs
test4.dbf    Sample input file for the DBF-reading programs
test4.dat    Sample output of ReadDBFDataOnly.py when run with test4.dbf as
input
book1-chapter[1-5].txt    Chapter files for book1
book1.txt    List of chapter files for book1
book2-chapter[1-5].txt    Chapter files for book2
book2.txt    List of chapter files for book2
file_[ab]    Sample input files for PDFWriter.py
README.txt    This file
stdio.m    Sample input file for PDFWriter.py
test4-640-line-num.txt.gz    Sample large file for text-to-PDF programs
file3.csv    Sample input file for the CSV-reading programs
file4.csv    Sample input file for the CSV-reading programs
file2.tdv    Sample input file for the TDV-reading programs
file3.tdv    Sample input file for the TDV-reading programs

=========================================================================
