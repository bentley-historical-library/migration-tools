# import what we need
import os
from os.path import join
import csv
from lxml import etree as ET
from tqdm import *

# where are the eads (test and production)?
ead_path_test = 'C:/Users/Public/Documents/Real_Masters_all'
ead_path_production = 'C:/Users/eckardm/GitHub/vandura/Real_Masters_all'

# xpaths
controlaccess_xpath = '//ead/archdesc//controlaccess/*'
origination_xpath = '//ead/archdesc//origination/*'

print 'Adding authority file numbers to <origination> tag when they exist in <controlaccess> subfields.'

# go through the files
for filename in tqdm(os.listdir(ead_path_test)):
    # parser = ET.XMLParser(remove_blank_text=True)
    if filename.endswith('.xml'):
        ead_tree = ET.parse(join(ead_path_test, filename))
        controlaccess_subelement_dictionary = {}
        for controlaccess_subelement in ead_tree.xpath(controlaccess_xpath):
            if 'authfilenumber' in controlaccess_subelement.attrib:
                controlaccess_subelement_dictionary[controlaccess_subelement.text] = controlaccess_subelement.get('authfilenumber')
        for origination_subelement in ead_tree.xpath(origination_xpath):
            if origination_subelement.text in controlaccess_subelement_dictionary:
                origination_subelement.set('authfilenumber', controlaccess_subelement_dictionary[origination_subelement.text])
    outfile = open(join(ead_path_test, filename), 'w')
    outfile.write(ET.tostring(ead_tree, pretty_print=True, encoding="utf-8", xml_declaration=True))
    outfile.close()
        
                
print '\rAdded authority file numbers to <origination> tag when they exist in <controlaccess> subfields.'

# don't forget pretty print