#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import openpyxl
from openpyxl import load_workbook
from entity import session, Country

class ExcelToDB(object):

    def __init__(self):
        # 地址
        self.__folder__ = 'data'

    def run(self):
        '''
            将EXCEL格式的数据导入数据库中
        '''
        province={}
        city={}
        country={}
        #获取excel对象
        filepath= os.path.join(self.__folder__, '港澳台地址.xlsx')
        wb = openpyxl.load_workbook(filepath)
        sheet = wb['Sheet2']

        #遍历所有数据
        for row in sheet.rows:
                province_name= row[0].value
                province_code = row[1].value
                city_name= row[2].value
                city_code = row[3].value
                country_name= row[4].value
                country_code = row[5].value
                print(country_name)
                if not province_code in province:
                    province[province_code] =province_name
                if not city_code in city:
                    city[city_code] =city_name                    
                if not country_code in country:
                    country[country_code] =country_name
        #插入数据库
        for province_code in province:
            province_name =province[province_code]
            self.add(province_code,province_name,'0','1')
        for city_code in city:
            city_name = city[city_code]
            parent_id ='%s0000000000' % city_code[0:2]
            self.add(city_code,city_name,parent_id,'2')
        for country_code in country:
            country_name = country[country_code]
            parent_id ='%s00000000' % country_code[0:4]
            self.add(country_code,country_name,parent_id,'3')
                    
    def add(self,id,name,parent_id,level):
        '''
             增加地址记录
        '''        
        obj=Country(
            id = id,
            name = name,                   
            parent_id = parent_id,  
            level = level
            )
        session.add(obj)
        session.commit()
        print(id,name,parent_id,level)

if __name__ == '__main__':
    print("开始")
    t = ExcelToDB()
    t.run()
    print("转换结束")

