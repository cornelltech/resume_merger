#!/usr/bin/python

import os
import csv
import re

from PyPDF2 import PdfFileMerger, PdfFileReader


def clean_text(s):
    s = s.lower()
    # ref: https://stackoverflow.com/questions/14361556/remove-all-special-characters-in-java
    s = re.sub(
           r"[^a-zA-Z0-9]", 
           '',
           s, 
       )
    # we want to trim the year in the back because it will be inconsistent
    # and a source of error because its so arbitrary and breakable.
    s = ''.join(
        [ s[0:-4], re.sub(
           r"\d+", 
           '',
           s[-4:], 
       ) ]
    )
    return s

def clean_filename(filename, extension='.pdf'):
    return clean_text(filename.replace(extension, '')) + extension

def clean_student_row(row):
    """company,netid,first last name, program/year, time, comment

    We don't care about the last two.
    """
    company = row[0].lower()
    raw_student_info = row[1:-2]
    student_info = ''.join(raw_student_info)
    student_info = clean_text(student_info)

    return company, student_info

def read_student_file(filename, extension='.pdf'):
    companies = {}
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if i is 0:
                continue
            company, student_info = clean_student_row(row)
            student_info = student_info + extension
            if company in companies:
                companies[company].append(student_info)
            else:
                companies[company] = [student_info]
            # print(clean_student_row(row))
    return companies

def write_and_merge_pdfs(company, student_filenames):
    print('creating pdf for', company)
    merger = PdfFileMerger()

    for student_filename in student_filenames:
        try:
            merger.append(PdfFileReader(file('./data/' + student_filename, 'rb')))
        except Exception as e:
            print(e)
        
    merger.write('dist/' + company + '.pdf')

def normalize_data_files(loc='./data'):
    file_list = os.listdir(loc)
    for filename in file_list:
        cleaned_filename = clean_filename(filename)
        os.rename(
            '/'.join([loc, filename]),
            '/'.join([loc, cleaned_filename]),
        )


if __name__ == '__main__':
    print('-> Starting Script')

    print('-> Normalizing Filenames in ./data')
    normalize_data_files()
    print('-- Done')

    dist = './dist'
    if not os.path.exists(dist):
        os.makedirs(dist)

    filename = 'students.csv'
    student_company_mapping = read_student_file(filename)
    for company in student_company_mapping:
        write_and_merge_pdfs(company, student_company_mapping[company])

    # f = 'Ebk46evankestenCM18.pdf'

    # print('*'*50)

    # print( clean_filename(f) )