import requests
import time
from time import sleep
from excel_use import read_data,write_data
import config

#订单创建excel
filePath = "海尔接口测试用例参数.xlsx"
sheetName = "创建订单-客户"
#请求url 方式 内容 响应内容的列名
url = 'C'
request_type= 'D'
request_params = 'E'
response_params = 'F'


class create_order():
    def __init__(self):
        self.url = read_data(filePath,sheetName,url)
        self.type = read_data(filePath,sheetName,request_type)
        self.data = read_data(filePath,sheetName,request_params)

    def post_create_order(self):
        headers = {"Content-Type":"text/plain"}
        response_data = []
        #利用python自带的zip函数可同时对两个列表进行遍历
        for url,type,request_params,in zip(self.url,self.type,self.data):
            execTime = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            sleep(1)
            if type =='get':
                #get请求的request_params按照{'show_env':1}
                r = requests.get(url,params = request_params)
                response_data.append(r.text + "  " + execTime)
            else :
                r = requests.post(url, json=request_params, headers=headers)
                response_data.append(r.text+"  "+execTime)
        write_data(filePath,sheetName,response_data,response_params)

if __name__ == "__main__":
    x = create_order()
    x.post_create_order()