# AUTHOR      : MOHAMMAD M. GHASSEMI <ghassemi@mit.edu>
# DATE        : FEB 9, 2019
# DESCRIPTION : Collects data from the Harvard Library API. See README.md for more detail. 

# IMPORT THE REQUIRED LIBRARIES

from six.moves import urllib
import xml.etree.ElementTree as ET
import xmltodict
import json
import csv
import collections
import time
import requests
# from importlib import reload
import numpy as np
import ast
import sys
import os.path

TIMEOUT = 3

#########################################################################################################################################
# DOCUMENTATION
#########################################################################################################################################
#1. https://wiki.harvard.edu/confluence/display/LibraryStaffDoc/LibraryCloud+Item+API

#########################################################################################################################################
# SUPPORTING FUNCTIONS
#########################################################################################################################################

# GETS JSON DATA FROM A URL CALL  -----------------------------------------------------------------------------------------------------
def get_json_from_url(url, is_type='json'):
	reload(requests)
	
	# MAKE A REQUEST
	try:
	   r   = requests.get(url, stream=False, timeout=TIMEOUT)
	except(requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
	   return None
	
	raw = r.content
	
	# EXTRACT THE JSON
	if is_type == 'xml':
	   return json.loads(json.dumps(xmltodict.parse(raw, 
		                                             process_namespaces = True, 
							     namespaces = {'http://www.loc.gov/mods/v3':None,
							                   'http://api.lib.harvard.edu/v2/item':None}, 
							     attr_prefix = '', 
							     cdata_key = '')))
	elif is_type == 'json':
		raw = raw.replace(b': null',b': "null"')
		raw = raw.replace(b':null',b':"null"')
		
		raw = raw.replace(b', null',b', "null"')
		raw = raw.replace(b',null',b',"null"')
		
		raw = raw.replace(b'[ null',b'[ "null"')
		raw = raw.replace(b'[null',b'["null"')
		
		raw = raw.replace(b'{ null',b'{ "null"')
		raw = raw.replace(b'{null',b'{"null"')

		return eval(raw)

# CONVERTS A DICT FULL OF UNICODE INTO STRING  ---------------------------------------------------------------------------------------
def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

#EXPANDS OUT A MESSY DICTIONARY  ---------------------------------------------------------------------------------------------------
def json2csv(my_dict, last_keys='',key_list=[], value_list=[]):
	# IF THIS IS A DICTIONARY IN THE DICTIONARY
	if isinstance(my_dict, dict):
		for key, value in my_dict.items():
			this_key = last_keys + '.' + key
			if isinstance(value, dict):
				json2csv(my_dict[key],this_key,key_list,value_list)
			elif isinstance(value,list):
				json2csv(my_dict[key],this_key,key_list,value_list)
			elif value == None:
				key_list.append(this_key[1:])
				value_list.append('None')
			else:
				key_list.append(this_key[1:])
				value_list.append(value)
	# IF THIS IS A LIST IN THE DICT 
	if isinstance(my_dict, list):
		for i in range(len(my_dict)):
			this_key = last_keys + '_' + str(i) + '_'
			if isinstance(my_dict[i], dict):
				json2csv(my_dict[i],this_key,key_list,value_list)
			elif isinstance(my_dict[i],list):
				json2csv(my_dict[i],this_key,key_list,value_list)
			elif my_dict[i] == None:
				key_list.append(this_key[1:])
				value_list.append('None')
			else:
				key_list.append(this_key[1:])
				value_list.append(my_dict[i])
	return dict(zip(key_list, value_list))

#TODO - add #text, add @authority.
def assign_key_numbers_to_value(data):
	r_key,r_value = [], []
	for key, value in data.items():
		new_key, new_value = key, value		

		if '_' in key:
			where = [pos for pos, char in enumerate(key) if char == '_']
			starts,ends = where[0:len(where):2],where[1:len(where):2]
			en_data = ''
			for i in range(len(starts)):
				ii      = (len(starts)-1) - i
				en_data += key[starts[ii]+1:ends[ii]] + '.' 
				new_key = new_key[:starts[ii]] + new_key[ends[ii]+1:] 
			en_data    = '[*] '
			new_value  = en_data + str(new_value)

		if '.@type' in key:
			new_key = new_key.replace('.@type','.type')

		if '.#text' in key:
			new_key = new_key.replace('.#text','')

		if '.@authority' in key:
			new_key = new_key.replace('.@authority','.authority')

		if '.@source' in key:
			new_key = new_key.replace('.@source','.source')

		if '.@otherType' in key:
			new_key = new_key.replace('.@otherType','.otherType')

		if '.@edition' in key:
			new_key = new_key.replace('.@edition','.edition')

		if '.@encoding' in key:
			new_key = new_key.replace('.@encoding','.encoding')

		r_key   = r_key   + [new_key]
		r_value = r_value + [new_value]

	return r_key, r_value

def remove_redundent_keyvals(key,value):
	a = []
	for i in range(len(key)):
		a.append(key[i] + '|||' + value[i])
	a = list(set(a))
	key  = [x.split('|||')[0] for x in a]
	value = [x.split('|||')[1] for x in a]
	return key, value

def merge_clashing_key_vals_into_dict(key,value):
	new_data = {}
	for i in range(len(key)):
		if value[i] not in ['[*] text','[*] date']: 
			if key[i] in new_data: 
				new_data[key[i]] += ' ' + value[i]
			else:
				new_data[key[i]] = value[i]
	return new_data

#########################################################################################################################################
# MAIN
#########################################################################################################################################
terms       = ['titleInfo.title']
search_term = sys.argv[1]

# if user supplies optional argument, provide common terms file
if len(sys.argv) >= 3:
    terms = []
    common_terms_file_name = sys.argv[2]
    common_terms = open(common_terms_file_name, 'r')
    
    for common_term in common_terms:
        terms.append(common_term)
        
output_file = search_term + '.csv'
start       = 0
limit 	    = 250   
    
# GET THE DATA FROM THE API  ------------------------------------------------------------------------------------------------------------

i = 0
count_keys = []
num_records = 0

while (1):  

    content = ''
    
    # The actual API request, returned as JSON
    url         = 'http://api.lib.harvard.edu/v2/items.json?q='+ search_term + '&start=' + str(start) + '&limit=' + str(limit)
    
    raw_json    = get_json_from_url(url,'json')
    
    if raw_json == None or raw_json['items'] == 'null':
        print('Search complete')
        break
    
    # counts the number of returned records    
    mods = raw_json['items']['mods']
    max = len(mods)
    
    #Process/clean up the data
    data = {}
    for i in range (max): 
        datai = json2csv(raw_json['items']['mods'][i])
        data[i] = datai
    
    for i in range (max):  
        key,value   = assign_key_numbers_to_value(data[i])
        
        num_records += 1
        
        # add the terms of each record to count_keys
        for term in key:
            count_keys.append(term)
             
        key,value   = remove_redundent_keyvals(key,value)
        data[i]     = merge_clashing_key_vals_into_dict(key,value)

    # Write the header to the CSV file
    if start == 0:
        
        # replace CSV file upon new search
        try:
            os.remove(output_file)
        except:
            print('file did not previously exist')
        
        header = ''
        for i in range(len(terms)):
            header += '"' + terms[i] + '",'
        content += header[:-1] + '\n'

    # Writing the data to the CSV file
    for i in range(max):
        row = ''
        for j in range(len(terms)):
            term = terms[j][0:-1] #take off newline
            if (term in data[i]):
                row += '"' + data[i][term] + '",'
            else:
                row += '"",'
                
        content += row[:-1] + '\n'

    #write to output_file (named by search term)
    save_file = open(output_file, 'a') 
    save_file.write(content)
    save_file.close()

    start = start + limit
    i = i + 1 
    
    # write all keys to an output file (separate file for getting common keys)
    count_keys_file = open(search_term + '_keys.csv', 'w') 
    
    for term in count_keys:
        count_keys_file.write(str(term))
        count_keys_file.write("\n")
    
    count_keys_file.close()
    
    print('Number of Records: ' , num_records)