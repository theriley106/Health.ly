import glob
import json
import os
information = {}

def inputJson(jsonfile):
	with open(jsonfile) as json_data:
		d = json.load(json_data)
		return d

listOfAllergens = ['halal', 'vegan', 'vegetarian', 'gmoFree', 'kosher', 'lowCarb']

for allergens in listOfAllergens:
	information[allergens] = inputJson('{}.json'.format(allergens))[allergens]

with open('Database.json', 'w') as fp:
	json.dump(information, fp)