# import what we need
import csv
import urllib2
import time

# viaf api parts
viaf_api_url_part_1 = 'http://viaf.org/viaf/search?query=local.geographicNames+all+"'
viaf_api_url_part_2 = '"+and+local.sources+any+"lc"&sortKeys=holdingscount&recordSchema=BriefVIAF'

# open the csv
with open('corpname.csv', 'r') as corpname_csv:
    # read it
    corpname_csv_reader = csv.reader(corpname_csv)
    # skip the first row
    next(corpname_csv_reader)
    # and go through each row
    for row in corpname_csv_reader:
        # identify the original
        original = row[5]
        print original
        # format it for viaf
        original_formatted = original.replace(' ', '%20')
        # create the viaf query
        viaf_api_url = viaf_api_url_part_1 + original_formatted + viaf_api_url_part_2
        # open that url
        viaf_api_url_response = urllib2.urlopen(viaf_api_url)
        # read it
        viaf_api_url_response_reader = viaf_api_url_response.read()
        # parse the string (yes, i know this is xml) to find the number of records
        number_found = viaf_api_url_response_reader.split('<numberOfRecords xsi:type="xsd:nonNegativeInteger">')[1].split('</numberOfRecords')[0]
        # if that is not 0 (yes, i know this is a number), and it's not one of the exceptions, then we have a culprit
        if number_found != '0' and number_found != 'Alphadelphia Association.' and number_found != 'Alphadelphia Association.':
            with open('C:/Users/Public/Documents/culprits-geognames.txt', 'a') as culprits:
                culprits.write(original + '\n')
        # don't overload the viaf server
        time.sleep(.1)
        