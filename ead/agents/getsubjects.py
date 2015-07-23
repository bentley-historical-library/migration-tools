from lxml import etree as ET
import os
from os.path import join
import csv
from tqdm import *

# where are the eads?
ead_path = 'C:/Users/eckardm/GitHub/vandura/Real_Masters_all'

# where are the output files?
persname_output = 'persname.csv'
famname_output = 'geogname.csv'
corpname_output = 'corpname.csv'

# headers
persname_headers = ['Type', 'Publish', 'Authority ID', 'Source', 'Rules', 'Name Order', 'ORIGINAL', 'Prefix', 'Title', 'Primary Part of Name', 'Rest of Name', 'Suffix', 'Fuller Form', 'Number', 'Dates', 'Qualifier']
famname_headers = ['Type', 'Publish', 'Authority ID', 'Source', 'Rules', 'ORIGINAL', 'Prefix', 'Family Name', 'Dates', 'Qualifier']
corpname_headers = ['Type', 'Publish', 'Authority ID', 'Source', 'Rules', 'ORIGINAL', 'Primary Part of Name', 'Subordinate Name 1', 'Subordinate Name 2', 'Number', 'Dates', 'Qualifier']

# empty list
list = []

print 'Creating dictionary...'

for filename in tqdm(os.listdir(ead_path)):
    if filename.endswith('.xml'):
        ead_tree = ET.parse(join(ead_path, filename))
        for controlaccess_subelement in ead_tree.xpath('//*'):
            if (controlaccess_subelement.tag == 'persname' or controlaccess_subelement.tag == 'famname' or controlaccess_subelement.tag == 'corpname') and controlaccess_subelement.text is not None and '--' not in controlaccess_subelement.text:
                dictionary = {}
                dictionary['Type'] = controlaccess_subelement.tag
                dictionary['ORIGINAL'] = controlaccess_subelement.text.strip()
                if 'authfilenumber' in controlaccess_subelement.attrib:
                    dictionary['Authority ID'] = controlaccess_subelement.get('authfilenumber')
                if 'source' in controlaccess_subelement.attrib:
                    dictionary['source'] = controlaccess_subelement.get('source')
                list.append(dictionary)
            
print 'Creating <persname> CSV...'

with open(persname_output, 'wb') as persname_csv:
    persname_header_writer = csv.writer(persname_csv)
    persname_header_writer.writerow(persname_headers)
    
for dictionary_item in tqdm(list):
    if dictionary_item['Type'] == 'persname':
        persname_row = ['persname', 'TRUE']
        if 'authfilenumber' in dictionary_item:
            persname_row.append(dictionary_item['authfilenumber'])
        else:
            persname_row.append('')
        if 'source' in dictionary_item:
            persname_row.append(dictionary_item['source'])
        else:
            persname_row.append('')
        persname_row.append('')
        persname_row.append('')
        persname_row.append('Indirect')
        persname_row.append(dictionary_item['ORIGINAL'].encode('utf-8'))
        with open(persname_output, 'ab') as persname_csv_take_two:
            persname_writer = csv.writer(persname_csv_take_two)
            persname_writer.writerow(persname_row)
        
print 'Creating <famname> CSV...'
        
with open(famname_output, 'wb') as famname_csv:
    famname_header_writer = csv.writer(famname_csv)
    famname_header_writer.writerow(famname_headers)
    
for dictionary_item in tqdm(list):        
    famname_row = ['famname', 'TRUE']
    if dictionary_item['Type'] == 'famname':
        if 'authfilenumber' in dictionary_item:
            famname_row.append(dictionary_item['authfilenumber'])
        else:
            famname_row.append('')
        if 'source' in dictionary_item:
            famname_row.append(dictionary_item['source'])
        else:    
            famname_row.append('')
        famname_row.append('')
        famname_row.append(dictionary_item['ORIGINAL'].encode('utf-8'))
        with open(famname_output, 'ab') as famname_csv_take_two:
            famname_writer = csv.writer(famname_csv_take_two)
            famname_writer.writerow(famname_row) 

print 'Creating <corpname> CSV...'
        
with open(corpname_output, 'wb') as corpname_csv:
    corpname_header_writer = csv.writer(corpname_csv)
    corpname_header_writer.writerow(corpname_headers)
    
for dictionary_item in tqdm(list):          
    corpname_row = ['corpname', 'TRUE']
    if dictionary_item['Type'] == 'corpname':
        if 'corpfilenumber' in dictionary_item:
            corpname_row.append(dictionary_item['authfilenumber'])
        else:
            corpname_row.append('')
        if 'source' in dictionary_item:
            corpname_row.append(dictionary_item['source'])
        else:
            corpname_row.append('')
        corpname_row.append('')
        corpname_row.append(dictionary_item['ORIGINAL'].encode('utf-8'))
        with open(corpname_output, 'ab') as corpname_csv_take_two:
            corpname_writer = csv.writer(corpname_csv_take_two)
            corpname_writer.writerow(famname_row)  
            
print 'Done!'
                    