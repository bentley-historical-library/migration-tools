from lxml import etree
import os
from os.path import join

def prettify_xml_in_directory(input_directory, output_directory):
  # WARNING - will overwrite files in the output directory if there are any name conflicts
    parser = etree.XMLParser(remove_blank_text=True)
    for filename in os.listdir(input_directory):
        if filename.endswith(".xml"):
            print("Prettifying {0}...".format(filename))
            xml = etree.parse(join(input_directory, filename), parser)
            with open(output_directory + filename, mode='w') as f:
                f.write(etree.tostring(xml, pretty_print=True))
