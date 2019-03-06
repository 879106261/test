#-*- coding:utf-8 -*-
"""
created on 2019年2月24日
@author: 周迎春

"""
import  requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import threading

class WageItme(object):
    Title =  None
    Edu = None
    Wage = None
    Work_time = None


class GetWage():
    def __init__(self):
        self.__url__ = 'https://www.liepin.com/zhaopin/?isAnalysis=&dqs=020&pubTime=30&salary=&subIndustry=&industryType=&compscale=&key=%E9%AB%98%E7%BA%A7java%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88&init=-1&searchType=1&headckid=8a0c7f33f7e82943&compkind=&fromSearchBtn=2&sortFlag=15&ckid=69eb29e39a7dd4b5&degradeFlag=0&jobKind=&industries=&clean_condition=&siTag=9LP194E4Q_uQw2bhCU4kAQ%7E_UZEWASKggZZcVzClwcBJQ&d_sfrom=search_prime&d_ckId=b49ee222d40ca93ee5502f3e024b4fc0&d_curPage=0&d_pageSize=40&d_headId=377192570a765e3d920d4510d2f7bc41&curPage='
        self.__pageNum__ = 40
        self.__urls__ = self.getUrls(self.__pageNum__)
        #如果不存在目录则创建
        self.__folder__ = 'data'
        if not os.path.exists(self.__folder__ ):
            os.mkdir(self.__folder__ )
        self.__file_path__='工资.txt'
        self.__lock__ = threading.Lock()
        #记录运行的线程组
        self.__threads__=[]

    def getUrls(self,pageNum):
        urls = []
        pns = [str(i) for i in range(0, pageNum)]
        for pn in pns:
            url = self.__url__ +  pn
            urls.append(url)
        return urls

    def getThreads(self):
        #返回所有的运行的线程组
        return self.__threads__

    def insertData (self, title, edu, Wage, workTime):
        '''
            向csv文件中写入数据库地址
        '''
        #写入数据
        self.__lock__.acquire()
        filepath= os.path.join(self.__folder__, self.__file_path__)
        with open(filepath, 'a', encoding='utf-8') as file:
            obj = title+','+ edu+',' + workTime + ',' + Wage + '\n'
            print('往工资.txt写入%s'%obj)
            file.write(obj)
        self.__lock__.release()

    def getHtml(self, url):
        """请求html页面信息"""
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        soup = None
        for i in range(10):
            try:
                response = requests.get(url=url, headers=header)
                if str(response.status_code)=='200':
                    response.encoding = 'utf-8'
                    html = response.text
                    soup = BeautifulSoup(html, 'lxml')
                    break
                else:
                    print('请求地址' + url + '状态码不是200++++++++++++++++++++++++++')
            except Exception as e:
                print('请求地址' + url + '失败*****************************************************')
        if soup == None:
            print('无法请求地址' + url )
        return soup

    def run(self):
        """执行入口"""
        # 解析G工资的html
        print('开始解析上海地区java高级工程师工资信息……')
        for url in self.__urls__:
            soup = self.getHtml(url)
            tagsList = soup.select('.sojob-list li')
            for tag in tagsList:
                itme = WageItme()
                itme.Title = tag.find('a',attrs={'target':"_blank"}).get_text().strip()
                itme.Edu = tag.find('span',attrs={'class':"edu"}).get_text().strip()
                itme.Wage = tag.find('span',attrs={'class':"text-warning"}).get_text().strip()
                itme.WorkTime = tag.find_all('span')[2].get_text().strip()
                self.insertData(itme.Title , itme.Edu, itme.Wage, itme.WorkTime)
        print('工资解析结束！')


if __name__ == "__main__":
    GTI =  GetWage()
    x = GTI.run()
