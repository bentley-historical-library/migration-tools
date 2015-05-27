# Script to find component (<c0x> level) elements that do not have ArchivesSpace-acceptable titles

import lxml
from lxml import etree
import os
from os.path import join
 
# Enter the path to the folder containing your EADs
path = 'path/to/EADs'
 
# Check each file in the EAD folder
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for cs in tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]"): # Check each <c0x> componenet
        t = cs.xpath("./did[1]//unittitle/text()") # Check for a unittitle
        subt = cs.xpath("./did[1]//unittitle/*/text()") # Check for a nested title within a unittitle
        d = cs.xpath("./did[1]//unitdate/text()") # Check for a unitdate
        titlepath = tree.getpath(cs)
        if len(t) == 0 and len(subt) == 0 and len(d) == 0: # Output an error message if all possible titles are missing
            print filename + ' is missing a component title at ' + titlepath # Error message contains filename and xpath to missing component title
