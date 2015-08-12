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

# xpaths list for names (persname, corpname and famname elements)
name_xpaths = ['//persname', '//corpname', '//famname']

# dictionary
name_source_dictionary = {}


'''
make a dictionary of names and sources'''

# for each name elements
for name_xpath in name_xpaths:
    # go through each of the files in the ead folder
    for filename in tqdm(os.listdir(ead_folder)):
        # but only do the ones that are actually eads (we can tell because they are xml files)
        if filename.endswith('.xml'):
            # create an etree (part of lxml) tree that we can parse
            ead_tree = etree.parse(join(ead_folder, filename))
            # go through each of the elements at that xpath
            for name in ead_tree.xpath(name_xpath):
                # skip the ones without sources
                if not name.get('source'):
                    continue
                # otherwise add it to the dictionary
                else:
                    name_source_dictionary[name.text] = name.get('source')


'''
now add any sources in the dictionary to names that are missing them'''

# go through each of the files in the ead folder
for filename in tqdm(os.listdir(ead_folder)):
    # but only do the ones that are actually eads (we can tell because they are xml files)
    if filename.endswith('.xml'):
        # create an etree (part of lxml) tree that we can parse
        ead_tree = etree.parse(join(ead_folder, filename))
        # go through each of the elements at that xpath
        for name in ead_tree.xpath(name_xpath):
            # if it doesn't have a source and the name is in the dictionary we just created
            if not name.get('source') and name.text in name_source_dictionary:
                # add the appropriate source
                name.attrib['source'] = name_source_dictionary[name.text]
                # find the ead to update
                with open(os.path.join(ead_folder, filename), mode="w") as see_i_am_making_all_things_new:
                    # and write it
                    see_i_am_making_all_things_new.write(etree.tostring(ead_tree))
                 
                    
