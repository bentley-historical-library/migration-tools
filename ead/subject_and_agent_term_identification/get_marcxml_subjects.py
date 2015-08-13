from lxml import etree
import os
from os.path import join
import csv

path = 'C:/Users/Public/Documents/marc_xml-has_ead-split'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    subject_fields = ['650','651','655']
    for subject_field in subject_fields:
        subjects = tree.xpath('//marc:datafield[@tag="'+subject_field+'"]', namespaces={'marc': 'http://www.loc.gov/MARC21/slim'})
        for subject in subjects:
            terms_dict = {}
            terms_list = []
            print filename
            index = 1
            for subfield in subject.xpath('./*'):
                if not subfield.attrib['code'].isdigit():
                    code = subfield.attrib['code']
                    term = subfield.text.encode('utf-8')
                    terms_dict[index] = {}
                    terms_dict[index][term] = code
                    terms_list.append(term)
                    index += 1
            joined = '--'.join([term for term in terms_list])
            row = []
            row.append(joined)
            row.append(subject_field)
            loop = 0
            while loop+1 < index:
                for term in terms_dict[loop+1]:
                    row.append(term)
                    row.append(terms_dict[loop+1][term])
                    loop += 1

            with open('C:/Users/Public/Documents/marc_xml-subjects_20150806.csv','ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow(row)
