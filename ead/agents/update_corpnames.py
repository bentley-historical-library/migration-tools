'''
first things first, import what we need'''

# lxml is a powerful xml document parser, you'll need to download it
from lxml import etree

# os provides a portable way of using operating system dependent functionality
import os
from os.path import join

# tqdm adds a progress meter to loops, you'll need to install it
from tqdm import *


'''
setup'''

# where are the eads?
ead_folder = 'C:/Users/eckardm/GitHub/vandura/Real_Masters_all'
# ead_folder = 'C:/Users/Public/Documents/Real_Masters_all'


'''
now add any sources in the dictionary to names that are missing them'''

# go through each of the files in the ead folder
for filename in tqdm(os.listdir(ead_folder)):
    # but only do the ones that are actually eads (we can tell because they are xml files)
    if filename.endswith('.xml'):
        # create an etree (part of lxml) tree that we can parse
        ead_tree = etree.parse(join(ead_folder, filename))
        # go through each of the elements at that xpath
        for name in ead_tree.xpath('//corpname'):
            # if it doesn't have a source and the name is in the dictionary we just created
            if 'controlaccess' in ead_tree.getpath(name) or 'origination' in ead_tree.getpath(name):
                if not name.get('source') and '--' not in name.text:
                    name.attrib['source'] = 'lcnaf'
                    with open(os.path.join(ead_folder, filename), mode="w") as see_i_am_making_all_things_new:
                        # and write it
                        see_i_am_making_all_things_new.write(etree.tostring(ead_tree, xml_declaration=True, encoding='utf-8', pretty_print=True))