import requests
import json
from flask import Flask, redirect, url_for, request, render_template, jsonify

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/chat/<chat>', methods = ['POST', 'GET'])
def callAPI(chat):
    print(chat)
    str = '{ "sender": "api", "message": "'+chat+'" }'
    print(json.loads(str))

    response_data=requests.post('http://localhost:5005/webhooks/rest/webhook',str)
    print(type(response_data))
    data = json.loads(response_data.content)
    print(data)
    print(data[0])
    print(type(data[0]))
    data_dict=data[0]
    for key in data_dict:
        print (key)
        print (data_dict[key])

    return data[0].get("text")


if __name__ == '__main__':
  app.run(host='0.0.0.0', port="8000", debug=True)