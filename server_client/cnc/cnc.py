from flask import Flask, url_for
from flask import request
from flask import jsonify
from flask import json
import random
import sys

app = Flask(__name__)
auth = []

@app.route('/register', methods = ['GET'])
def api_location():
    if request.method == 'GET':
        #js = request.json[0]
        identifier = str(random.randint(0, sys.maxsize))
        print ("identifier: ", identifier)
        auth.append(identifier)


        return jsonify({"id":identifier})

@app.route('/request', methods = ['POST'])
def api_request():
    if request.method == 'POST':
        print("now read json payload")
        js = request.get_json()
        print (js)
        if js["id"] not in auth:
            return jsonify({"id":"error"})
        else:
            return jsonify({"commands":"ls", "type":"run", "args":[]})

@app.route('/response', methods = ['POST'])
def api_response():
    print ("api response")
    if request.method == 'POST':
        print ("now read json payload in response")
        js = request.get_json()
        print (js)
        return "",200

if __name__ == "__main__":
    app.run(host="147.46.114.22", port=6666)
