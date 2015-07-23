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

# go through the xml files
for filename in tqdm(os.listdir(ead_path_test)):
    if filename.endswith('.xml'):
        ead_tree = ET.parse(join(ead_path_test, filename))
        controlaccess_subelement_dictionary = {}
        # make a dictionary of controlaccess subelement text and authfilenumbers
        for controlaccess_subelement in ead_tree.xpath(controlaccess_xpath):
            if 'authfilenumber' in controlaccess_subelement.attrib:
                controlaccess_subelement_dictionary[controlaccess_subelement.text] = controlaccess_subelement.get('authfilenumber')
        # match the origination subelement text to dictionary and add authfilenumber attribute
        for origination_subelement in ead_tree.xpath(origination_xpath):
            if origination_subelement.text in controlaccess_subelement_dictionary:
                origination_subelement.set('authfilenumber', controlaccess_subelement_dictionary[origination_subelement.text])
    # write the files, and pretty print
    outfile = open(join(ead_path_test, filename), 'w')
    outfile.write(ET.tostring(ead_tree, pretty_print=True, encoding="utf-8", xml_declaration=True))
    outfile.close()