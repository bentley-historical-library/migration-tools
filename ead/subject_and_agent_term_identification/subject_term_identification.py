from lxml import etree
import csv

ead_agents = 'C:/Users/Public/Documents/compound_agents.csv'
#ead_subjects = 'C:/Users/Public/Documents/ead_subjects_20150810.csv'
ead_subjects = 'C:/Users/Public/Documents/ead_unique_subjects_20150810.csv'

marc_agents = 'C:/Users/Public/Documents/marc_xml-agents_20150812.csv'
marc_subjects = 'C:/Users/Public/Documents/marc_xml-subjects_20150806.csv'

multiple_term_types = 'C:/Users/Public/Documents/multiple_type_terms_fix.csv'
unidentified_term_types = 'C:/Users/Public/Documents/unidentified_terms_fix.csv'
fixed_term_types = {}

aspace_subjects = 'C:/Users/Public/Documents/aspace_subjects.csv'
compound_agents_fix = 'C:/Users/Public/Documents/compound_agents_terms.csv'

terms_dict = {}
type_dict = {'t':'uniform_title','v':'genre_form','b':'topical','x':'topical','d':'temporal','y':'temporal','z':'geographic','subject':'topical','geogname':'geographic','genreform':'genre_form','655':'genre_form','650':'topical','651':'geographic'}


with open(ead_agents,'rb') as agent_csv:
    reader = csv.reader(agent_csv)
    for row in reader:
        row_indexes = len(row) - 1
        for row_num in range(2, row_indexes+1):
            term = row[row_num]
            if row_num == row_indexes:
                term = term.strip('.')
            if term not in terms_dict:
                terms_dict[term] = []

with open(ead_subjects,'rb') as ead_csv:
    reader = csv.reader(ead_csv)
    for row in reader:
        row_indexes = len(row) - 1
        sub_tag = row[0]
        sub_tag_type = type_dict[sub_tag]
        if row_indexes > 3:
            first_term = row[3]
            if first_term not in terms_dict:
                terms_dict[first_term] = []
            if sub_tag_type not in terms_dict[first_term]:
                terms_dict[first_term].append(sub_tag_type)
            row_nums = []
            for row_num in range(4,row_indexes+1):
                term = row[row_num]
                if row_num == row_indexes:
                    term = term.strip('.')
                if term not in terms_dict:
                    terms_dict[term] = []
        else:
            subject = row[2]
            subject = subject.strip('.')
            if subject not in terms_dict:
                terms_dict[subject] = []
            if sub_tag_type not in terms_dict[subject]:
                terms_dict[subject].append(sub_tag_type)

with open(marc_subjects,'rb') as marc_csv:
    reader = csv.reader(marc_csv)
    for row in reader:
        row_indexes = len(row) - 1
        sub_field = row[1]
        sub_field_type = type_dict[sub_field]
        first_term = row[2]
        if first_term in terms_dict:
            if sub_field_type not in terms_dict[first_term]:
                terms_dict[first_term].append(sub_field_type)
        terms_types = {4:5,6:7,8:9,10:11}
        row_nums = []
        for row_num in terms_types:
            if row_num < row_indexes:
                row_nums.append(row_num)
        for row_num in row_nums:
            term = row[row_num]
            if row_nums.index(row_num) == (len(row_nums) - 1):
                term = term.strip('.')
            term_type_row = terms_types[row_num]
            term_type = row[term_type_row]
            term_type = type_dict[term_type]
            if term in terms_dict:
                if term_type not in terms_dict[term]:
                    terms_dict[term].append(term_type)

with open(marc_agents,'rb') as marc_agent_csv:
    reader = csv.reader(marc_agent_csv)
    for row in reader:
        row_indexes = len(row) - 1
        terms_types = {4:5,6:7,8:9,10:11,12:13,14:15}
        row_nums = []
        for row_num in terms_types:
            if row_num < row_indexes:
                row_nums.append(row_num)
        for row_num in row_nums:
            term = row[row_num]
            if row_nums.index(row_num) == (len(row_nums) - 1):
                term = term.strip('.')
            if term in terms_dict:
                print term
                term_type_row = terms_types[row_num]
                term_type = row[term_type_row]
                term_type = type_dict[term_type]
                if term_type not in terms_dict[term]:
                    terms_dict[term].append(term_type)

with open(multiple_term_types,'rb') as multi_csv:
    reader = csv.reader(multi_csv)
    for row in reader:
        term = row[0]
        term_type = row[2]
        fixed_term_types[term] = term_type

with open(unidentified_term_types,'rb') as unid_csv:
    reader = csv.reader(unid_csv)
    for row in reader:
        term = row[0]
        term_type = row[1]
        fixed_term_types[term] = term_type

unid = 0
multi = 0
total = 0
for term in terms_dict:
    total += 1
    if len(terms_dict[term]) == 0:
        if term not in fixed_term_types:
            unid += 1
            with open('C:/Users/Public/Documents/unidentified_terms.csv','ab') as unid_csv:
                writer = csv.writer(unid_csv)
                writer.writerow([term])
    if len(terms_dict[term]) > 1:
        if term not in fixed_term_types:
            print term, terms_dict[term]
            multi += 1
            with open('C:/Users/Public/Documents/multiple_type_terms.csv','ab') as multi_csv:
                writer = csv.writer(multi_csv)
                writer.writerow([term,terms_dict[term]])
print unid
print multi
print total



#Write a csv with aspaceified subjects
with open(ead_subjects,'rb') as unique_file:
    reader = csv.reader(unique_file)
    for row in reader:
        sub_tag = row[0]
        source = row[1]
        subject = row[2]
        print subject
        first_term_type = type_dict[sub_tag]
        row_indexes = len(row) - 1
        if row_indexes == 3:
            term = row[3]
            with open(aspace_subjects,'ab') as csv_out:
                writer = csv.writer(csv_out, dialect='excel')
                writer.writerow([sub_tag,source,subject,term,first_term_type])
        elif row_indexes > 3:
            first_term = row[3]
            new_row = []
            new_row.append(sub_tag)
            new_row.append(source)
            new_row.append(subject)
            new_row.append(first_term)
            new_row.append(first_term_type)
            for row_num in range(4,row_indexes + 1):
                term = row[row_num]
                new_row.append(term)
                if term.strip('.') in fixed_term_types:
                    term_type = fixed_term_types[term.strip('.')]
                else:
                    if len(terms_dict[term.strip('.')]) == 0:
                        term_type = 'unidentified'
                    elif len(terms_dict[term.strip('.')]) > 1:
                        term_type = 'multiple'
                    else:
                        for item in terms_dict[term.strip('.')]:
                            term_type = item
                new_row.append(term_type)
            with open(aspace_subjects,'ab') as csv_out:
                writer = csv.writer(csv_out,dialect='excel')
                writer.writerow(new_row)

with open(ead_agents, 'rb') as compound_file:
    reader = csv.reader(compound_file)
    for row in reader:
        row_indexes = len(row) - 1
        compound_agent = row[0]
        new_row = []
        new_row.append(compound_agent)
        for row_num in range(2, row_indexes + 1):
            term = row[row_num]
            new_row.append(term)
            if term.strip('.') in fixed_term_types:
                term_type = fixed_term_types[term.strip('.')]
            else:
                if len(terms_dict[term.strip('.')]) == 0:
                    term_type = 'unidentified'
                elif len(terms_dict[term.strip('.')]) > 1:
                    term_type = 'multiple'
                else:
                    for item in terms_dict[term.strip('.')]:
                        term_type = item
            new_row.append(term_type)
        with open(compound_agents_fix,'ab') as csv_out:
            writer = csv.writer(csv_out, dialect='excel')
            writer.writerow(new_row)
