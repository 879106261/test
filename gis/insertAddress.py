#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
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

engine = create_engine("mysql+pymysql://admin:password@127.0.0.1:3306/address", max_overflow=20)
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

class GetCity(object):

    """
    将CSV中的数据写入数据库
    """

    def __init__(self):
        # 地址
        self.__folder__ = 'data'
        self.__file_path__='data.csv'

    def initSession(self):
        #初始化Session
        Session = sessionmaker(bind=engine)
        self.__session__ = scoped_session(Session)

    def closeSession(self):
         #关闭Session
         self.__session__.close()

    def insertDb (self, id, name, parent_id, level, category = ''):
        '''
            地址数据插入数据库,含有城乡分类编码
        '''
        obj = Country(id = id, name = name, parent_id=parent_id, level = level, category =category)
        self.__session__.add(obj)
        self.__session__.commit()

    def getData(self):
        filepath= os.path.join(self.__folder__, self.__file_path__)
        i = 1
        n = 1
        for line in open(filepath, 'r', encoding='utf-8'):
            #print(line)
            datalist = line.split(',')
            self.insertDb(datalist[0],datalist[1],datalist[2],datalist[3],datalist[4])
            i=i+1
            if (i%1000)==0:
                print ('已经导入'+ str(n*1000) + '行')
                n=n+1  

# 程序主入口
if __name__ == '__main__':
    # 实例化执行
    print('开始执行……')
    start_time = datetime.now()
    city = GetCity()
    city.initSession()
    city.getData()
    city.closeSession()
    end_time = datetime.now()
    print('程序执行结束！')
    print('开始时间：%s，结束时间：%s' % (start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S')))
