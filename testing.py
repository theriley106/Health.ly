#!/usr/bin/env python

# Prototyped with Barcode Scanner on Android and the "custom search" url
#   https://play.google.com/store/apps/details?id=com.google.zxing.client.android&hl=en_GB
#
# Routes:
#   http://[ip-address]:5001/
#   http://[ip-address]:5001/add/[barcode]


FLASK_PORT_NUMBER = 5001
FLASK_DEBUG = True
OPEN_BROWSER = False

import os
import json
import appFlask
from flask import Flask, redirect, request, make_response

def inputJson(jsonfile):
    with open(jsonfile) as json_data:
        d = json.load(json_data, strict=False)
        return d

DATABASE = inputJson('data/Database.json')


BASEDIR = os.path.dirname(__file__)
FILEPATH = os.path.join(BASEDIR, 'save.txt')

app = Flask(__name__)

@app.route('/')
@app.route('/list', methods=['GET'])
def list():
    try:
        with open(FILEPATH, "rb") as f:
            s = ''
            for line in f.readlines():
                s += line
                s += '<br>'
            return s
    except:
        return 'Nothing found in %s' % FILEPATH


@app.route('/add/<string:code>/<diet>', methods=['GET'])
def add(code, diet):
    try:
        a = 0
        with open(FILEPATH, "a+") as f:
            f.write(code)
            f.write(os.linesep)
        print code
        code = appFlask.searchByUPC(code)
        ingredients = appFlask.retIng(code)
        if ingredients != None and len(ingredients) > 0:
            for items in ingredients:
                for saveditem in DATABASE[diet]:
                    if appFlask.levenshtein(items, saveditem) < 3:
                        a += 1
            percent = float(a) / float(len(ingredients))
            if percent != 0:
                return str("{}\nPositive".format(' '.join(ingredients)))
        return str("{}\nNegative".format(' '.join(ingredients)))
    except Exception as exp:
        print exp
        return str("Negative")
    

if __name__ == "__main__":
    with open(FILEPATH, "a+") as f:
        pass

    try:
        if OPEN_BROWSER:
		    import webbrowser
		    webbrowser.open("http://localhost:%d" % FLASK_PORT_NUMBER, new=2)
    except:
        print "unable to open browser window"

    app.run(debug=FLASK_DEBUG, host = '0.0.0.0', port=FLASK_PORT_NUMBER)
