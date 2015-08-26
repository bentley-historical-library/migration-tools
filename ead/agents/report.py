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


'''
do the reporting (we want to know how many there are, and a histogram of source attributes (including blanks), for all and just for controlaccess and origination ones)'''

# for each name elements
for name_xpath in name_xpaths:
    
    # first, set up a couple of counters and a dictionary
    # counter for total attributes
    total_elements = 0
    # counter for no source in total elements
    total_elements_no_source = 0
    # counter for attributes inside of controlaccess and origination
    elements_in_controlaccess_and_origination = 0
    # counter for no source in attributes inside of controlaccess and origination
    elements_in_controlaccess_and_origination_no_source = 0
    # initializes a histogram dictionary with one entry for blanks
    attributes_histogram = {'NO SOURCE': 1}
    
    # then, do some counting
    # go through each of the files in the ead folder
    for filename in tqdm(os.listdir(ead_folder)):
        # but only do the ones that are actually eads (we can tell because they are xml files)
        if filename.endswith('.xml'):
            # create an etree (part of lxml) tree that we can parse
            ead_tree = etree.parse(join(ead_folder, filename))
            # go through each of the elements at that xpath
            for name in ead_tree.xpath(name_xpath):
                # add 1 to the total
                total_elements += 1
                if not name.get('source'):
                        # add to new counter
                        total_elements_no_source += 1
                # if it is inside a controlaccess or origination elements
                if 'controlaccess' in ead_tree.getpath(name) or 'origination' in ead_tree.getpath(name):
                    # add 1 to that total
                    elements_in_controlaccess_and_origination += 1
                    # quick edit to count how many of these don't have sources
                    if not name.get('source'):
                        # add to new counter
                        elements_in_controlaccess_and_origination_no_source += 1
                # if there is no source attribute
                if not name.get('source'):
                    # add one to the no source key in the histogram dictionary
                    attributes_histogram['NO SOURCE'] += 1
                # else if the source attribute value is not a key in the histogram dictionary
                elif name.get('source') not in attributes_histogram:
                    # initialize it
                    attributes_histogram[name.get('source')] = 1
                # and if it already is
                else:
                    # add one to it
                    attributes_histogram[name.get('source')] += 1
   
    # finally, print everything out
    # skips a space for readability
    print '\n'
    # print what we're talking about
    print 'XPath: ', name_xpath
    # print the total
    print 'Total elements: ', total_elements
    # print the new count for no source
    print 'Number of total elements without sources: ', total_elements_no_source
    # print the total in controlaccess and origination
    print 'Sub-elements of <controlaccess> and <origination> elements', elements_in_controlaccess_and_origination
    # print the new count
    print 'Total number of sub-elements of without sources: ', elements_in_controlaccess_and_origination_no_source
    # print histogram dictionary
    print 'Attribute counts:'
    for key in attributes_histogram:
        print key + ': ' + str(attributes_histogram[key])
