'''
step one of https://github.com/mcarruthers/LCNAF-Named-Entity-Reconciliation, hopefully we'll get some lcnaf or viaf out of this'''

import lxml
from lxml import etree as ET
import os
from os.path import join
import re

# where are the eads?
ead_path = 'C:/Users/eckardm/GitHub/vandura/Real_Masters_all'

# where are the output files?
persname_output = 'persname.txt'
corpname_output = 'corpname.txt'
geogname_output = 'geogname.txt'

# empty_lists
persname_list = []
corpname_list = []
geogname_list = []

# regex
xml = re.compile('\.xml$')

# controlaccess xpath
controlaccess_xpath = '//ead/archdesc//controlaccess/*'

# error counter
error_counter = 0

# got through the files
for filename in os.listdir(ead_path):
    # only look at xml
    if xml.search(filename):
        print '\rWorking on it... |',
        print '\rWorking on it... /',
        print '\rWorking on it... -',
        print '\rWorking on it... \\',
        print '\rWorking on it... |',
        print '\rWorking on it... /',
        print '\rWorking on it... -',
        print '\rWorking on it... -',
        print '\rWorking on it... \\',
        # parse
        ead_tree = ET.parse(join(ead_path, filename))
        # go through the eads
        for sub in ead_tree.xpath(controlaccess_xpath):
            # persname <-- could make these next three functions...
            if sub.tag == 'persname' and sub.text is not None and '--' not in sub.text:
                output = sub.text.strip()
                if output not in persname_list:
                    persname_list.append(output)
            # corpname
            elif sub.tag == 'corpname' and sub.text is not None and '--' not in sub.text:
                output = sub.text.strip()
                if output not in corpname_list: 
                    corpname_list.append(output)
            # geogname
            if sub.tag == 'geogname' and sub.text is not None and '--' not in sub.text:
                output = sub.text.strip()   
                if output not in geogname_list:
                    geogname_list.append(output)

# output <-- could make these next three functions...
for persname in persname_list:
    with open(persname_output, 'a') as text_file:
        text_file.write(persname.encode("utf-8") + '\n')
        
for corpname in corpname_list:
        with open(corpname_output, 'a') as text_file:
            text_file.write(corpname.encode("utf-8") + '\n')
            
for geogname in geogname_list:
        with open(geogname_output, 'a') as text_file:
            text_file.write(geogname.encode("utf-8") + '\n')
                    
print '\rThere were ' + str(error_counter) + ' errors!'