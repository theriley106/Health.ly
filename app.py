from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response
import requests
import bs4
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import json

app = Flask(__name__)

def inputJson(jsonfile):
	with open(jsonfile) as json_data:
		d = json.load(json_data, strict=False)
		return d

DATABASE = inputJson('data/Database.json')

@app.route('/')
def li():
    return '''<a href="zxing://scan/?ret=http%3A%2F%2F{}%2Fvegan%2F%7BCODE%7D%2Fdescription&SCAN_FORMATS=UPC_A,EAN_13">
    <span>Test Now!</span>
	</a>
	'''.format(url_for('mainStock', allergy='', upc=''))

@app.route('/info/<allergy>/<upc>', methods=['POST', 'GET'])
def mainStock(allergy=None, upc=None):
	a = searchByUPC(upc)
	ingredients = retIng(a)
	a = 0
	if ingredients != None and len(ingredients) > 0:
		for items in ingredients:
			for saveditem in DATABASE[allergy]:
				if levenshtein(items, saveditem) < 3:
					a += 1
		percent = float(a) / float(len(ingredients))
		return str(percent)
	else:
		return "ERROR"
	
def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

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
	app.run(host='0.0.0.0', port=5000)