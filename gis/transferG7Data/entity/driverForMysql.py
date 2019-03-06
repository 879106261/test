#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据库引擎函数
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

'''
初始化数据库的连接
'''
def initSession(ip, port, instance, user, password):
    engine = create_engine("mysql+pymysql://%s:%s@%s:%s/%s"%(user, password, ip,port,instance), max_overflow=20)    
    Session = sessionmaker(bind=engine)
    return scoped_session(Session)

#初始化表的父类
Base = declarative_base()

#默认的初始化用户的编码
admin_code='000000000000000000'
