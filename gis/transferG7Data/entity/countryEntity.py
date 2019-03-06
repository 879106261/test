# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Date, Numeric,Text
from driverForMysql import Base, initSession
from datetime import datetime

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

#初始化标准地址数据库连接的session信息
session = initSession('127.0.0.1','3306','country','root','password')
