# import what we need
import csv
from fuzzywuzzy import fuzz

csv.field_size_limit(1000000000)

# what's coming form openrefine?
openrefine_persname_1 = 'openrefine_persname_1.csv'
openrefine_persname_2 = 'openrefine_persname_2.csv'
openrefine_corpname = 'openrefine_corpname.csv'

# empty dictionaries
persnames_dictionary = {}
corpnames_dictionary = {}

# print 'Creating persname dictionary.'

# persnames
def persnames(openrefine_persname):
    with open(openrefine_persname, 'rb') as persnames:
        openrefine_persname_reader = csv.reader(persnames)
        # skip the first row
        next(openrefine_persname_reader, None)
        # make dictionary
        for row in openrefine_persname_reader:
            print '\rWorking on it... |',
            print '\rWorking on it... /',
            print '\rWorking on it... -',
            print '\rWorking on it... \\',
            print '\rWorking on it... |',
            print '\rWorking on it... /',
            print '\rWorking on it... -',
            print '\rWorking on it... -',
            print '\rWorking on it... \\',
            original = row[0]
            authority = row[1]
            link = row[2]
            if link is not None and link.startswith('http://id.loc.gov/authorities/names/'):
                fuzz_ratio = fuzz.ratio(original, authority)
                if fuzz_ratio >= 80:
                    persnames_dictionary[original] = link
                    
persnames(openrefine_persname_1)               
persnames(openrefine_persname_2)               
            
print '\rPersname dictionary created.'

print 'Creating corpname dictionary.'

# corpnames
with open(openrefine_corpname, 'rb') as corpnames:
    openrefine_corpname_reader = csv.reader(corpnames)
    # skip the first row
    next(openrefine_corpname_reader, None)
    # make dictionary
    for row in openrefine_corpname_reader:
        print '\rWorking on it... |',
        print '\rWorking on it... /',
        print '\rWorking on it... -',
        print '\rWorking on it... \\',
        print '\rWorking on it... |',
        print '\rWorking on it... /',
        print '\rWorking on it... -',
        print '\rWorking on it... -',
        print '\rWorking on it... \\',
        original = row[0]
        authority = row[1]
        link = row[2]
        if link is not None and link.startswith('http://id.loc.gov/authorities/names/'):
            fuzz_ratio = fuzz.ratio(original, authority)
            if fuzz_ratio >= 80:
                corpnames_dictionary[original] = link

print '\rCorpname dictionary created.'

print 'Writing to constants.'
            
# where is constants.py?
constants = 'constants.py'

# put the dictionaries in constants.py
with open(constants, "a") as txt_file:
    txt_file.write('# dictionary for persnames\npersnames_dictionary = ' + str(persnames_dictionary))
    txt_file.write('\n\n# dictionary for corpnames\ncorpnames_dictionary = ' + str(corpnames_dictionary))
    
print 'Written to constants.'