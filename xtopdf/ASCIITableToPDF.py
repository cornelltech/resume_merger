
# ASCIITableToPDF.py
# Author: Vasudev Ram - http://www.dancingbison.com
# Demo program to show how to generate an ASCII table as PDF,
# using the xtopdf toolkit for PDF creation from Python.
# Generates a PDF file with information about the 
# first 32 ASCII codes, i.e. the control characters.
# Based on the ASCII Code table at http://www.ascii-code.com/

import sys
from PDFWriter import PDFWriter

# Define the header information.
column_names = ['DEC', 'OCT', 'HEX', 'BIN', 'Symbol', 'Description']
column_widths = [4, 6, 4, 10, 7, 20]

# Define the ASCII control character information.
ascii_control_characters = \
"""
0    000    00    00000000    NUL    &#000;         Null char
1    001    01    00000001    SOH    &#001;         Start of Heading
2    002    02    00000010    STX    &#002;         Start of Text
3    003    03    00000011    ETX    &#003;         End of Text
4    004    04    00000100    EOT    &#004;         End of Transmission
5    005    05    00000101    ENQ    &#005;         Enquiry
6    006    06    00000110    ACK    &#006;         Acknowledgment
7    007    07    00000111    BEL    &#007;         Bell
8    010    08    00001000    BS    &#008;         Back Space
9    011    09    00001001    HT    &#009;         Horizontal Tab
10    012    0A    00001010    LF    &#010;         Line Feed
11    013    0B    00001011    VT    &#011;         Vertical Tab
12    014    0C    00001100    FF    &#012;         Form Feed
13    015    0D    00001101    CR    &#013;         Carriage Return
14    016    0E    00001110    SO    &#014;         Shift Out / X-On
15    017    0F    00001111    SI    &#015;         Shift In / X-Off
16    020    10    00010000    DLE    &#016;         Data Line Escape
17    021    11    00010001    DC1    &#017;         Device Control 1 (oft. XON)
18    022    12    00010010    DC2    &#018;         Device Control 2
19    023    13    00010011    DC3    &#019;         Device Control 3 (oft. XOFF)
20    024    14    00010100    DC4    &#020;         Device Control 4
21    025    15    00010101    NAK    &#021;         Negative Acknowledgement
22    026    16    00010110    SYN    &#022;         Synchronous Idle
23    027    17    00010111    ETB    &#023;         End of Transmit Block
24    030    18    00011000    CAN    &#024;         Cancel
25    031    19    00011001    EM    &#025;         End of Medium
26    032    1A    00011010    SUB    &#026;         Substitute
27    033    1B    00011011    ESC    &#027;         Escape
28    034    1C    00011100    FS    &#028;         File Separator
29    035    1D    00011101    GS    &#029;         Group Separator
30    036    1E    00011110    RS    &#030;         Record Separator
31    037    1F    00011111    US    &#031;         Unit Separator
"""

# Create and set some of the fields of a PDFWriter instance.
pw = PDFWriter("ASCII-Table.pdf")
pw.setFont("Courier", 12)
pw.setHeader("ASCII Control Characters - 0 to 31")
pw.setFooter("Generated by xtopdf: http://slid.es/vasudevram/xtopdf")

# Write the column headings to the output.
column_headings = [ str(val).ljust(column_widths[idx]) \
    for idx, val in enumerate(column_names) ]
pw.writeLine(' '.join(column_headings))

# Split the string into lines, omitting the first and last empty lines.
for line in ascii_control_characters.split('\n')[1:-1]:

    # Split the line into space-delimited fields.
    lis = line.split()

    # Join the words of the Description back into one field, 
    # since it was split due to having internal spaces.
    lis2 = lis[0:5] + [' '.join(lis[6:])]

    # Write the column data to the output.
    lis3 = [ str(val).ljust(column_widths[idx]) \
        for idx, val in enumerate(lis2) ]
    pw.writeLine(' '.join(lis3))

pw.close()

