# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Date, Numeric,Text
from .driverForMysql import Base, initSession,admin_code
from datetime import datetime          

class  TestAnalyse(Base):
    __tablename__ = 't_test_analyse_gis'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    address = Column(String)   
    gd_address = Column(String) 
    gd_location =Column(String)  
    bd_address  = Column(String)
    bd_location  = Column(String)
    tx_address = Column(String)
    tx_location = Column(String)
    gis_location = Column(String)
    gis_gd_diff = Column(String)
    gis_tx_diff = Column(String)
    gis_bd_diff = Column(String)
    remark = Column(String)


session = initSession('127.0.0.1','3306','test','root','123456')
