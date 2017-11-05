import requests
import os
import csv
import bs4
import threading
csvfiles = []
for file in os.listdir("data/"):
	if file.endswith(".csv"):
		csvfiles.append(os.path.join("data/", file))
information = {}
FinishedDPI = []
for files in csvfiles:
	if 'backup' not in str(files):
		a = []
		with open('data/' + file, 'r') as f:
			reader = csv.reader(f)
			your_list = list(reader)
		print(your_list)
		for e in your_list:
			if len(e[0]) > 2:
				a.append(e[0])
		information[files.partition("/")[2].partition('.csv')[0]] = a

lock = threading.Lock()
print csvfiles
def returnIngredients(dpnum):
	rea = []
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	url = 'https://www.amazon.com/dp/{}'.format(dpnum)
	a = requests.get(url, headers=headers)
	page = bs4.BeautifulSoup(a.text, 'lxml')
	print page.title.string
	box = page.select('#importantInformation .content')
	if 'Ingredients</h5>' in str(box):
		a = str(box).partition('Ingredients</h5>')[2].partition('<br/>')[0]
		a = a.replace("(", ",").replace(")", ",").replace(".", "")
		a = a.split(',')
		for e in a:
			if len(str(e.strip())) > 2:
				rea.append([str(e.strip())])
	if len(rea) > 2:
		return rea



def findAll(csvfile):
	e = []
	for i, dpi in enumerate(information[csvfile.partition("/")[2].partition('.csv')[0]]):
		print len(information[csvfile.partition("/")[2].partition('.csv')[0]])
		print i
		lock.acquire()
		if dpi not in FinishedDPI:
			FinishedDPI.append(dpi)
			lock.release()
			if len(dpi) > 3:
				try:
					ing = returnIngredients(dpi)
					if ing != None:
						for eee in ing:
							e.append(eee)
					else:
						print("ing is none")
				except Exception as exp:
					print exp
				if ing != None:
					lock.acquire()
					with open("{}backup.csv".format(csvfile.partition(".")[0]), "wb") as ff:
						writer = csv.writer(ff)
						writer.writerows(e)
					lock.release()
		else:
			print("_")
			lock.release()



threads = [threading.Thread(target=findAll, args=(csvfi,)) for csvfi in csvfiles]
for thread in threads:
	thread.start()
for thread in threads:
	thread.join()

#print csvfiles
#print returnIngredients("B00QT7V5RA")