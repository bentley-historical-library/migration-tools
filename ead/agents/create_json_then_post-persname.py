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
persname_csv = 'agents-persname.csv'

# where is the csv that we'll record the original name and the new uri
persname_uris = 'persname-uris.csv'

# go ahead and create the headers of that csv
# open the csv in write mode
with open(persname_uris, 'wb') as persname_uris_csv_file:
    # set up the writer
    persname_uris_csv_file_writer = csv.writer(persname_uris_csv_file)
    # write the headers
    persname_uris_csv_file_writer.writerow(['ORIGINAL', 'uri'])

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
      "title": "Title",
      "prefix": "Prefix",
      "rest_of_name": "Rest of Name",
      "suffix": "Suffix",
      "fuller_form": "Fuller Form",
      "number": "Number",
      "dates": "Dates",
      "qualifier": "Qualifier",
      "sort_name": "Primary Part of Name, Rest of Name, Prefix, Suffix, Title, Number (Fuller Form), Dates (Qualifier)",
      "sort_name_auto_generate": true,
      "created_by": "admin",
      "last_modified_by": "admin",
      "create_time": "2015-08-26T16:08:03Z",
      "system_mtime": "2015-08-26T16:08:03Z",
      "user_mtime": "2015-08-26T16:08:03Z",
      "authorized": true,
      "is_display_name": true,
      "source": "lcnaf",
      "name_order": "inverted",
      "jsonmodel_type": "name_person",
      "use_dates": [
        
      ],
      "authority_id": "Authority ID DELETE"
    }
  ]'''

# open the persname csv in read mode
with open(persname_csv, 'r') as persname_csv_file:
    # read it to get the data
    persname_data = csv.reader(persname_csv_file)
    
    # skip the first row
    next(persname_data)
    
    # go through each row
    for row in persname_data:
        
        # match up fields to row index
        # original
        original = row[0]
        # prefix
        prefix = row[1]
        # title
        title = row[2]
        # primary name
        primary_name = row[3]
        # rest of name
        rest_of_name = row[4]
        # suffix
        suffix = row[5]
        # number
        number = row[6]
        # fuller form
        fuller_form = row[7]
        # dates
        dates = row[8]
        # authority id
        authority_id = row[9]
        # source
        source = row[10]
        
        # set up list and dictionaries
        row_dictionary = {}
        # empty list for persname dictionaries
        persname_list = []
        # empty dictionary
        persname_dictionary = {}
        
        # add to dictionary
        # if family name exists
        if prefix:
            # append it
            persname_dictionary["prefix"] = prefix
        # if a title exists
        if title:
            # append it
            persname_dictionary["title"] = title
        # if a primary name exists
        if primary_name:
            # append it
            persname_dictionary["primary_name"] = primary_name
        # if rest of name exists
        if rest_of_name:
            # append it
            persname_dictionary["rest_of_name"] = rest_of_name
        # if suffix exists
        if suffix:
            # append it
            persname_dictionary["suffix"] = suffix
        # if number exists
        if number:
            # append it
            persname_dictionary["number"] = number
        # if fuller form exists
        if fuller_form:
            # append it
            persname_dictionary["fuller_form"] = fuller_form
        # if dates exists
        if dates:
            # append them
            persname_dictionary["dates"] = dates
        # if authority id exists
        if authority_id:
            # add it to dictionary
            persname_dictionary["authority_id"] = authority_id
        # if source exists
        if source:
            # add it to dictionary
            persname_dictionary["source"] = source
                
        # add other required fields to dictionary
        # auto generate sort name
        persname_dictionary["sort_name_auto_generate"] = True
        # name order
        persname_dictionary["name_order"] = "inverted"
        
        # add dictionary to list
        persname_list.append(persname_dictionary)
        
        # add list to dictionary
        row_dictionary["names"] = persname_list
        
        
        '''
        create json out of this'''
        
        # create json
        persname_json = json.dumps(row_dictionary)
        print persname_json
        
       
        '''
        post it to archivesspace'''
        
        # post the persname
        persnames = requests.post(base_url + '/agents/people', headers = headers, data = persname_json).json()
        print persnames
        

        '''
        get uri and append it to new csv'''
        # write row of csv
        # open the csv in append mode
        with open(persname_uris, 'ab') as persname_uris_csv_file:
            # set up the writer
            persname_uris_csv_file_writer = csv.writer(persname_uris_csv_file)
            # write the headers
            if "status" in persnames:
                persname_uris_csv_file_writer.writerow([original, persnames["uri"]])
        