import csv

# you'll need to install fuzzywuzzy -- from a command line: 'pip install fuzzywuzzy'
from fuzzywuzzy import fuzz

# where are the input files?
persname_csv_filepath = 'path/to/persname/csv/output.csv'
corpname_csv_filepath = 'path/to/corpname/csv/output.csv'

# what should we name the output file?
constants = 'constants.py'

# sets up the authority dictionary. Contains a dictionary for each authority type you'll be parsing
auth_dict = {'persnames': {}, 'corpnames': {}}


# Function to populate the dictionaries
# Takes a path to the input csv and an authority-type string ('persname', 'corpname', etc.).
# The authority type should match one of the auth_dict keys
def populate_dictionary(path_to_refined_csv, auth_type):
    with open(path_to_refined_csv, 'rb') as f:
        reader = csv.reader(f)
        next(reader)  # skip the first row (this is assuming it starts with a header)

        # update the dictionary
        for row in reader:
            original_name, lc_name, lc_link = row

            if lc_link is not None and lc_link.startswith('http://id.loc.gov/authorities/names/'):
                fuzz_ratio = fuzz.ratio(original_name, lc_name)
                if fuzz_ratio >= 80:
                    auth_dict[auth_type][original_name] = lc_link


# call the function with our csv files as inputs
populate_dictionary(persname_csv_filepath, auth_type='persnames')
populate_dictionary(corpname_csv_filepath, auth_type='corpnames')


# write the new dictionaries to constants.py
with open(constants, "w") as txt_file:
    txt_file.write('# dictionary for persnames\npersnames_dictionary = ' + str(auth_dict['persnames']))
    txt_file.write('\n\n# dictionary for corpnames\ncorpnames_dictionary = ' + str(auth_dict['corpnames']))
    
print 'Written to constants.'
