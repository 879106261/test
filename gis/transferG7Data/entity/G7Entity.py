# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Date, Numeric,Text
from driverForMysql import Base, initSession
from datetime import datetime

class  Station(Base):
    '''
       G7服务范围表
    '''
    __tablename__ = 'tb_station'
    id = Column(Integer,primary_key=True)      
    orgcode = Column(String) 
    code = Column(String)     
    types =Column(String) 
    name  = Column(String)
    address  = Column(String)
    lat  = Column(Numeric(10,6))
    lng  = Column(Numeric(10,6))
    radius  = Column(String)
    linkman  = Column(String)
    phone  = Column(String)
    createtime  = Column(Date)
    updatetime  = Column(Date)
    bounded  = Column(String)
    area  = Column(String)
    used  = Column(String)
    issync  = Column(String)
    parentid  = Column(String)
    provinceid  = Column(String)
    cityid  = Column(String)
    partid  = Column(String)    
    remark  = Column(String)
    color  = Column(String)
    maxlat  = Column(Numeric(10,6))
    maxlng  = Column(Numeric(10,6))
    minlat  = Column(Numeric(10,6))
    minlng  = Column(Numeric(10,6))
    maptype  = Column(String)
    operateid = Column(String)
    areadesc = Column(String)
    orgcheck = Column(String)
    issignlist = Column(String)
    isEdit = Column(String)
    orgcheck_opt = Column(String)
    orgname = Column(String)
    bound = Column(Text)    

#初始化G7数据库连接的session信息
session = initSession('127.0.0.1','3306','g7','root','password')
