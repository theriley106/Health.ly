from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response

import requests
import bs4
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

app = Flask(__name__)

@app.route('/info/<upc>', methods=['POST'])
def mainStock(upc):
	a = searchByUPC(upc)
	a = retIng(a)
	return str(a)
	

def searchByUPC(upc):
	url = "http://search.mobile.walmart.com/v1/products-by-code/UPC/{}".format(upc)
	return str(requests.get(url).text.encode("utf8")).partition('"wwwItemId":"')[2].partition('"')[0]

def returnIngredients(wwwitemid):
	url = 'https://www.walmart.com/ip/{}'.format(wwwitemid)
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	res = requests.get(url, headers=headers)
	with open("A.html", "w") as f:
		f.write(res.content)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	print page.title.string
	print page.select('.subTitle')
	if 'Niacinamide' in str(page):
		print("True")
	return a

def retIng(wwwitemid):
	a = requests.get('https://www.walmart.com/ip/{}#read-more'.format(wwwitemid)).text
	a = a.partition('"ingredients":"')[2].partition('"')[0]
	ingredients = []
	for e in a.split(','):
		ingredient = e.partition(' (')[0].strip()
		ingredient = ingredient.replace('.', ' ').replace(':', ' ')
		if len(ingredient) > 2:
			ingredients.append(ingredient.strip())
	return ingredients



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)