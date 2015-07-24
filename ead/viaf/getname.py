'''
step one of https://github.com/mcarruthers/LCNAF-Named-Entity-Reconciliation
'''

import os
from os import path

# you'll need to install the following python modules -- should be as simple as running "pip install tqdm" and "pip install lxml" from the command-line
# lxml is a powerful xml document parser, and tqdm is used to show a command-line progress bar as the script progresses
from lxml import etree as ET
from tqdm import tqdm

# where are the eads?
ead_path = 'path/to/eads'

# tag names - set these to the tag types you want to capture the values of
tag_names = ["persname", "corpname", "geogname", "genreform"]

# initializes the dictionary we'll use to hold the tag names
controlaccess_term_dictionary = {}
for tag in tag_names:
	controlaccess_term_dictionary[tag] = []

# xpath to where in the ead document we'll be looking for the given tag names
controlaccess_xpath = '//controlaccess/*'

# go through the files
for filename in tqdm(os.listdir(ead_path)):
	# only look at xml files
	if filename.endswith(".xml"):
		# create lxml etree version of ead document
		ead_tree = ET.parse(path.join(ead_path, filename))

		# go through the ead and grab all the text appearing in the tag types defined above
		for sub in ead_tree.xpath(controlaccess_xpath):
			for tag in tag_names:
			    # we don't want to grab compound subject terms or empty strings
				if tag in sub.tag and sub.text is not None and "--" not in sub.text:
					controlaccess_term_dictionary[tag].append(sub.text.strip())

# write all the names to a file - one file for each tag type
for tag_type, names in controlaccess_term_dictionary.items():
	with open(tag_type + ".txt", mode="w") as text_file:
		for name in names:
			text_file.write(name.encode("utf-8") + '\n')
