'''
first things first, import what we need'''

# lxml is a powerful xml document parser, you'll need to download it
from lxml import etree

# os provides a portable way of using operating system dependent functionality
import os
from os.path import join


'''
setup'''

# where are the eads?
ead_folder = 'C:/Users/eckardm/GitHub/vandura/Real_Masters_all'

# xpaths list for names (persname, corpname and famname elements)
name_xpaths = ['//persname', '//corpname', '//famname']


'''
do the reporting (we want to know how many there are, and a histogram of source attributes (including blanks), for all and just for controlaccess and origination ones)'''

# for each name elements
for name_xpath in name_xpaths:
    print '\n' + name_xpath
    # go through each of the files in the ead folder
    for filename in os.listdir(ead_folder) :
        # but only do the ones that are actually eads (we can tell because they are xml files)
        if filename.endswith('.xml'):
            # create an etree (part of lxml) tree that we can parse
            ead_tree = etree.parse(join(ead_folder, filename))
            # go through each of the elements at that xpath
            for name in ead_tree.xpath(name_xpath):
                # if it doesn't have a source and the name is in the dictionary we just created
                if 'controlaccess' in ead_tree.getpath(name) or 'origination' in ead_tree.getpath(name):
                    if not name.get('source'):
                        print name.text
                    