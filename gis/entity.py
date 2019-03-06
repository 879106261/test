#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

#初始化表的父类
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
    category  = Column(String,default='')                     #城乡分类码

def initSession(ip, port, instance, user, password):
    engine = create_engine("mysql+pymysql://%s:%s@%s:%s/%s"%(user, password, ip,port,instance), max_overflow=20)    
    Session = sessionmaker(bind=engine)
    return scoped_session(Session)

#初始化数据库session
session = initSession('127.0.0.1','3306','address','root','password')
