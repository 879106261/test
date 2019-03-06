# -*- coding: utf-8 -*-
from urllib import request, parse
import http.cookiejar
import time
import os
import json

class PullData(object):
    '''
    从G7系统抓取区域的绘图数据
    '''
    def __init__(self):
        #G7地址
        #self.__url__ = "http://101.95.26.138:88/inside.php" #测试环境
        self.__url__ = "http://10.39.59.167/inside.php"
        #设置获取cookie
        cookie=http.cookiejar.CookieJar()
        cookie_handler=request.HTTPCookieProcessor(cookie)
        self.__opener__=request.build_opener(cookie_handler)
        #设置请求头信息
        self.__headers__ = {'Content-Type':'application/x-www-form-urlencoded'}
        #如果不存在目录则创建
        self.__folder__ = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "..")), 'data/制图数据')
        if not os.path.exists(self.__folder__ ):
            os.mkdir(self.__folder__ )
        #设置省级地址码
        self.__province__ = {
            '1' : '北京市',
            '21' : '天津市',
            '36' : '河北省',
            '48' : '山西省',
            '59' : '内蒙古',
            '70' : '辽宁省',
            '85' : '吉林省',
            '94' : '黑龙江省',
            '108' : '上海市',
            '128' : '江苏省',
            '142' : '浙江省',
            '154' : '安徽省',
            '172' : '福建省',
            '182' : '江西省',
            '194' : '山东省',
            '212' : '河南省',
            '230' : '湖北省',
            '248' : '湖南省',
            '263' : '广东省',
            '285' : '广西自治区',
            '300' : '海南省',
            '303' : '重庆市',
            '342' : '四川省',
            '363' : '贵州省',
            '373' : '云南省',
            '391' : '西藏自治区',
            '399' : '陕西省',
            '409' : '甘肃省',
            '424' : '青海省',
            '433' : '宁夏回族自治区',
            '439' : '新疆维吾尔自治区',
            '457' : '香港特别行政区',
            '459' : '澳门特别行政区',
            '461' : '台湾省'
        }

    def post(self, params, data=''):
        ''''
            用POST方式发送请求，带有登录产生的cookie信息
        '''
        #拼出完整的请求url
        posturl = self.__url__ +"?"+ parse.urlencode(params)
        #请求头信息
        
        #数据转换为utf-8编码
        data = data.encode('utf-8')
        #发送请求
        response = self.__opener__.open( request.Request(posturl, data = data, headers=self.__headers__, method="POST"))
        #打印请求的响应信息
        page = response.read().decode('unicode_escape')
        #print(page)
        return page

    def saveAsFile(self, content, filename):
        '''
            将在字符串保存到文本文件中
        '''
        filename= os.path.join(self.__folder__, filename)
        try:    
            f = open(filename,'w',encoding='utf-8')
            f.write(content)
            f.close()
            print('数据文件%s保存完毕' % filename)
        except Exception as e:
            print ('保存数据文件%s出错' % filename)
            print(e)
            
    def login(self):
        '''
        登录G7系统
        '''
        #username = 'tdhyzb_admin'  #登录用户名
        #password = 'hoau123456'     #登录密码
        username = 'ningbo9'  #登录用户名
        password = 'HOAU123456'     #登录密码
        logurl = self.__url__ + '?t=json&m=login&f=getallcode&opurl=/login/index.html'
        data = "username=%s&password=%s&checkcode=&loginflag=1&cookietime=0&isgetcode=1" % (username,password)
        data = data.encode('utf-8')
        #登录请求连接
        response = self.__opener__.open(request.Request(logurl, data = data, headers=self.__headers__))
        page = response.read().decode('unicode_escape')
        print(page)

    def getStation(self):
        '''
        获取制图范围数据
        '''
        '''
        self.__province__ ={
            '182' : '江西省'
            }
        '''
        self.login()
        #遍历获取所有省份数据
        for id in self.__province__:
            params = {
                't':'json',
                'm':'station',
                'f':'search',
                'page_no':'1',
                'page_size':'5000',
                'getbound':'true',
                'types':'20',
                'provinceid':id
            }

            #请求数据
            page = self.post(params) 
            time.sleep(10)
            
            #数据写入本地文本文件
            filename= self.__province__[id] + '.txt'
            self.saveAsFile(page, filename)

    def getOrg(self):
        '''
            获取机构数据，暂时未用
        '''
        #登录系统
        self.login()
        #抓取机构数据
        params = {
            't':'json',
            'm':'org',
            'f':'search',
            'opurl':'/org/index.html'
        }
        data = "page_no=1&page_size=5000&sortname=undefined&sortorder=undefined&query=&qtype=&qop=Eq"

        #请求数据
        page = self.post(params, data) 

        #数据写入本地文本文件
        self.saveAsFile(page, '机构数据.txt')

    def getUser(self):
        '''
            获取用户数据,暂时未用
        '''
        #登录系统
        self.login()
        #抓取用户数据
        params = {
            't':'json',
            'm':'user',
            'f':'search',
            'opurl':'/user/index.html'
        }
        data = "page_no=1&page_size=5000&sortname=undefined&sortorder=undefined&query=&qtype=&qop=Eq"
        #请求数据
        page = self.post(params, data) 

        #数据写入本地文本文件
        self.saveAsFile(page, '用户数据.txt')          
            
if __name__ == '__main__':
    print("start......")
    gis = PullData()
    gis.getStation()
    print ("game over!")
