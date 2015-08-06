# import what we need
import os

from lxml import etree
from tqdm import tqdm

# requires the constants.py file made by the makedictionary.py script
from constants import persnames_dictionary
from constants import corpnames_dictionary


# where is your ead input directory, and where will you be saving the changed files to?
input_dir = 'path/to/your/eads'
output_dir = 'path/to/your/desired/output/directory'


# create the master authority dictionary by combining the persname and corpname dictionaries
auth_dict = persnames_dictionary.copy()
auth_dict.update(corpnames_dictionary)


# function to add auth IDs to matching controlaccess tags
def write_ids_to_ead(auth_dict, input_dir, output_dir):
    # the tags we're looking for
    tags = ['corpname', 'persname']

    # go through every ead in the input directory
    for ead in tqdm(os.listdir(input_dir)):
        
        # only parse xml files in the input directory
        if ead.endswith(".xml"):
            
            # parse the ead xml into an lxml etree for processing
            tree = etree.parse(os.path.join(input_dir, ead))

            # iterate through every tag inside of a <controlaccess> parent
            for controlaccess_child in tree.xpath('//controlaccess/*'):
                
                # only process the child tag if its tag type is in our list of desired tags
                if any([controlaccess_child.tag in tag for tag in tags]):
                    
                    # if the authority dictionary file has a key for this tag's text, then add that auth data to this tag
                    if controlaccess_child.text in auth_dict:
                        auth_key = controlaccess_child.text
                        lc_address = auth_dict[auth_key]

                        # set the authfilenumber attribute to the Library of Congress authority address
                        controlaccess_child.attrib['authfilenumber'] = lc_address

            with open(os.path.join(output_dir, ead), mode="w") as f:
                f.write(etree.tostring(tree, pretty_print=True))

write_ids_to_ead(auth_dict, input_dir, output_dir)
