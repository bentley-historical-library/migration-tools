import csv
from fuzzywuzzy import fuzz
from tqdm import *

csv.field_size_limit(1000000000)

openrefine_persname_1 = 'openrefine_persname_1.csv'
openrefine_persname_2 = 'openrefine_persname_2.csv'
openrefine_corpname = 'openrefine_corpname.csv'

def percentage(portion, total):
    percent = float(portion) / float(total) * 100
    return percent

# persnames
print '\nComparing fuzzywuzzy ratios for <persname> attributes...'

persnames_total = 0
persname_100 = 0
persname_95 = 0
persname_a = 0
persname_b = 0

with open(openrefine_persname_1, 'rb') as persnames:
    openrefine_persname_reader = csv.reader(persnames)
    next(openrefine_persname_reader, None)
    for row in openrefine_persname_reader:
        persnames_total += 1
        original = row[0]
        authority = row[1]
        link = row[2]
        if link is not None and link.startswith('http://id.loc.gov/authorities/names/'):
            fuzz_ratio = fuzz.ratio(original, authority)
            if fuzz_ratio == 100:
                persname_100 += 1
            if fuzz_ratio >= 95:
                persname_95 += 1
            if fuzz_ratio >= 90:
                persname_a += 1
            if fuzz_ratio >= 80:
                persname_b += 1
                
with open(openrefine_persname_2, 'rb') as persnames:
    openrefine_persname_reader = csv.reader(persnames)
    next(openrefine_persname_reader, None)
    for row in openrefine_persname_reader:
        persnames_total += 1
        original = row[0]
        authority = row[1]
        link = row[2]
        if link is not None and link.startswith('http://id.loc.gov/authorities/names/'):
            fuzz_ratio = fuzz.ratio(original, authority)
            if fuzz_ratio == 100:
                persname_100 += 1
            if fuzz_ratio >= 95:
                persname_95 += 1
            if fuzz_ratio >= 90:
                persname_a += 1
            if fuzz_ratio >= 80:
                persname_b += 1
            
print '\nTotal <persname> attributes: ' + str(persnames_total)
print 'Ratio score of 100: ' + str(persname_100) + ' (' + str(percentage(persname_100, persnames_total)) + '%)'
print 'Ratio score of 95: ' + str(persname_95) + ' (' + str(percentage(persname_95, persnames_total)) + '%)'
print 'Ratio score of "A": ' + str(persname_a) + ' (' + str(percentage(persname_a, persnames_total)) + '%)'
print 'Ratio score of "B": ' + str(persname_b) + ' (' + str(percentage(persname_b, persnames_total)) + '%)'

# corpnames
print '\nComparing fuzzywuzzy ratios for <corpname> attributes...'

corpnames_total = 0
corpname_100 = 0
corpname_95 = 0
corpname_a = 0
corpname_b = 0

with open(openrefine_corpname, 'rb') as corpnames:
    openrefine_corpname_reader = csv.reader(corpnames)
    next(openrefine_corpname_reader, None)
    for row in openrefine_corpname_reader:
        corpnames_total += 1
        original = row[0]
        authority = row[1]
        link = row[2]
        if link is not None and link.startswith('http://id.loc.gov/authorities/names/'):
            fuzz_ratio = fuzz.ratio(original, authority)
            if fuzz_ratio == 100:
                corpname_100 += 1
            if fuzz_ratio >= 95:
                corpname_95 += 1
            if fuzz_ratio >= 90:
                corpname_a += 1
            if fuzz_ratio >= 80:
                corpname_b += 1
                
print '\nTotal <corpname> attributes: ' + str(corpnames_total)
print 'Ratio score of 100: ' + str(corpname_100) + ' (' + str(percentage(corpname_100, corpnames_total)) + '%)'
print 'Ratio score of 95: ' + str(corpname_95) + ' (' + str(percentage(corpname_95, corpnames_total)) + '%)'
print 'Ratio score of "A": ' + str(corpname_a) + ' (' + str(percentage(corpname_a, corpnames_total)) + '%)'
print 'Ratio score of "B": ' + str(corpname_b) + ' (' + str(percentage(corpname_b, corpnames_total)) + '%)'