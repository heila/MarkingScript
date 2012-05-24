#!/bin/bash

#rename the files
#rename -n 's/(\d\d\d\d\d\d\d\d)(tut2).py/$2_$1.py/' *.py

#run the tests

echo -e "<html><head><meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\"><title>Tutorial 3 Results</title></head><body><h1>Tests:</h1>"
for FILE in `ls tut3_*.py`; do
	echo -e "<h2> File: $FILE</h2>"
	MODULE=${FILE:0:13}
	python MarkingScript.py $MODULE
done

echo -e "</body></html>"
