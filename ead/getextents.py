# import what we need
from lxml import etree
import csv
import os
from os.path import join

# where are the eads?
ead_path = 'path/to/EADs' # <-- you have to change this

# where is the output csv?
output_csv = 'path/to/output.csv' # <-- you have to change this

# "top level" extents xpath
extents_xpath = '//ead/archdesc/did//physdesc/extent'
# component extents xpath
component_extents_xpath = '//ead/archdesc/dsc//physdesc/extent'
# all extents xpath
all_extents = '//extent'

# open and write header row of csv
with open(output_csv, 'ab') as csv_file:
    writer = csv.writer(csv_file, dialect='excel')
    writer.writerow(['Filename', 'XPath', 'Original Extent'])

# creates a function to get extents
def getextents(xpath):
    # go through those files
    for filename in os.listdir(ead_path):
        tree = etree.parse(join(ead_path, filename))
        # keep up with where we are
        print("Processing " + filename)
        # parse and go through all component extents
        extents = tree.xpath(xpath)
        for extent in extents:
            # identify blank extents
            extent_text = extent.text.encode("utf-8") if extent.text else ""
            extent_path = tree.getpath(extent)
            with open(output_csv, 'ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow([filename, extent_path, extent_text])
                
# get extents       
getextents(all_extents) # <-- you'll have to change this to get the extents you want, "top level," component level or all (i want all)
