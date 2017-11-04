import requests
import bs4
import re
import csv
import threading
import time

categories = [['lowCarb', 'https://www.amazon.com/s/ref=sr_pg_2?fst=as%3Aoff&rh=n%3A16310101%2Cp_n_feature_nine_browse-bin%3A114327011'],['glutenFree', 'https://www.amazon.com/s/ref=sr_pg_2?fst=as%3Aoff&rh=n%3A16310101%2Cp_n_feature_nine_browse-bin%3A114329011'],
['vegan', 'https://www.amazon.com/s/ref=sr_pg_2?fst=as%3Aoff&rh=n%3A16310101%2Cp_n_feature_nine_browse-bin%3A114322011'],
['vegetarian', 'https://www.amazon.com/s/ref=sr_pg_2?fst=as%3Aoff&rh=n%3A16310101%2Cp_n_feature_nine_browse-bin%3A114321011&page=2'],
['kosher', 'https://www.amazon.com/s/ref=sr_pg_2?fst=as%3Aoff&rh=n%3A16310101%2Cp_n_feature_nine_browse-bin%3A114328011'],
['gmoFree', 'https://www.amazon.com/s/ref=sr_pg_2?fst=as%3Aoff&rh=n%3A16310101%2Cp_n_feature_nine_browse-bin%3A5712560011'],['halal', 'https://www.amazon.com/s/ref=sr_pg_2?fst=as%3Aoff&rh=n%3A16310101%2Cp_n_feature_nine_browse-bin%3A2251590011&page=2'],
['highFructoseFree', 'https://www.amazon.com/s/ref=sr_pg_2?fst=as%3Aoff&rh=n%3A16310101%2Cp_n_feature_nine_browse-bin%3A5712562011']]


def grabCategory(urlz):
	print urlz
	f = []
	cat = urlz[0]
	for i in range(1, 30):
		try:
			url = str(urlz[1]).replace('sr_pg_2', 'sr_pg_{}'.format(i))
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
			res = requests.get(url, headers=headers)
			page = bs4.BeautifulSoup(res.text, "lxml")
			a = page.select('.s-item-container')
			for e in a:
				try:
					num = str(e).partition('/dp/')[2].partition('/')[0]
					print num
					f.append([num])
				except:
					print("Error")
			print i
		except Exception as exp:
			print exp
			print("Fatal error")
		with open("{}.csv".format(cat), "wb") as ff:
		    writer = csv.writer(ff)
		    writer.writerows(f)


threads = [threading.Thread(target=grabCategory, args=(command,)) for command in categories]
for thread in threads:
	thread.start()
for thread in threads:
	thread.join()