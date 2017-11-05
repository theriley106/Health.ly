import json
import threading
import requests
import bs4
import random

r = requests.post("http://138.197.123.15:8888/proxies/{}".format(open('../../SecretCode.txt').read().strip())).json()
Proxies = r["proxies"]
print Proxies
lock = threading.Lock()
def inputJson(jsonfile):
	with open(jsonfile) as json_data:
		d = json.load(json_data)
		return d

def returnIngredients(dpnum):
	rea = []
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	url = 'https://www.amazon.com/dp/{}'.format(dpnum)
	try:
		prx = random.choice(Proxies)
		proxies = {'http': prx, 'https': prx}
		a = requests.get(url, headers=headers, proxies=proxies)
		page = bs4.BeautifulSoup(a.text, 'lxml')
	except:
		try:
			prx = random.choice(Proxies)
			proxies = {'http': prx, 'https': prx}
			a = requests.get(url, headers=headers, proxies=proxies)
			page = bs4.BeautifulSoup(a.text, 'lxml')
		except:
			return None
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

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in xrange(0, len(l), n))



def scrapeListOfASIN(key):
	listofASI = allASIN[key]
	listofASIN = chunks(listofASI, 15)
	info = []
	def doASINstuff(key, asin):
		res = returnIngredients(asin)
		if res != None:
			for e in res:
				info.append(e)
		lock.acquire()
		with open('{}.json'.format(key), 'w') as fp:
			json.dump({key: info}, fp)
		lock.release()
	for i, asin in enumerate(listofASIN, 1):
		try:
			threads = [threading.Thread(target=doASINstuff, args=(key, a)) for a in asin]
			for thread in threads:
				thread.start()
			for thread in threads:
				thread.join()
			print("Updated: {} with {} items".format(key, i*10))
		except Exception as exp:
			pass

listOfKeys = []
allASIN = inputJson('Database.json')

for key, item in allASIN.iteritems():
	listOfKeys.append(key)


threads = [threading.Thread(target=scrapeListOfASIN, args=(key,)) for key in listOfKeys]
for thread in threads:
	thread.start()
for thread in threads:
	thread.join()


