import json
import threading
import requests
import bs4

def inputJson(jsonfile):
	with open(jsonfile) as json_data:
		d = json.load(json_data)
		return d

def returnIngredients(dpnum):
	rea = []
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	url = 'https://www.amazon.com/dp/{}'.format(dpnum)
	a = requests.get(url, headers=headers)
	page = bs4.BeautifulSoup(a.text, 'lxml')
	box = page.select('#importantInformation .content')
	if 'Ingredients</h5>' in str(box):
		a = str(box).partition('Ingredients</h5>')[2].partition('<br/>')[0]
		a = a.replace("(", ",").replace(")", ",").replace(".", "")
		a = a.split(',')
		for e in a:
			if len(str(e.strip())) > 2:
				rea.append(str(e.strip()))
	if len(rea) > 2:
		return rea


def scrapeListOfASIN(key):
	listofASIN = allASIN[key]
	info = []
	for i, asin in enumerate(listofASIN, 1):
		res = returnIngredients(asin)
		if res != None:
			for e in res:
				info.append(e)
		if i % 10 == 0 or i == 1:
			with open('{}.json'.format(key), 'w') as fp:
				json.dump({key: info}, fp)
			print("Updated: {} with {} items".format(key, i))

listOfKeys = []
allASIN = inputJson('Database.json')

for key, item in allASIN.iteritems():
	listOfKeys.append(key)


threads = [threading.Thread(target=scrapeListOfASIN, args=(key,)) for key in listOfKeys]
for thread in threads:
	thread.start()
for thread in threads:
	thread.join()


