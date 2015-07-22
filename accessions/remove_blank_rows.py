'''
From A-Team meeting on 2015-07-22...

Check core fields: if blank, then it's probably not a good record
  * Name
  * Description
  * Processing status (?)
  
DECISION: Incomplete records of legacy accession are not valuable--it's OK if not all these go in.'''

import csv
import os

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
    for row in csv_temp_take_two_reader:
        #if there is no accessionid, the row is entirely blank
        accession_id = row[2]
        if len(accession_id) == 0:
            continue
        else:
            with open('C:/Users/Public/Documents/accessions/accessions-20150722-final.csv', 'ab') as csv_final_take_two:
                csv_final_take_two_writer = csv.writer(csv_final_take_two, dialect='excel')
                csv_final_take_two_writer.writerow(row)
                
# delete the temporary csv
os.remove('C:/Users/Public/Documents/accessions/accessions-20150722-temp.csv')
