import csv
import sys

search_term = sys.argv[1]
num_records = sys.argv[2]
input_file = search_term + '_keys.csv'

csvfile = open(input_file, 'r')

terms_dict = {}

# count the number of times a search term shows up
for term in csvfile:
    if term in terms_dict:
        terms_dict[term] += 1
    else: 
        terms_dict[term] = 1

print(num_records)
print(terms_dict)
common_terms = []
uncommon_terms = []

# if term shows up less than 80% of time add to uncommon terms file
for term in terms_dict:
    if ((float(terms_dict[term]) / float(num_records)) < .8):
        # add to the uncommon terms file
        uncommon_terms.append(term) 
        
    else:
        # add to the common terms file
        common_terms.append(term)

# get the unique set of terms                
common_terms = list(set(common_terms))
uncommon_terms = list(set(uncommon_terms))

# write terms to files 
uncommon_terms_file = open('uncommon_' + search_term + '_keys.csv', 'w') 
uncommon_terms_file.write(''.join(uncommon_terms))
uncommon_terms_file.close()        
        
common_terms_file = open('common_' + search_term + '_keys.csv', 'w') 
common_terms_file.write(''.join(common_terms))
common_terms_file.close()      

csvfile.close()