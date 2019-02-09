# Harvard Library API

### About The Software
This software is used to collect structured data from the Harvard Library API (https://wiki.harvard.edu/confluence/display/LibraryStaffDoc/LibraryCloud+Item+API). The scripts in this directory use Python3, and bash. PLEASE NOTE: If you have both Python2, and Python3 installed on your machine, you may need to modify some of the commands listed below (e.g. pip --> pip3).

### Installaton Instruction
To install the required packages for the software, please navigate to the root directory of the software (i.e. where you find getdata.py) and run the following commands:

        pip install virtualenv
        virtualenv virt
        source virt/bin/activate
        pip install -r requirements.txt

### Run the Data Extraction
The python script takes two arguments: (1) search term, (2) result number. For example, to get the first result for the key term 'cat', run:
        
        python getdata.py 'cat' 0

Or, to get the 5th record for the key term 'dog', run:
        
        python getdata.py 'dog' 4


### What is returned, and how to chage it?
The code will return the fields specified in the 'terms' variable of getHarvardLibraryData.py (see line 175-181) in comma seperated variable format (CSV). In this initial commit of the software, the fields are: 

        terms       = ['titleInfo.title',
		       'name.namePart', 
			'subject.topic',
			'language.languageTerm',
			'physicalDescription.extent', 
			'abstract'
		       ]

The terms are based on the raw content that is returned from the harvard library API. For instance https://api.lib.harvard.edu/v2/items.json?q=fish&start=1&limit=1 returns a JSON formatted record from the API when searching for the term 'fish'. When processed by our program, that JSON data is converted into something like this:

	"Advances in Marine and Brackishwater Aquaculture","[*] Perumal, Santhanam. [*] Pachiappan, Perumal. [*] A.R., Thirunavukkarasu.","[*] Fish [*] Life sciences [*] Freshwater & Marine Ecology [*] Fish & Wildlife Biology & Management [*] Marine sciences [*] Aquatic ecology [*] Life Sciences [*] Freshwater [*] Marine & Freshwater Sciences [*] Oceanography [*] Wildlife","[*] eng [*] English","1 online resource (266 p.)","This book compiles the latest findings in the field of marine and brackishwater aquaculture. It covers significant topics such as techniques of culture of live feeds (microalgae, rotifer, Artemia, marine copepod & polychaetes), while also highlighting vital themes like the culture and applications of free and marine sponge associated microbial probiotics, controlled breeding, seed production and culture of commercially important fin and shell fishes. Moreover, the book focuses on the breeding and culture of marine ornamental fishes, sea cucumber and sea urchin, and discusses seaweeds culture, aqua feed formulation and nutrition, water quality management in hatchery and grow-out culture systems, fish disease diagnosis and health management and cryopreservation of fish gametes for sustainable aquaculture practices, all from a multidimensional perspective. The global fish production was 154 million tonnes in 2011 which more or less consisted of capture and culture fisheries (FAO, 2012). Roughly 80% of this is from inland-freshwater aquaculture and the remainder from capture fisheries in the marine and brackishwater sector. However, marine and brackishwater catches have recently begun to diminish due to overexploitation, climate change and pollution. The UNEP report affirmed that if the world remains on its current course of overfishing, by 2050, the ocean fish stock could become extinct or no longer commercially viable to exploit. In these circumstances, aquaculture is considered to be a promising sector to fulfill our future protein requirement. However, brackishwater and marine fish production now face serious challenges due to e.g. lack of quality fish seeds, feeds, poor water quality management and diseases. <It is well known that a regular supply of adequate quantities of quality seeds, feeds and proper water quality management are prerequisites for the sustainable growth of the aquaculture industry. Quality seeds are those that ensure high growth rates, low mortality and can withstand during stress conditions. Further, it is generally agreed that the utilization of nutritionally superior live feeds in fish larval production is indispensable. In this context, this book sheds light on techniques for sustainable aquaculture practices concerning various marine and brackishwater organisms. Fisheries and aquaculture sectors play a vital role as potential sources of nutritional security and food safety around the globe. Fish food is rich in protein, vitamins, phosphorous, calcium, zinc, selenium etc. In addition, fish contains omega-3 fatty acids, which help to prevent cardiovascular diseases. Fish food can also provide several health benefits to consumers. The omega 3 fatty acids found in fish can reduce the levels of LDL cholesterol (the “bad” cholesterol) and increase the HDL levels (the “good” cholesterol). Research conducted in Australia has proved that fish consumption can be used to cure hypertension and obesity. It is also reported that people who ate more fish were less prone to asthma and were able to breathe more easily. Omega 3 fish oil or fish consumption can help to prevent three of the most common forms of cancer: breast cancer, colon and prostate cancer. The omega 3 fatty acids present in fish or fish oil induce faster hair growth and prevent hair loss. Since most varieties of fish are rich in protein, eating fish helps to keep hair healthy. Furthermore, fish or fish oil helps in improving the condition of dry skin, giving it a healthy glow. It is useful in treating various skin problems such as eczema, psoriasis, itching, redness of skin, skin lesions and rashes. It is well known that eating fish improves vision and prevents Alzheimer’s and type-2 diabetes, and can combat arthritis. Further, fish oil or fish is good for pregnant women, as the DHA present in it helps in the development of the baby’s eyes and brain. It helps to avoid premature births, low birth weights and miscarriages. In addition, it is widely known that fish can be a good substitute for pulses in cereal-based diets for the poor. The global fish production was roughly 154 million tonnes in 2011 (FAO, 2012). It is estimated that by 2020 global fish requirements will be over 200 million tonnes; as such, innovative technological improvements are called for in order to improve the production and productivity in fisheries. In this context, this book provides valuable information for academics, scientists, researchers, government officials and farmers on innovative technological advances for sustainable fish production using aquaculture methods. The book identifies the main issues and trends in marine and brackishwater aquaculture from a global perspective in general and in the Indian context in particular. It includes 23 chapters written by prominent researchers from various institutes and universities across India, who address the latest aquaculture technologies with distinctive approaches to support academics, researchers and graduates in the fields of Fisheries, Aquaculture, Marine Science, Marine Biology, Marine Biotechnology, Zoology and Agricultural Sciences. Our thanks go to our contributors; we are confident that all readers will immensely benefit from their valued expertise in the field of marine and brackishwater aquaculture."

Inspecting the raw JSON, you will notice that under "items"-->"mods" there is a subfield called "titleInfo" which itself contains a subfeild called "title". The way to access this title, would be to add titleInfo.title to the list of 'terms' in the python script.

When the API returns more than one result for a given field request (e.g. name.namePart), those values will be contatenated and separted with a "[\*]". In the case of the earlier example, the code would return:

        [*] Perumal, Santhanam. [*] Pachiappan, Perumal. [*] A.R., Thirunavukkarasu.","[*] Fish [*] Life sciences [*]Freshwater & Marine Ecology [*] Fish & Wildlife Biology & Management [*] Marine sciences [*] Aquatic ecology [*] Life Sciences [*] Freshwater [*] Marine & Freshwater Sciences [*] Oceanography [*] Wildlife","[*] eng [*] English"

### Questions?
Please email me if you have questions about this code, or notice any mistakes.


