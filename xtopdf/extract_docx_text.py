# extract_docx_text.py

import sys
from docx import opendocx, getdocumenttext

def extract_docx_text(infil, outfil):

    # Extract the text from the DOCX file object infile and write it to 
    # the text file object outfil.

    paragraphs = getdocumenttext(infil)

    # For Unicode handling.
    new_paragraphs = []
    for paragraph in paragraphs:
        new_paragraphs.append(paragraph.encode("utf-8"))

    outfil.write('\n'.join(new_paragraphs))

def usage():

    return "Usage: python extract_docx_text.py infile.docx outfile.txt\n"

def main():

    if len(sys.argv) != 3:
        print usage()
        sys.exit(1)

    try:
        infil = opendocx(sys.argv[1])
        outfil = open(sys.argv[2], 'w')
    except Exception, e:
        print "Exception: " + repr(e) + "\n"
        sys.exit(1)

    extract_docx_text(infil, outfil)

if __name__ == '__main__':
    main()

# EOF
