'''
first things first, import what we need'''

# requests takes all of the work out of python http making your integration with web services seamless, you'll need to install it
import requests

# csv implements classes to read and write tabular data in csv format
import csv

# json is a lightweight data interchange format inspired by javascript object literal syntax
import json


'''
preliminaries'''

# where is the csv that has been exported from openrefine?
corpname_csv = 'agents-corpname.csv'

# where is the csv that we'll record the original name and the new uri
corpname_uris = 'corpname-uris.csv'

# go ahead and create the headers of that csv
# open the csv in write mode
with open(corpname_uris, 'wb') as corpname_uris_csv_file:
    # set up the writer
    corpname_uris_csv_file_writer = csv.writer(corpname_uris_csv_file)
    # write the headers
    corpname_uris_csv_file_writer.writerow(['ORIGINAL', 'uri'])

# preliminaries for using archivesspace api
# base url
base_url = 'http://localhost:8089'
# username default
username = 'admin'
# password default
password = 'admin'


'''
set up session in archivesspace using requests'''

# get authorization and return as json
authorization = requests.post(base_url + '/users/' + username + '/login?password=' + password).json()
# get the session token
session_token = authorization["session"]
# create the headers we'll need for posting
headers = {'X-ArchivesSpace-Session': session_token}


'''
go through csv, create a list of dictionaries for each entry'''


'''
for reference

 "names": [
    {
      "lock_version": 0,
      "primary_name": "Primary Part of Name",
      "subordinate_name_1": "Subordinate Name 1",
      "subordinate_name_2": "Subordinate Name 2",
      "number": "Number",
      "dates": "Dates",
      "qualifier": "Qualifier",
      "sort_name": "Primary Part of Name. Subordinate Name 1. Subordinate Name 2 (Number : Dates) (Qualifier)",
      "sort_name_auto_generate": true,
      "created_by": "admin",
      "last_modified_by": "admin",
      "create_time": "2015-08-26T13:47:36Z",
      "system_mtime": "2015-08-26T13:47:36Z",
      "user_mtime": "2015-08-26T13:47:36Z",
      "authorized": true,
      "is_display_name": true,
      "source": "naf",
      "jsonmodel_type": "name_corporate_entity",
      "use_dates": [
        
      ],
      "authority_id": "Authority ID"
    }
  ]'''

# open the corpname csv in read mode
with open(corpname_csv, 'r') as corpname_csv_file:
    # read it to get the data
    corpname_data = csv.reader(corpname_csv_file)
    
    # skip the first row
    next(corpname_data)
    
    # go through each row
    for row in corpname_data:
        
        # match up fields to row index
        # original
        original = row[5]
        # primary name
        primary_name = row[6]
        # subordinate name 1
        subordinate_name_1 = row[7]
        # subordinate name 2
        subordinate_name_2 = row[8]
        # qualifier
        qualifier = row[11]
        # authority id
        authority_id = row[2]
        # source
        source = row[3]
        
        # set up list and dictionaries
        row_dictionary = {}
        # empty list for corpname dictionaries
        corpname_list = []
        # empty dictionary
        corpname_dictionary = {}
        
        # add to dictionary
        # if primary name exists
        if primary_name:
            # append it
            corpname_dictionary["primary_name"] = primary_name
        # if subordinate name exists
        if subordinate_name_1:
            # append it
            corpname_dictionary["subordinate_name_1"] = subordinate_name_1
        # if a second subordinate name exists
        if subordinate_name_2:
            # append it
            corpname_dictionary["subordinate_name_2"] = subordinate_name_2
        # if a qualifer exists
        if qualifier:
            # append it
            corpname_dictionary["qualifier"] = qualifier
        # if authority id exists
        if authority_id:
            # add it to dictionary
            corpname_dictionary["authority_id"] = authority_id
        # if source exists
        if source:
            # add it to dictionary
            corpname_dictionary["source"] = source
                
        # add other required fields to dictionary
        # auto generate sort name
        corpname_dictionary["sort_name_auto_generate"] = True
        
        # add dictionary to list
        corpname_list.append(corpname_dictionary)
        
        # add list to dictionary
        row_dictionary["names"] = corpname_list
        
        
        '''
        create json out of this'''
        
        # create json
        corpname_json = json.dumps(row_dictionary)
        print corpname_json
        
       
        '''
        post it to archivesspace'''
        
        # post the corpname
        corpnames = requests.post(base_url + '/agents/corporate_entities', headers = headers, data = corpname_json).json()
        print corpnames
        

        '''
        get uri and append it to new csv'''
        # write row of csv
        # open the csv in append mode
        with open(corpname_uris, 'ab') as corpname_uris_csv_file:
            # set up the writer
            corpname_uris_csv_file_writer = csv.writer(corpname_uris_csv_file)
            # write the headers
            if "status" in corpnames:
                corpname_uris_csv_file_writer.writerow([original, corpnames["uri"]])
        