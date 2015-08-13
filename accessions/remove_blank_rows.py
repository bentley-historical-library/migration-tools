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
csv_exported = open('C:/Users/Public/Documents/accessions/accessions_20150729.csv', 'rb')
csv_exported_data = csv_exported.read()
csv_exported.close()

csv_temp = open('C:/Users/Public/Documents/accessions/accessions-20150729-temp.csv','wb')
csv_temp.write(csv_exported_data.replace('\x00', ''))
csv_temp.close()

# rewrite the csv, removing blank rows
with open('C:/Users/Public/Documents/accessions/accessions-20150729-temp.csv','rb') as csv_temp_take_two:
    csv_temp_take_two_reader = csv.reader(csv_temp_take_two)
    for row in csv_temp_take_two_reader:
        # if there is no accessionid, the row is entirely blank
        accession_id = row[2]
        # dates
        accession_date = row[1]
        # core fields
        donornumberid = row[9]

        accession_description = row[0]
        processing_status = row[35]
        # logic
        if len(accession_id) == 0:
            continue
        if len(accession_date) == 0 and processing_status == 'Backlog':
            with open('C:/Users/Public/Documents/accessions/accessions-20150729-final.csv', 'ab') as csv_final_take_two:
                csv_final_take_two_writer = csv.writer(csv_final_take_two, dialect='excel')
                csv_final_take_two_writer.writerow(row)
        if len(accession_date) == 0 and len(accession_description) == 0 and len(donornumberid) == 0:
            continue
        else:
            with open('C:/Users/Public/Documents/accessions/accessions-20150729-final.csv', 'ab') as csv_final_take_two:
                csv_final_take_two_writer = csv.writer(csv_final_take_two, dialect='excel')
                csv_final_take_two_writer.writerow(row)

# delete the temporary csv
os.remove('C:/Users/Public/Documents/accessions/accessions-20150729-temp.csv')
