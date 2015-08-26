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
famname_csv = 'agents-famname.csv'

# where is the csv that we'll record the original name and the new uri
famname_uris = 'famname-uris.csv'

# go ahead and create the headers of that csv
# open the csv in write mode
with open(famname_uris, 'wb') as famname_uris_csv_file:
    # set up the writer
    famname_uris_csv_file_writer = csv.writer(famname_uris_csv_file)
    # write the headers
    famname_uris_csv_file_writer.writerow(['ORIGINAL', 'uri'])

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
      "family_name": "Eckard",
      "prefix": "Prefix",
      "dates": "Dates",
      "qualifier": "Qualifer",
      "sort_name": "Eckard, Prefix, Dates (Qualifer)",
      "sort_name_auto_generate": true,
      "created_by": "admin",
      "last_modified_by": "admin",
      "create_time": "2015-08-26T15:55:22Z",
      "system_mtime": "2015-08-26T15:55:22Z",
      "user_mtime": "2015-08-26T15:55:22Z",
      "authorized": true,
      "is_display_name": true,
      "source": "lcnaf",
      "jsonmodel_type": "name_family",
      "use_dates": [
        
      ],
      "authority_id": "Authority ID"
    }
  ]'''

# open the famname csv in read mode
with open(famname_csv, 'r') as famname_csv_file:
    # read it to get the data
    famname_data = csv.reader(famname_csv_file)
    
    # skip the first row
    next(famname_data)
    
    # go through each row
    for row in famname_data:
        
        # match up fields to row index
        # original
        original = row[5]
        # family name
        family_name = row[7]
        # qualifier
        qualifier = row[9]
        # authority id
        authority_id = row[2]
        # source
        source = row[3]
        
        # set up list and dictionaries
        row_dictionary = {}
        # empty list for famname dictionaries
        famname_list = []
        # empty dictionary
        famname_dictionary = {}
        
        # add to dictionary
        # if family name exists
        if family_name:
            # append it
            famname_dictionary["family_name"] = family_name
        # if a qualifer exists
        if qualifier:
            # append it
            famname_dictionary["qualifier"] = qualifier
        # if authority id exists
        if authority_id:
            # add it to dictionary
            famname_dictionary["authority_id"] = authority_id
        # if source exists
        if source:
            # add it to dictionary
            famname_dictionary["source"] = source
                
        # add other required fields to dictionary
        # auto generate sort name
        famname_dictionary["sort_name_auto_generate"] = True
        
        # add dictionary to list
        famname_list.append(famname_dictionary)
        
        # add list to dictionary
        row_dictionary["names"] = famname_list
        
        
        '''
        create json out of this'''
        
        # create json
        famname_json = json.dumps(row_dictionary)
        print famname_json
        
       
        '''
        post it to archivesspace'''
        
        # post the famname
        famnames = requests.post(base_url + '/agents/families', headers = headers, data = famname_json).json()
        print famnames
        

        '''
        get uri and append it to new csv'''
        # write row of csv
        # open the csv in append mode
        with open(famname_uris, 'ab') as famname_uris_csv_file:
            # set up the writer
            famname_uris_csv_file_writer = csv.writer(famname_uris_csv_file)
            # write the headers
            if "status" in famnames:
                famname_uris_csv_file_writer.writerow([original, famnames["uri"]])
        