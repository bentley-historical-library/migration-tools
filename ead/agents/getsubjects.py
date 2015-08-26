from lxml import etree as ET
import os
from os.path import join
import csv
from tqdm import *

# where are the eads?
ead_path = 'C:/Users/eckardm/GitHub/vandura/Real_Masters_all'

# where are the temp files?
persname_temp = 'persname_temp.csv'
famname_temp = 'famname_temp.csv'
corpname_temp = 'corpname_temp.csv'

# where are the output files?
persname_output = 'persname.csv'
famname_output = 'famname.csv'
corpname_output = 'corpname.csv'

# headers
persname_headers = ['Type', 'Publish', 'Authority ID', 'Source', 'Rules', 'Name Order', 'ORIGINAL', 'Prefix', 'Title', 'Primary Part of Name', 'Rest of Name', 'Suffix', 'Fuller Form', 'Number', 'Dates', 'Qualifier']
famname_headers = ['Type', 'Publish', 'Authority ID', 'Source', 'Rules', 'ORIGINAL', 'Prefix', 'Family Name', 'Dates', 'Qualifier']
corpname_headers = ['Type', 'Publish', 'Authority ID', 'Source', 'Rules', 'ORIGINAL', 'Primary Part of Name', 'Subordinate Name 1', 'Subordinate Name 2', 'Number', 'Dates', 'Qualifier']

# empty list
list = []

# xpaths
origination_xpath =  '//origination/*'
controlaccess_xpath = '//controlaccess/*'

print 'Creating dictionary...'

for filename in tqdm(os.listdir(ead_path)):
    if filename.endswith('.xml'):
        ead_tree = ET.parse(join(ead_path, filename))
        dictionary = {}
        for controlaccess_subelement in ead_tree.xpath(origination_xpath):
            if (controlaccess_subelement.tag == 'famname' or controlaccess_subelement.tag == 'corpname') and controlaccess_subelement.text is not None and '--' not in controlaccess_subelement.text:
                dictionary['Type'] = controlaccess_subelement.tag
                dictionary['ORIGINAL'] = controlaccess_subelement.text.strip()
                if 'authfilenumber' in controlaccess_subelement.attrib:
                    dictionary['Authority ID'] = controlaccess_subelement.get('authfilenumber')
                if 'source' in controlaccess_subelement.attrib:
                    dictionary['source'] = controlaccess_subelement.get('source')
                list.append(dictionary)
            elif (controlaccess_subelement.tag == 'persname' or controlaccess_subelement.tag == 'famname' or controlaccess_subelement.tag == 'corpname') and controlaccess_subelement.text is not None and '--' in controlaccess_subelement.text:
                dictionary['Type'] = controlaccess_subelement.tag
                dictionary['ORIGINAL'] = controlaccess_subelement.text.strip().split('--')[0]
                if 'authfilenumber' in controlaccess_subelement.attrib:
                    dictionary['Authority ID'] = controlaccess_subelement.get('authfilenumber')
                if 'source' in controlaccess_subelement.attrib:
                    dictionary['source'] = controlaccess_subelement.get('source')
                list.append(dictionary)
                
for filename in tqdm(os.listdir(ead_path)):
    if filename.endswith('.xml'):
        ead_tree = ET.parse(join(ead_path, filename))
        dictionary = {}
        for controlaccess_subelement in ead_tree.xpath(controlaccess_xpath):
            if (controlaccess_subelement.tag == 'famname' or controlaccess_subelement.tag == 'corpname') and controlaccess_subelement.text is not None and '--' not in controlaccess_subelement.text:
                dictionary['Type'] = controlaccess_subelement.tag
                dictionary['ORIGINAL'] = controlaccess_subelement.text.strip()
                if 'authfilenumber' in controlaccess_subelement.attrib:
                    dictionary['Authority ID'] = controlaccess_subelement.get('authfilenumber')
                if 'source' in controlaccess_subelement.attrib:
                    dictionary['source'] = controlaccess_subelement.get('source')
                list.append(dictionary)
            elif (controlaccess_subelement.tag == 'persname' or controlaccess_subelement.tag == 'famname' or controlaccess_subelement.tag == 'corpname') and controlaccess_subelement.text is not None and '--' in controlaccess_subelement.text:
                dictionary['Type'] = controlaccess_subelement.tag
                dictionary['ORIGINAL'] = controlaccess_subelement.text.strip().split('--')[0]
                if 'authfilenumber' in controlaccess_subelement.attrib:
                    dictionary['Authority ID'] = controlaccess_subelement.get('authfilenumber')
                if 'source' in controlaccess_subelement.attrib:
                    dictionary['source'] = controlaccess_subelement.get('source')
                list.append(dictionary)
            
# print 'Creating <persname> CSV...'

# with open(persname_temp, 'wb') as persname_csv:
    # persname_header_writer = csv.writer(persname_csv)
    # persname_header_writer.writerow(persname_headers)
    
# for dictionary_item in tqdm(list):
    # if dictionary_item['Type'] == 'persname':
        # persname_row = ['persname', 'TRUE']
        # if 'Authority ID' in dictionary_item:
            # persname_row.append(dictionary_item['Authority ID'])
        # else:
            # persname_row.append('')
        # if 'source' in dictionary_item:
            # persname_row.append(dictionary_item['source'])
        # else:
            # persname_row.append('')
        # persname_row.append('')
        # persname_row.append('Indirect')
        # persname_row.append(dictionary_item['ORIGINAL'].encode('utf-8'))
        # with open(persname_temp, 'ab') as persname_csv_take_two:
            # persname_writer = csv.writer(persname_csv_take_two)
            # persname_writer.writerow(persname_row)
            
# with open(persname_temp, 'rb') as persname_in, open(persname_output, 'wb') as persname_out:
    # persnames = set()
    # for row in persname_in:
        # if row in persnames: 
            # continue
        # persnames.add(row)
        # persname_out.write(row)

# os.remove(persname_temp)
        
print 'Creating <famname> CSV...'
        
with open(famname_temp, 'wb') as famname_csv:
    famname_header_writer = csv.writer(famname_csv)
    famname_header_writer.writerow(famname_headers)
    
for dictionary_item in tqdm(list):        
    famname_row = ['famname', 'TRUE']
    if dictionary_item['Type'] == 'famname':
        if 'Authority ID' in dictionary_item:
            famname_row.append(dictionary_item['Authority ID'])
        else:
            famname_row.append('')
        if 'source' in dictionary_item:
            famname_row.append(dictionary_item['source'])
        else:    
            famname_row.append('')
        famname_row.append('')
        famname_row.append(dictionary_item['ORIGINAL'].encode('utf-8'))
        with open(famname_temp, 'ab') as famname_csv_take_two:
            famname_writer = csv.writer(famname_csv_take_two)
            famname_writer.writerow(famname_row) 
            
with open(famname_temp, 'rb') as famname_in, open(famname_output, 'wb') as famname_out:
    famnames = set()
    for row in famname_in:
        if row in famnames: 
            continue
        famnames.add(row)
        famname_out.write(row)

os.remove(famname_temp)

print 'Creating <corpname> CSV...'
        
with open(corpname_temp, 'wb') as corpname_csv:
    corpname_header_writer = csv.writer(corpname_csv)
    corpname_header_writer.writerow(corpname_headers)
    
for dictionary_item in tqdm(list):          
    corpname_row = ['corpname', 'TRUE']
    if dictionary_item['Type'] == 'corpname':
        if 'Authority ID' in dictionary_item:
            corpname_row.append(dictionary_item['Authority ID'])
        else:
            corpname_row.append('')
        if 'source' in dictionary_item:
            corpname_row.append(dictionary_item['source'])
        else:
            corpname_row.append('')
        corpname_row.append('')
        corpname_row.append(dictionary_item['ORIGINAL'].encode('utf-8'))
        with open(corpname_temp, 'ab') as corpname_csv_take_two:
            corpname_writer = csv.writer(corpname_csv_take_two)
            corpname_writer.writerow(corpname_row)  
            
with open(corpname_temp, 'rb') as corpname_in, open(corpname_output, 'wb') as corpname_out:
    corpnames = set()
    for row in corpname_in:
        if row in corpnames: 
            continue
        corpnames.add(row)
        corpname_out.write(row)

os.remove(corpname_temp)
            
print 'Done!'
                    