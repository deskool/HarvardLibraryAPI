#!/bin/bash
# Basic while loop
searchTerm=$1
start=0

# execute numRecords.py to get max and common terms
python3 ./numRecords.py $searchTerm $start

# get max from maxNumRecords.txt
input="./$searchTerm""_maxNumRecords.txt"
 
declare -i max

if [[ -f "$input" ]]
	then
		while read line 
		do
			echo "$line"
			max="$line"
		done <"$input"
fi

# scrape Harvard Library API for data
commonTermsFile="./common_$searchTerm""_keys.csv"

mkdir $searchTerm
while [ $start -le $max ]
do
python3 ./getHarvardLibraryData.py $searchTerm $start $commonTermsFile
((start+=250))
done

#TAKES UP A LOT OF SPACE
#cd $searchTerm
#cat *.csv >merged.csv
echo All done
