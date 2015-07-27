# import what we need
import os
from os.path import join

# you'll need and want, respectively, to import the following python modules, i.e., pip install lxml and pip install tqdm
from lxml import etree as ET
from tqdm import *

# where are the eads?
ead_path = 'C:/Users/eckardm/GitHub/vandura/Real_Masters_all'

# xpath to where we'll be looking in each ead
container_xpath = '//container'

# go through all thie files in that directory
for filename in tqdm(os.listdir(ead_path)):
    # but only look at the xml files
    if filename.endswith('.xml'):
        # create a lxml etree version of the ead
        ead_tree = ET.parse(join(ead_path, filename))
        
        # look at each of the container elements
        for container_element in ead_tree.xpath(container_xpath):
            # and try and see if it has a label="Oversize Volume" attribute
            try: 
                if container_element.attrib['label'] == 'Oversize Volume':
                    # for now, just print
                    print filename
                    print container_element.attrib
            # if not, don't worry about it, just continue on
            except:
                continue
