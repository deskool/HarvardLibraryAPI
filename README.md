# About The Software
###This software is used to collect structured data from the Harvard Library API (https://wiki.harvard.edu/confluence/display/LibraryStaffDoc/LibraryCloud+Item+API). The scripts in this directory use Python3, and bash. PLEASE NOTE: If you have both Python2, and Python3 installed on your machine, you may need to modify some of the commands listed below (e.g. pip --> pip3).

# Installaton Instruction
###To install the required packages for the software, please navigate to the root directory of the software (i.e. where you find getdata.py) and run the following commands:

        pip install virtualenv
        virtualenv virt
        source virt/bin/activate
        pip install -r requirements.txt

# Run the Data Extraction
### The python script takes two arguments: (1) search term, (2) result number 
### For example, to get the first result for the key term 'cat', run:
        python getdata.py 'cat' 0

### Or, to get the 5th record for the key term 'dog', run:
        python getdata.py 'dog' 4


# What is returned, and how to change what is returned?
### The code will return the fields specified in the 'terms' variable of getHarvardLibraryData.py (see line 175). The terms are based on the raw return from the harvard library API. For instance https://api.lib.harvard.edu/v2/items.json?q=fish&start=1&limit=1 returns a JSON formatted record from the API. Notice that under "items"-->"mods" there is a subfield called "titleInfo" which itself contains a subfeild called "title". The way to access this title, would be to add titleInfo.title to the list of 'terms' in the python script.


