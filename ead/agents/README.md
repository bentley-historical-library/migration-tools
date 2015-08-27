Agents
======

The following scripts and CSVs take Agents (ArchivesSpace-speak) or Names (Archivist's Toolkit-speak) in our EADs and import them to ArchivesSpace. This is a three step process:

  1. get agents (that is, corpname, famname and persname subelements of controlaccess and origination elements)from our EADs; 
  2. use OpenRefine (or, in the case of persname elements, a separate script) to parse them out into the different parts that ArchivesSpace expects (for example, in the case of corpname elements, primary name, subordinate name one and subordinate name two); and
  3. build the JSON that the ArchivesSpace API expects and programmatically add the agents to ArchivesSpace, recording the URI that ArchivesSpace generates so that it can be re-incorporated into the EAD later.
  
There are also a number of micellaneous scripts that were used during cleanup and to generate reports.

Get Agents
----------

### getsubjects.py

Goes through our EADs, generates a list of dictionaries of unique agent elements, and uses this dictionary to generate the **corpname.csv**, **famname.csv*** and **persname.csv*** CSVs to be used in OpenRefine. The section that generates the **persname.csv** CSV is currently commented out because Walker took this over (see Walker's [persname parsing scripts](https://github.com/walkerdb/bentley_code/tree/master/main_projects/persname_parsing).

### corpname.csv

Output of the **getsubjects.py** script for corpname elements.

### famname.csv

Output of the **getsubjects.py** script for famname elements.

### persname.csv

Output of the **getsubjects.py** script for persname elements.

Parse Agents
------------

### corpname.json

OpenRefine JSON used for parsing the **corpname.csv** CSV.

### agents-corpname.csv

Output of OpenRefine after **corpname.json** has been used.

### famname.json

OpenRefine JSON used for parsing the **famname.csv** CSV.

### agents-famname.csv

Output of OpenRefine after **famname.json** has been used.

### agents-persname.csv

What we're left with after Walker's persname parsing scripts.

Post Agents
-----------

This was inspired by Dallas's [post subjects script](https://github.com/djpillen/bentley_scripts/blob/master/post_subjects.py). 

### create_json_then_post-corpname.py

Creates the JSON expected by the ArchivesSpace API for corpname elements, programmatically posts them to ArchivesSpace and returns the **corpname-uris.csv** CSV with the URI for each unique subject.

### corpname-uris.csv

Output of the **create_json_then_post-corpname.py** script.

### create_json_then_post-famname.py

Creates the JSON expected by the ArchivesSpace API for famname elements, programmatically posts them to ArchivesSpace and returns the **famname-uris.csv** CSV with the URI for each unique subject.

### famname-uris.csv

Output of the **create_json_then_post-famname.py** script.

### create_json_then_post-persname.py

Creates the JSON expected by the ArchivesSpace API for persname elements, programmatically posts them to ArchivesSpace and returns the **persname-uris.csv** CSV with the URI for each unique subject.

### persname-uris.csv

Output of the **create_json_then_post-persname.py** script.

Miscellaneous
-------------

### check_geogname.py

There were some corpname elements that looked suspiciously like geogname elements. 

This script goes through the **corpname.csv** CSV to check to see if any of the corpname elements return hits through the VIAF API.

### make_name_source_dictionary.py

Many agents had missing or inaccurate source attributes. 

This script goes through the EADs and builds a dictionary of agents and their source attributes. It then then goes back through the EADs and tries to add the appropriate source attribute to any source that's missing one. 

### no_source_report.py

Many agents had missing or inaccurate source attributes. 

This script generates a simple report of agents that don't have source attributes.

### report.py

Many agents had missing or inaccurate source attributes. 

This script generates a simple report of agents and the variety and number of their source attributes.

### update_corpnames.py

Many agents had missing or inaccurate source attributes. 

This script goes through the EADs and builds adds a source attribute value of "lcnaf" to any remaining coprname elements.

### update_persnames.py

This script goes through the EADs and builds adds a source attribute value of "lcnaf" to any remaining persname elements.