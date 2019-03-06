#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
爬取省、市、区县、乡/镇/街道、居委/村五级地址，居委/村级地址带城乡分类代码，并且直接写入数据库
"""
from bs4 import BeautifulSoup
from urllib import parse
import json
import os
from datetime import datetime
import threading
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index, Date, Numeric
from sqlalchemy.orm import sessionmaker, relationship,scoped_session
from sqlalchemy import create_engine
import time
from urllib3 import response,PoolManager

engine = create_engine("mysql+pymysql://admin:password@127.0.0.1:3306/country", max_overflow=20)
Base = declarative_base()
class  Country(Base):
    '''
        中国大陆地区五级地址库表
    '''
    __tablename__ = 'tb_country'
    id = Column(String, primary_key=True)  #行政区域编码
    name = Column(String)                            #行政区域名称
    parent_id = Column(String)                     #父级行政区编码    
    level =Column(String)                             #行政区域级别，1省 2地市 3 区县 4乡镇街道 5村居委
    category  = Column(String)                     #城乡分类码

class adress(object):
    """
       爬取国家统计局省、市、区、街道、办事处五级地址
    """
    def __init__(self):
        # 地址
        self.__url__ = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'
        #记录运行的线程组
        self.__threads__=[]
        self.initSession()

    def getThreads(self):
        #返回所有的运行的线程组
        return self.__threads__
        
    def initSession(self):
        #初始化Session
        Session = sessionmaker(bind=engine)
        self.__session__ = scoped_session(Session)

    def closeSession(self):
         #关闭Session
         self.__session__.close()

    def get_html(self, url, divclass):
        '''
          请求html
        '''
        manager = PoolManager()
        datalist = None
        for i in range(10):
            try:
                #print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'请求地址' + url + '开始')
                resp =manager.request('get',url)
                #print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'请求地址' + url + '结束')
                if str(resp.status)=='200':
                    html=resp.data.decode('GB18030')
                    soup = BeautifulSoup(html, 'lxml')
                    body =soup.body
                    datalist = body.select(divclass)
                    if len(datalist) >0:
                        break
                    else:
                        self.log('请求地址%s没有获取到数据'%url)
                        time.sleep(2)
                else:
                    self.log('请求地址%s状态码不是200'%url)
                    time.sleep(2)
            except Exception as e:
                self.log('请求地址%s失败,原因%s'%(url,repr(e)))
                time.sleep(10)                    
        if datalist==None or len(datalist) ==0:
            self.log('无法请求地址%s,class=%s' %(url,divclass))
        return datalist

    def log(self, context):
        '''
            写入日志信息
        '''
        filepath= 'log.txt'
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = '{' + time +'}' +context+'\n'
        with open(filepath, 'a', encoding='utf-8') as file:
            file.write(message)
            print(message)

    def insertDb (self, id, name, parent_id, level, category = ''):
        '''
            地址数据插入数据库,含有城乡分类编码
        '''
        obj = Country(id = id, name = name, parent_id=parent_id, level = level, category =category)
        self.__session__.add(obj)
        self.__session__.commit()
        
    def get_city(self, origin_url, now_url, origin_code):
        """
          获取市级地址信息
        """
        province_url = parse.urljoin(origin_url, now_url)
        # 解析市级的html
        print('开始解析'+origin_code+'下级市级信息……')
        city_list = self.get_html(province_url, '.citytr')
        for city_info in city_list:
            a_info = city_info.find_all(name='a')
            city_name = a_info[1].get_text()
            city_code = a_info[0].get_text()
            #city_code = city_code[0:4]        #市级地址只有4位
            city_url = a_info[0].attrs['href']
            print(city_name, city_code, city_url)
            #写入数据库
            self.insertDb(city_code, city_name, origin_code, '2')
            if city_code in ['460400000000','441900000000','442000000000']:
                #直接调乡镇处理
                print('处理地级市无区县情况')
                self.get_town(province_url, city_url, city_code)
            else:
                # 获取县区信息
                self.get_county(province_url, city_url, city_code)
        print(origin_code + '市级解析结束！')

    def get_county(self, origin_url, now_url, origin_code):
        """
            获取县、区级地址信息
        """
        print('开始解析'+origin_code+'下级县/区级信息……' )
        city_url = parse.urljoin(origin_url, now_url)
        county_list = self.get_html(city_url, '.countytr')
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
        print(origin_code+'县/区级解析结束！')

    def get_town(self, origin_url, now_url, origin_code):
        """
          获取乡镇地址信息
        """
        county_url = parse.urljoin(origin_url, now_url)
        town_list = self.get_html(county_url, '.towntr')
        for town_info in town_list:
            a_info = town_info.find_all(name='a')
            town_name = a_info[1].get_text()
            town_code = a_info[0].get_text()
            #town_code = town_code[0:9]        #乡镇街道地址只有9位
            town_url = a_info[0].attrs['href']
            # 数据存入数据库
            self.insertDb(town_code, town_name, origin_code, '4')
            #print(town_code, town_name, origin_code, '4')
            # 获取村级信息
            self.get_village(county_url, town_url, town_code)

    def get_village(self, origin_url, now_url, origin_code):
        """
            获取村级地址信息
        """
        town_url = parse.urljoin(origin_url, now_url)
        village_list = self.get_html(town_url, '.villagetr')
        for village_info in village_list:
            a_info = village_info.find_all(name='td')
            village_name = a_info[2].get_text()
            village_category = a_info[1].get_text()
            village_code = a_info[0].get_text()
            # 数据存入数据库
            self.insertDb(village_code, village_name, origin_code, '5',  village_category)
            #print(village_code, village_name, origin_code, '5',  village_category)

    def get_province(self):
        """
            获取省级地址
        """
        # 解析省份的html
        print('开始解析省份信息……')
        province_list = self.get_html(self.__url__, '.provincetr a')
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

    def run(self):
        '''
            运行入口
        '''
        print('开始执行……')
        start_time = datetime.now()
        self.get_province()
        for t in self.__threads__:
            t.join()
        end_time = datetime.now()
        print('程序执行结束！')
        print('开始时间：%s，结束时间：%s' % (start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S')))

    def singleRun(self):
        '''
            单线程爬取数据
        '''
        start_time = datetime.now()
        print('开始解析省份信息……')
        province_list = self.get_html(self.__url__, '.provincetr a')
        for province_info in province_list:
            province_name = province_info.get_text()
            province_url = province_info.attrs['href']
            province_code = province_url.split('.')[0]        
            province_code = province_code + '0000000000'    #省级代码补充到12位
            print(province_name, province_code, province_url)
            # 数据存入数据库
            self.insertDb(province_code, province_name, '0', '1')
            # 爬取市级信息
            self.get_city(self.__url__, province_url, province_code)
        print('省份解析结束！')
        end_time = datetime.now()
        print('程序执行结束！')
        print('开始时间：%s，结束时间：%s' % (start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S')))
        
            
if __name__ == '__main__':
    # 实例化执行
    city = adress()
    city.run()

    
