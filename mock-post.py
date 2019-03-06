# -*- coding: utf-8 -*-
# __author__="ZJL"

from flask import Flask
from flask import request
from flask import make_response, Response

import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'hello world'


def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


data = {
	"sourceCustomer": "haier",
  	"channelNo": "",
  	"resultFlag": 1,
  	"resultCode": "",
  	"resultDesc": "",
  	"errorMsg": ""
}

@app.route('/test', methods=['GET','POST'])
def test():
    if request.method == 'POST':
        a = request.get_data()
        dict1 = json.loads(a)
        print(dict1)
        return json.dumps(data)
    # else:
    #     return '<h1>只接受post请求！</h1>'

    else:
        content = json.dumps({"error_code": "1001"})
        resp = Response_headers(content)
        return resp


@app.errorhandler(403)
def page_not_found(error):
    content = json.dumps({"error_code": "403"})
    resp = Response_headers(content)
    return resp


@app.errorhandler(404)
def page_not_found(error):
    content = json.dumps({"error_code": "404"})
    resp = Response_headers(content)
    return resp


@app.errorhandler(400)
def page_not_found(error):
    content = json.dumps({"error_code": "400"})
    # resp = Response(content)  
    # resp.headers['Access-Control-Allow-Origin'] = '*'  
    resp = Response_headers(content)
    return resp
    # return "error_code:400"  


@app.errorhandler(410)
def page_not_found(error):
    content = json.dumps({"error_code": "410"})
    resp = Response_headers(content)
    return resp


@app.errorhandler(500)
def page_not_found(error):
    content = json.dumps({"error_code": "500"})
    resp = Response_headers(content)
    return resp


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=6000,debug=True, threaded=True)


