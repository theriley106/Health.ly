import requests
import os
import csv
import json
csvfiles = []
for file in os.listdir("data/"):
	if file.endswith(".csv"):
		csvfiles.append(os.path.join("data/", file))

def csvToList(csvfile):
	with open(file, 'r') as f:
		reader = csv.reader(f)
		your_list = list(reader)
	flat_list = [item for sublist in your_list for item in sublist]
	return flat_list

information = {}

for file in csvfiles:
	nameOfAllergy = file.partition("/")[2].partition(".csv")[0]
	print nameOfAllergy
	information[nameOfAllergy] = csvToList(file)


with open('data.json', 'w') as fp:
    json.dump(information, fp)