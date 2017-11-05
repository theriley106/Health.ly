# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
import requests
import bs4
import re
import csv
import json
#def grabAllSKU(url):
information = {}

listOfAllergens = ['halal', 'vegan', 'vegetarian', 'gmoFree', 'kosher', 'lowCarb', ]
for a in listOfAllergens:
	with open('WM{}.csv'.format(a), 'r') as f:
		reader = csv.reader(f)
		your_list = list(reader)
	main_list = []
	for e in your_list:
		main_list.append(e[0])
	information[a] = main_list


with open('WMDatabase.json', 'w') as fp:
	json.dump(information, fp)

print information['halal']

'''if __name__ == '__main__':
	for allergy in listOfAllergens:
		a = []
		for i in range(1, 15):
			try:
				res = requests.get("https://www.walmart.com/search/?page={}&query={}".format(i, allergy))
				page = bs4.BeautifulSoup(res.text, 'lxml')
				for items in list(set(re.findall('\"usItemId\":\"(\d+)\"', str(page)))):
					a.append([items])
				print page.title.string
			except:
				pass
		with open("WM{}.csv".format(allergy), "wb") as ff:
			writer = csv.writer(ff)
			writer.writerows(a)'''