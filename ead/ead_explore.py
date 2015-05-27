import csv, re
from string import ascii_letters
from os import listdir
from lxml import etree


def split_sentence_into_parts(sentence):
	# sentence-splitting function, built to help characterize long extent statements containing multiple discrete extents
	# returns a list of discrete items in the sentence

	clauses = sentence.split(",")
	clauses = filter(None, [item for clause in clauses for item in clause.split(" and ")])
	clauses = filter(None, [item for clause in clauses for item in clause.split(" (")])
	clauses = ["(" + clause if clause.endswith(")") else clause for clause in clauses]

	discrete_items = []
	for clause in clauses:
		clause = clause.strip(" \t\n")
		if clause.startswith("and "):
			clause = clause[4:]

		discrete_items.append(clause)

	return discrete_items


def normalize_extent_list(discrete_extents, include_size=False):
	# Normalizes a list of extents by type, returning the results in a new list
	# If include_size is set to True, it will also record the accompanying size of the extent, returning the results
	# as a list of lists

	normalized_extents = []
	num_replace_regex = re.compile(r"(\d\d?\d?\d?) ")
	extent_size_regex = re.compile(r"^(\d\d?\d?\d?\.?\d?\d?) ")
	for extent in discrete_extents:
		extent_size = 0
		# check if extent name is entirely numerical
		if all(letter not in extent for letter in ascii_letters):
			extent_name = extent.rstrip(".")
		# account for edge-case
		elif "-inch" in extent[:10]:
			extent_name = extent[2:]
		# otherwise,
		else:
			try:
				extent_size = float(re.findall(extent_size_regex, extent.lstrip("ca. "))[0])
			except:
				print("failed to find extent size for" + ": " + extent)
			extent_name = extent.lstrip("0123456789 .+").rstrip(".")
			extent_name = re.sub(num_replace_regex, "[x] ", extent_name)

		if include_size:
			normalized_extents.append([extent_name, extent_size])
		else:
			normalized_extents.append(extent_name)

	return normalized_extents



def characterize_series_in_directory(source_directory):
	series = {}
	for filename in listdir(source_directory):
		if filename.endswith(".xml"):
			print(filename)
			tree = etree.parse(source_directory + "\\" + filename)
			inventory = tree.xpath("/ead/archdesc/dsc")[0]
			attribute_paths = build_xml_tree_tag_paths(inventory)
			for key, value in attribute_paths.items():
				if key in series:
					series[key] += value
				else:
					series[key] = value
	write_sorted_histogram(series, "series_exploration.csv")


def build_xml_tree_tag_paths(etree_of_full_ead_dsc_node, tag="c0", attribute="level"):
	# Recursive function built to help characterize all possible c0x "level" hierarchies found in our EAD documents.
	# could be generalized to characterize the hierarchy of any regular attribute in any self-nesting tag by changing
	# the "tag" and "attribute" default values
	#
	# returns a dictionary containing each unique path, and a count of its instances

	series = {}
	parent_etree_nodes = list(etree_of_full_ead_dsc_node)
	path_breadcrumb_list = []

	# recursion function
	def recurse_down_tree(node):
		path_breadcrumb_string = "->".join([str(level) for level in path_breadcrumb_list])

		# add current level to series breadcrumb path
		path_breadcrumb_list.append(node.get(attribute))

		# for each child in the current node that starts with c0, recurse
		for child in list(node):
			if child.tag.startswith(tag):
				recurse_down_tree(child)

		# if none of the current node's child tags start with c0, record the full path to node, and move on
		if all([not child.tag.startswith(tag) for child in list(node)]):
			key = "{0}->{1}".format(path_breadcrumb_string, node.get(attribute))
			key = key.lstrip("->") # bit of a hack-ish fix to remove leading arrows

			# add full series path to the recording dictionary if it isn't there already; else increment its count
			if key in series:
				series[key] += 1
			else:
				series[key] = 1

		# if the code reaches this point, this is the end of this branch of the tree, so remove this leaf of the tree
		# from the path breadcrumb list
		path_breadcrumb_list.pop()

	for node in parent_etree_nodes:
		if node.tag.startswith("c0"):
			recurse_down_tree(node)

	return series


def build_histogram_dict(list_of_items, with_item_size=False):
	# given a list of items, builds a histogram of item frequency within that list
	# optionally can be given of list of item lists, in the format [item_name (a string), item_size (a number)], and will record cumulative
	# size along with pure instance counts.

	histogram_dict = {}
	for item in list_of_items:
		if with_item_size:
			item_name = item[0]
			item_size = float(item[1])
			if item_name not in histogram_dict:
				histogram_dict[item_name] = [1, item_size]
			else:
				histogram_dict[item_name][0] += 1
				histogram_dict[item_name][1] += item_size
		else:
			item_name = item
			if item_name not in histogram_dict:
				histogram_dict[item_name] = 1
			else:
				histogram_dict[item_name] += 1
	return histogram_dict


def write_sorted_histogram(histogram_dict, filename, with_item_size=False):
	"""
	Sorts a histogram dictionary by EAD instance count and item name, then writes that date to a csv file
	:param histogram_dict: A dictionary whose key is a unique string, and whose value is either a numerical count value
						   or a list containing [instance_counts, cumulative_size]
	:param filename:       String containing the name of the file to write. Will overwrite any existing file with that name.
	:param with_item_size: Boolean describing whether the values of the passed histogram_dict also contain cumulative
						   item size counts
	"""

	if with_item_size:
		sorted_hist_data_as_list = sorted(sorted([(key, value[0], value[1]) for key, value in histogram_dict.items()],
		                                         key=lambda x: x[0]), key=lambda x: -x[1][0])
	else:
		sorted_hist_data_as_list = sorted(sorted([(key, value) for key, value in histogram_dict.items()],
	                                             key=lambda x: x[0]), key=lambda x: -x[1])

	with open(filename, mode="wb") as f:
		writer = csv.writer(f)
		if with_item_size:
			header = ["name", "number of appearances within EADs", "cumulative size"]
		else:
			header = ["name", "number of appearances within EADs"]
		writer.writerow(header)
		writer.writerows(sorted_hist_data_as_list)
