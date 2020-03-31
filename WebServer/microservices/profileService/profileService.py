import argparse
import requests
from flask import Response, Flask, request
from urllib3._collections import HTTPHeaderDict

#Create the web app
app = Flask(__name__)

url = "http://dbresolver:1337/user/"
@app.route('/login',methods=['POST'])
def login():
    response = requests.post(url + "login", data=request.form)
    return Response(response.text, response.status_code)

@app.route('/update', methods=['POST'])
def update():
    response = requests.post(url + "update", data=request.form)
    return Response(response.text, response.status_code)

@app.route('/get', methods=['GET'])
def get():
    response = requests.get(url + "get", data=request.form)
    return Response(response.text, response.status_code)


@app.route('/delete', methods=['DELETE'])
def delete():
    response = requests.delete(url + "delete", data=request.form)
    return Response(response.text, response.status_code)

@app.route('/signup',methods=['POST'])
def signup():
    response = requests.post(url + "signup", data=request.form)
    return Response(response.text, response.status_code)

@app.route('/list',methods=['GET'])
def users():
    response = requests.get(url + "list", data=request.form)
    return Response(response.text, response.status_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Provides different function calls to retrieve data from the database.'
    )

    args = parser.parse_args()
    app.run(host='0.0.0.0',port=1440,debug=True)




