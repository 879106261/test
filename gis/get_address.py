#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
爬取省、市、区县、乡/镇/街道、居委/村五级地址，居委/村级地址带城乡分类代码，写入CSV文件
"""
import requests
from bs4 import BeautifulSoup
from urllib import parse
import os
from datetime import datetime
import threading

class GetCity(object):
    """
       爬取国家统计局省、市、区、街道、办事处五级地址
    """

    def __init__(self):
        # 地址
        self.__url__ = ' '
        #如果不存在目录则创建
        self.__folder__ = 'data'
        if not os.path.exists(self.__folder__ ):
            os.mkdir(self.__folder__ )
        self.__file_path__='data.csv'
        self.__lock__ = threading.Lock()
        #记录运行的线程组
        self.__threads__=[]


    def getThreads(self):
        #返回所有的运行的线程组
        return self.__threads__

    def get_html(self, url):
        """请求html页面信息"""
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        soup = None
        for i in range(10):
            try:
                response = requests.get(url=url, headers=header)
                if str(response.status_code)=='200':
                    response.encoding = 'gbk'
                    html = response.text
                    soup = BeautifulSoup(html, 'lxml')
                    break
                else:
                    self.log('请求地址' + url + '状态码不是200++++++++++++++++++++++++++')
            except Exception as e:
                self.log('请求地址' + url + '失败*****************************************************')
        if soup==None:
            self.log('无法请求地址' + url )
        return soup

    def log(self, context):
        '''
            写入日志信息
        '''
        filepath= 'log2.txt'
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = '{' + time +'}' +context+'\n'
        with open(filepath, 'a', encoding='utf-8') as file:
            file.write(message)
            print(message)

    def insertDb (self, id, name, parent_id, level, category = ''):
        '''
            向csv文件中写入数据库地址
        '''
        #写入数据
        self.__lock__.acquire()
        filepath= os.path.join(self.__folder__, self.__file_path__)
        with open(filepath, 'a', encoding='utf-8') as file:
            obj = id+','+ name+','+parent_id+','+level+','+category+'\n'
            file.write(obj)
        self.__lock__.release()
        
    def get_city(self, origin_url, now_url, origin_code):
        """
          获取市级地址信息
        """
        province_url = parse.urljoin(origin_url, now_url)
        # 解析市级的html
        print('开始解析市级信息……')
        soup = self.get_html(province_url)
        city_list = soup.select('.citytr')
        for city_info in city_list:
            a_info = city_info.find_all(name='a')
            city_name = a_info[1].get_text()
            city_code = a_info[0].get_text()
            #city_code = city_code[0:4]        #市级地址只有4位
            city_url = a_info[0].attrs['href']
            print(city_name, city_code, city_url)
            #写入数据库
            self.insertDb(city_code, city_name, origin_code, '2')
            # 获取县区信息
            self.get_county(province_url, city_url, city_code)
        print('['+origin_code+']市级解析结束！')

    def get_county(self, origin_url, now_url, origin_code):
        """
            获取县、区级地址信息
        """
        city_url = parse.urljoin(origin_url, now_url)
        # 解析县区的html
        print('开始解析县/区级信息……')
        soup = self.get_html(city_url)
        county_list = soup.select('.countytr')
        for county_info in county_list:
            a_info = county_info.find_all(name='a')
            if a_info:
                county_name = a_info[1].get_text()
                county_code = a_info[0].get_text()
                #county_code = county_code[0:6]        #区县地址只有6位
                county_url = a_info[0].attrs['href']
                print(county_name, county_code, county_url)
                # 数据存入数据库
                self.insertDb(county_code, county_name, origin_code, '3')
                # 获取乡镇信息
                self.get_town(city_url, county_url, county_code)
            else:
                td_info = county_info.find_all(name='td')
                county_name = td_info[1].get_text()
                county_code = td_info[0].get_text()
                #county_code = county_code[0:6]        #区县地址只有6位
                county_url = ''
                print(county_name, county_code, county_url)
                 # 数据存入数据库
                self.insertDb(county_code, county_name, origin_code, '3')
        print('['+origin_code+']县/区级解析结束！')

    def get_town(self, origin_url, now_url, origin_code):
        """
          获取乡镇地址信息
        """
        county_url = parse.urljoin(origin_url, now_url)
        # 解析县区的html
        #print('开始解析乡镇级信息……')
        soup = self.get_html(county_url)
        town_list = soup.select('.towntr')
        for town_info in town_list:
            a_info = town_info.find_all(name='a')
            town_name = a_info[1].get_text()
            town_code = a_info[0].get_text()
            #town_code = town_code[0:9]        #乡镇街道地址只有9位
            town_url = a_info[0].attrs['href']
            #print(town_name, town_code, town_url)
            # 数据存入数据库
            self.insertDb(town_code, town_name, origin_code, '4')
            # 获取村级信息
            self.get_village(county_url, town_url, town_code)
        #print('乡镇级解析结束！')

    def get_village(self, origin_url, now_url, origin_code):
        """获取村级地址信息"""
        town_url = parse.urljoin(origin_url, now_url)
        # 解析县区的html
        #print('开始解析村级信息……')
        soup = self.get_html(town_url)
        village_list = soup.select('.villagetr')
        for village_info in village_list:
            a_info = village_info.find_all(name='td')
            village_name = a_info[2].get_text()
            village_category = a_info[1].get_text()
            village_code = a_info[0].get_text()
            #print(village_name, village_code, village_category)
            # 数据存入数据库
            self.insertDb(village_code, village_name, origin_code, '5',  village_category)
        #print('村级解析结束！')
 
    def run(self):
        """执行入口"""
        # 解析省份的html
        print('开始解析省份信息……')
        soup = self.get_html(self.__url__)
        province_list = soup.select('.provincetr a')
        print(province_list)
        for province_info in province_list:
            province_name = province_info.get_text()
            province_url = province_info.attrs['href']
            province_code = province_url.split('.')[0]
            province_code = province_code + '0000000000'    #省级代码补充到12位
            print(province_name, province_code, province_url)
            # 数据存入数据库
            self.insertDb(province_code, province_name, '0', '1')
            # 多线程爬取市级信息
            t = threading.Thread(target=self.get_city, name='LoopThread', args=(self.__url__, province_url, province_code))
            t.setDaemon(True)
            t.start()
            self.__threads__.append(t)
        print('省份解析结束！')


# 程序主入口
if __name__ == '__main__':
    # 实例化执行
    print('开始执行……')
    start_time = datetime.now()
    city = GetCity()
    city.run()
    for t in city.getThreads():
        t.join()
    end_time = datetime.now()
    print('程序执行结束！')
    print('开始时间：%s，结束时间：%s' % (start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S')))
