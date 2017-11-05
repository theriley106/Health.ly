#!/usr/bin/env python

# Prototyped with Barcode Scanner on Android and the "custom search" url
#   https://play.google.com/store/apps/details?id=com.google.zxing.client.android&hl=en_GB
#
# Routes:
#   http://[ip-address]:5001/
#   http://[ip-address]:5001/add/[barcode]


FLASK_PORT_NUMBER = 8000
FLASK_DEBUG = True
OPEN_BROWSER = True

import os
from flask import Flask, redirect, request, make_response

BASEDIR = os.path.dirname(__file__)
FILEPATH = os.path.join(BASEDIR, 'save.txt')

app = Flask(__name__)

@app.route('/')
def li():
    return '''<a href="zxing://scan/?ret=http%3A%2F%2Ffoo.com%2Fproducts%2F%7BCODE%7D%2Fdescription&SCAN_FORMATS=UPC_A,EAN_13"> 
    <span>My scan</span>
</a>
'''
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


@app.route('/add/<string:code>', methods=['GET'])
def add(code):
    with open(FILEPATH, "a+") as f:
        f.write(code)
        f.write(os.linesep)
    return redirect('/')
    

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
