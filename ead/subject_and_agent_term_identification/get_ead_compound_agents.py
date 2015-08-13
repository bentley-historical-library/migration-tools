from lxml import etree
import csv
import os
from os.path import join

tags = ['persname','corpname','famname']

output = 'C:/Users/Public/Documents/compound_agents.csv'

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

uniques = []

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    for sub in tree.xpath('//controlaccess/*'):
        if sub.tag in tags and sub.text is not None:
            if '--' in sub.text:
                if sub.text not in uniques:
                    uniques.append(sub.text)
    print filename

for unique in uniques:
    print unique
    row = []
    row.append(unique)
    terms = unique.split('--')
    for term in terms:
        row.append(term)
    with open(output, 'ab') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)
