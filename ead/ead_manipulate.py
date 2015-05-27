from lxml import etree
from os import listdir, path

def prettify_xml_in_directory(input_directory, output_directory):
    # WARNING: will overwrite files in the output directory if there are filename conflicts
    parser = etree.XMLParser(remove_blank_text=True)
    for filename in listdir(input_directory):
        if filename.endswith(".xml"):
            print("prettifying {0}...".format(filename))
            xml = etree.parse(path.join(input_directory, filename), parser)
            with open(output_directory + filename, mode='w') as f:
                f.write(etree.tostring(xml, pretty_print=True))

def remove_node(lxml_etree_node):
    lxml_etree_node.getparent().remove(lxml_etree_node)


def get_c0x_parent_xpath(full_ead_xml_as_etree, xpath_of_source_node):
    c0x_parent = full_ead_xml_as_etree.xpath(xpath_of_source_node)[0]

    is_c0x_level = False
    while not is_c0x_level:
        if c0x_parent.tag.startswith("c0"):
            is_c0x_level = True
        else:
            c0x_parent = c0x_parent.getparent()

    xpath = full_ead_xml_as_etree.getpath(c0x_parent)
    return xpath


def get_upper_c0x_neighbor_xpath(full_ead_xml_as_etree, xpath_of_source_node):
    """
    "Upper c0x neighbor" refers to whatever tag starting with "c0" first appears above the source node's parent c0x tag. 
    This can be either a parent or a sibling.
    """

    # find the parent c0x node of the passed xpath element
    c0x_parent_xpath = get_c0x_parent_xpath(full_ead_xml_as_etree, xpath_of_source_node)

    # See if the c0x parent has a c0x sibling above it. If not, return its own parent.
    upper_siblings = full_ead_xml_as_etree.xpath(c0x_parent_xpath + "/preceding-sibling::*")
    parent = full_ead_xml_as_etree.xpath(c0x_parent_xpath)[0].getparent()
    if len(upper_siblings) == 0:
        return full_ead_xml_as_etree.getpath(parent)
    else:
        for sibling in reversed(upper_siblings):
            if sibling.tag.startswith("c0"):
                return full_ead_xml_as_etree.getpath(sibling)
        return full_ead_xml_as_etree.getpath(parent)



def insert_node_into_upper_c0x_neighbor(full_ead_xml_as_etree, xpath_of_node_to_move, copy_full_hierarchy_up_to_c0x_parent=True):
    """
    Cuts and copies a target node into its upper c0x-level neighbor. Can either move the exact node only, or the node and its
    full parent hierarchy all the way up to its first c0x parent.
    
    :param full_ead_xml_as_etree: lxml etree object representing the full EAD file
    :param xpath_of_node_to_move: exact xpath to the node you are moving
    :param copy_full_hierarchy_up_to_c0x_parent: :bool:
            If true, it finds parent tags of the node to move between it and its nearest c0x parent, then recreates that
            structure in the c0x node it is moving to. This does not overwrite any tags already present.
            For example, if the node to move is at /ead/archdesc/dsc/c01/c02/did/physdesc/extent and the node to copy to
            is at /ead/archdesc/dsc/c01/, then the full did/physdesc/extent hierarchy will be copied into the new location.
            If there is already a <did> tag at the c01 level, the physdesc/extent is appended into it.
            If false, only the target tag is copied into the upper neighbor. The result of the above situation would be
            /ead/archdesc/dsc/c01/extent, instead of /ead/archdesc/dsc/c01/did/physdesc/extent
    """
    upper_neighbor_xpath = get_upper_c0x_neighbor_xpath(full_ead_xml_as_etree, xpath_of_node_to_move)
    upper_neighbor = full_ead_xml_as_etree.xpath(upper_neighbor_xpath)[0]

    if copy_full_hierarchy_up_to_c0x_parent:
        tag_c0x_parent_xpath = get_c0x_parent_xpath(full_ead_xml_as_etree, xpath_of_node_to_move)
        subpath_from_c0x_parent_to_tag = xpath_of_node_to_move.split(tag_c0x_parent_xpath)[1]
        print(subpath_from_c0x_parent_to_tag)
        print(xpath_of_node_to_move)
        print(tag_c0x_parent_xpath)
        print(upper_neighbor_xpath)

        subpaths = []
        for path in subpath_from_c0x_parent_to_tag.split("/")[1:]:
            subpaths.append(path.split("[")[0])
        print(subpaths)

        subpath = ""
        new_path = upper_neighbor_xpath
        for path in subpaths:
            new_path += "/" + path
            xpath_result_list = full_ead_xml_as_etree.xpath(new_path)
            if len(xpath_result_list) > 0:
                subpath += "/" + path
                continue
            else:
                print("I appended")
                print(tag_c0x_parent_xpath + subpath + "/" + path)

                node = full_ead_xml_as_etree.xpath(tag_c0x_parent_xpath + subpath + "/" + path)[0]
                full_ead_xml_as_etree.xpath(upper_neighbor_xpath + subpath)[0].append(node)
                print(etree.tostring(full_ead_xml_as_etree, pretty_print=True))
                break

    else:
        print(xpath_of_node_to_move)
        upper_neighbor.insert(1, full_ead_xml_as_etree.xpath(xpath_of_node_to_move)[0])
        print(etree.tostring(full_ead_xml_as_etree, pretty_print=True))


def does_text_in_given_tag_change_in_upper_c0x_neighbor(full_ead_xml_as_etree, tag_xpath):
    tag_texts = []
    upper_neighbor_tag_texts = []

    tag_c0x_parent_xpath = get_c0x_parent_xpath(full_ead_xml_as_etree, tag_xpath)
    subpath_from_c0x_parent_to_tag = tag_xpath.split(tag_c0x_parent_xpath)[1]

    # un = upper neighbor
    un_xpath = get_upper_c0x_neighbor_xpath(full_ead_xml_as_etree, tag_c0x_parent_xpath)
    un_equivalent_tag_xpath = un_xpath + subpath_from_c0x_parent_to_tag

    tag_etree_list = full_ead_xml_as_etree.xpath(tag_xpath)
    un_tag_etree_list = full_ead_xml_as_etree.xpath(un_equivalent_tag_xpath)

    for etree in tag_etree_list:
        tag_texts.append(etree.text)
    for etree in un_tag_etree_list:
        upper_neighbor_tag_texts.append(etree.text)

    if tag_texts == upper_neighbor_tag_texts:
        return False
    else:
        return True
