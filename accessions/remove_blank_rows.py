import csv

# we need to rewrite this csc with no null bytes
exported = open('beal_export_20150710-copy.csv','rb')
data = exported.read()
exported.close()

no_nulls = open('beal_export_20150710-nonull.csv','wb')
no_nulls.write(data.replace('\x00',''))
no_nulls.close()

# add the accessions fields header information, since BEAL does not
accession_fields = []
with open('accessionfields.txt','r') as accfields:
    for line in accfields:
        accession_fields.append(line.strip())

with open('beal_export_20150710-noblanks.csv', 'ab') as csvfinal:
    writer = csv.writer(csvfinal, dialect='excel')
    writer.writerow(accession_fields)


# rewrite the csv, removing blank rows
with open('beal_export_20150710-nonull.csv','rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        #if there is no accessionid, the row is entirely blank
        if len(row[2]) == 0:
            continue
        else:
            with open('beal_export_20150710-noblanks.csv', 'ab') as csvout:
                writer = csv.writer(csvout, dialect='excel')
                writer.writerow(row)
