#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import openpyxl
from openpyxl import load_workbook

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
    __tablename__ = 'tb_country3'
    id = Column(String, primary_key=True)  #行政区域编码
    name = Column(String)                            #行政区域名称
    parent_id = Column(String)                     #父级行政区编码    
    level =Column(String)                             #行政区域级别，1省 2地市 3 区县 4乡镇街道 5村居委
    category  = Column(String)                     #城乡分类码

class DBToExcel(object):
    """
        将CSV格式数据导成Excel格式
    """
    def __init__(self):
        # 地址
        self.__folder__ = 'data'
        self.__file_path__='五级地址库.xlsx'
        Session = sessionmaker(bind=engine)
        self.__session__ = scoped_session(Session)

    def getDB(self,p_level):
        dict={}
        results = self.__session__.query(Country).filter_by(level = p_level)
        for r in results:
            dict[r.id]=r.name
        print(str(p_level) + '级地址共有' + str(len(dict)))
        return dict
          
    def toExcel(self):
        '''
             将CSV文件中所有的5级地址导入excel文件，同时写入前4级地址库
        '''
        #暂存前四级地址
        dict_province = self.getDB('1')  #省级
        dict_city = self.getDB('2')          #市级
        dict_county = self.getDB('3')     #区县
        dict_town = self.getDB('4')        #乡镇街道
        dict_village = self.getDB('5')     #乡村
             
        #获取写入数据的excel对象
        filepathExcel= os.path.join(self.__folder__, self.__file_path__)
        write_wb = openpyxl.Workbook()
        write_sheet = write_wb.active
        
        #保存数据到excel
        i = 1
        n = 1
        for id in dict_village.keys():
            #查找4级地址
            id4 = id[0:9] +'000'
            name4 = dict_town[id4]
            #查找3级地址
            id3 = id[0:6] +'000000'
            if id3 in ['460400000000','441900000000','442000000000']:
                name3 =dict_city[id3]
                print('无区县情况' + id)
            else:    
                name3 = dict_county[id3]
            #查找2级地址
            id2 = id[0:4] +'00000000'
            name2 = dict_city[id2]
            #查找1级地址
            id1 = id[0:2] +'0000000000'
            name1 = dict_province[id1]
            #写入excel
            name = dict_village[id]
            write_sheet.append([name1,id1,name2,id2,name3,id3,name4,id4,name,id])
            i=i+1
            if (i%1000)==0:
                print ('已经导入'+ str(n*1000) + '行')
                n=n+1
        #保存excel
        print ('已经导入'+ str(i) + '行')
        print('开始保存excel')
        write_wb.save(filepathExcel)
        print('完成保存excel')
        
# 程序主入口
if __name__ == '__main__':
    csv = DBToExcel()
    csv.toExcel()
    print("转换结束")

