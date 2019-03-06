# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Date, Numeric,Text
from driverForMysql import Base, initSession
from datetime import datetime


class  StandardAddr(Base):
    '''
       标准地址库
    '''
    __tablename__ = 't_standard_addr'
    id = Column(Integer,primary_key=True)      
    code = Column(String)  #标准地址记录编码
    adcode = Column(String)   #国内标准地址编码
    name = Column(String)      #地址名称
    level  = Column(String)      #地址级别
    parent_code = Column(String)      #上级地址编码
    remark  = Column(String)   #备注
    creator  = Column(String, default = 'admin')  #创建人
    create_time  = Column(Date, default = datetime.now)  #创建时间
    modifier  = Column(String, default = 'admin')   #修改人
    modify_time  = Column(Date, default = datetime.now)  #修改时间

class  StandardAddrDetail(Base):
    '''
       标准地址库，每条记录中同时记录上级地址名称和编码
    '''
    __tablename__ = 't_standard_addr_detail'
    id = Column(Integer,primary_key=True)      
    standard_addr_code = Column(String)  #标准地址记录编码
    standard_addr_detail = Column(String)   #包含上级地址的地址信息
    pcode = Column(String)      #省级地址编码
    pname  = Column(String)      #省级地址名称
    ccode = Column(String)      #市级地址编码
    cname  = Column(String)      #市级地址名称
    dcode = Column(String)      #县级地址编码
    dname  = Column(String)      #县级地址名称
    scode = Column(String)      #乡镇级地址编码
    sname  = Column(String)      #乡镇级地址名称
    remark  = Column(String)   #备注
    creator  = Column(String, default = 'admin')  #创建人
    create_time  = Column(Date, default = datetime.now)  #创建时间
    modifier  = Column(String, default = 'admin')   #修改人
    modify_time  = Column(Date, default = datetime.now)  #修改时间


#初始化标准地址数据库连接的session信息
addressSession = initSession('127.0.0.1','3306','hoau-address','root','password')
