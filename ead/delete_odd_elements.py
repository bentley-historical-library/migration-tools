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
                    # find "cousin" paragraph tags in odd, first by getting xpath for that particular container
                    oversize_volume_xpath = ead_tree.getpath(container_element)
                    # then replacing did/container with odd/p to get cousin paragraph xpath
                    cousin_paragraph_xpath = oversize_volume_xpath.replace('did/container', 'odd/p')
                    # now let's check the text at that xpath
                    cousin_paragraph = ead_tree.xpath(cousin_paragraph_xpath)[0].text
                    print filename
                    print container_element.attrib
                    print cousin_paragraph_xpath
                    print cousin_paragraph
            # if not, don't worry about it, just continue on
            except:
                continue
