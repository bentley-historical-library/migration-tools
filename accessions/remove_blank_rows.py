'''
From A-Team meeting on 2015-07-22 regarding accessions without dates...

Check core fields: if blank, then it's probably not a good record
  * Name
  * Description
  * Processing status (?)
  
DECISION: Incomplete records of legacy accession are not valuable--it's OK if not all these go in.'''

import csv
import os
from tqdm import *

# we need to rewrite this csv with no null bytes
csv_exported = open('C:/Users/Public/Documents/accessions/accessions-20150722-original.csv', 'rb')
csv_exported_data = csv_exported.read()
csv_exported.close()

csv_temp = open('C:/Users/Public/Documents/accessions/accessions-20150722-temp.csv','wb')
csv_temp.write(csv_exported_data.replace('\x00', ''))
csv_temp.close()

# add the accessions fields header information, since BEAL does not
accession_fields_list = []
with open('accessionfields.txt', 'r') as accession_fields:
    for accession_field in accession_fields:
        accession_fields_list.append(accession_field)

with open('C:/Users/Public/Documents/accessions/accessions-20150722-final.csv', 'ab') as csv_final:
    csv_final_writer = csv.writer(csv_final, dialect='excel')
    csv_final_writer.writerow(accession_fields_list)

# rewrite the csv, removing blank rows
with open('C:/Users/Public/Documents/accessions/accessions-20150722-temp.csv','rb') as csv_temp_take_two:
    csv_temp_take_two_reader = csv.reader(csv_temp_take_two)
    for row in tqdm(csv_temp_take_two_reader, total=19253):
        # if there is no accessionid, the row is entirely blank
        accession_id = row[2]
        # dates
        accession_date = row[1]
        # core fields
        contact = []
        first_name = row[20]
        if len(first_name) > 0:
            contact.append(first_name)
        last_name = row[21]
        if len(last_name) > 0:
            contact.append(last_name)
        middle_name = row[22]
        if len(middle_name) > 0:
            contact.append(middle_name)
        organization_or_unit = row[23]
        if len(organization_or_unit) > 0:
            contact.append(organization_or_unit)
        suffix = row[24]
        if len(suffix) > 0:
            contact.append(suffix)
        title = row[25]    
        if len(title) > 0:
            contact.append(title)
        accession_description = row[0]
        processing_status = row[35]
        # logic
        if len(accession_id) == 0:
            continue
        if len(accession_date) == 0:
            if len(contact) == 0 and len(accession_description) == 0:
                continue
            if len(processing_status) == 0 or processing_status.strip() == 'Completed':
                continue
        else:
            with open('C:/Users/Public/Documents/accessions/accessions-20150722-final.csv', 'ab') as csv_final_take_two:
                csv_final_take_two_writer = csv.writer(csv_final_take_two, dialect='excel')
                csv_final_take_two_writer.writerow(row)
                
# delete the temporary csv
os.remove('C:/Users/Public/Documents/accessions/accessions-20150722-temp.csv')
