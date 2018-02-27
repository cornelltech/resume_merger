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
    if filename:
        return clean_text(filename.replace(extension, '')) + extension

def clean_student_row(row):
    """company,netid,first last name, program/year, time, comment

    We don't care about the last two.
    """
    company = row[0].lower()
    raw_student_info = row[1:4]
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
    return companies

def write_and_merge_pdfs(company, student_filenames):
    print('creating pdf for', company)
    merger = PdfFileMerger(strict=False)

    for student_filename in student_filenames:
        print('looking for student filename')
        print(student_filename)
        try:
            merger.append(PdfFileReader(open('/Users/kristinaortiz/Desktop/resume_merger/data/' + student_filename, 'rb'), strict=False))
        except Exception as e:
            print(e)

    merger.write('/Users/kristinaortiz/Desktop/resume_merger/dist/' + company + '.pdf')

def normalize_data_files(loc='/Users/kristinaortiz/Desktop/resume_merger/data'):
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

    dist = '/Users/kristinaortiz/Desktop/resume_merger/dist'
    if not os.path.exists(dist):
        os.makedirs(dist)

    filename = '/Users/kristinaortiz/Desktop/resume_merger/students.csv'
    student_company_mapping = read_student_file(filename)
    for company in student_company_mapping:
        if company == '':
            pass
        else:
          write_and_merge_pdfs(company, student_company_mapping[company])
