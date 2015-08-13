from lxml import etree
import csv
import os
from os.path import join


tags = ['subject', 'geogname','genreform']
subjects = {'subject':{},'geogname':{},'genreform':{}}

# Get a csv with only unique subjects
path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for sub in tree.xpath('//controlaccess/*'):
        if sub.tag in tags and sub.text is not None:
            sub_text = sub.text.encode('utf-8')
            source = sub.attrib['source']
            if source not in subjects[sub.tag]:
                subjects[sub.tag][source] = []
            if sub_text not in subjects[sub.tag][source]:
                subjects[sub.tag][source].append(sub_text)
    print '\rProcessing unique subjects for',filename

print 'Writing unique subject csv'
for subject_type in subjects:
    for source in subjects[subject_type]:
        for subject in subjects[subject_type][source]:
            with open('C:/Users/Public/Documents/ead_unique_subjects_20150810.csv', 'ab') as csvfile:
                row = []
                row.append(subject_type)
                row.append(source)
                row.append(subject)
                terms = subject.split('--')
                for term in terms:
                    row.append(term)
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow(row)
'''
# Get a csv with all subjects for each file
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for sub in tree.xpath('//controlaccess/*'):
        if sub.tag in tags and sub.text is not None:
            row = []
            row.append(filename)
            row.append(sub.tag)
            row.append(sub.attrib['source'])
            sub_text = sub.text.encode('utf-8')
            row.append(sub_text)
            if '--' in sub_text:
                terms = sub_text.split('--')
                for term in terms:
                    row.append(term)
            with open('C:/Users/Public/Documents/ead_subjects_20150810.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow(row)
    print '\rWriting csv with all subjects for',filename
'''
