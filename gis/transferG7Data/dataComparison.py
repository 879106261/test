# -*- coding: utf-8 -*-
import sys
sys.path.append('./entity')


import os
import openpyxl
from datetime import datetime
from sqlalchemy import and_

from entity.addressEntity import addressSession as session, StandardAddrDetail
from entity.GISEntity import Area,gisSession
from tools import log


class  CompareData():
    """
        将EXCEL文件中的机构信息与Area数据进行对比
    """

    def __init__(self):
        # 地址
        self.__folder__ = '../data'
        # 版图编码
        self.all_territory_code = '244423365703815168'  # 全部版图编码
        self.pick_territory_code = '244423366521704448'  # 自提版图编码
        self.deliver_territory_code = '244423366479761408'  # 派送版图编码

    def queryArea(self,area_name,territory_code):
        '''
         查询area表机构standard_addr_code
        '''
        results = gisSession.query(Area.standard_addr_code).filter(and_(Area.area_name == area_name ,Area.territory_code == territory_code)).all()
        if  len(results) == 1:            
            return results[0][0]
        gisSession.close()


    def queryStandardAddrDetail(self,area_name,standard_addr_code):
        '''
         查询StandardAddrDetail表的地址,使用Area表中standard_addr_code查询
        '''
        results = session.query(StandardAddrDetail.standard_addr_detail).filter_by(standard_addr_code = standard_addr_code).all()
        if len(results) == 1:
            return results[0][0]
        session.close()

    def excel_compare_db(self,sheet_name,file_name):
        '''
             将EXCEL文件中的机构信息导入数据库中
        '''
        #获取excel对象
        filepath= os.path.join(self.__folder__, file_name)
        wb = openpyxl.load_workbook(filepath)
        sheet = wb[sheet_name]

        #根据sheet类型，判断版图类型
        if sheet_name =='全部版图':
            territory_code = self.all_territory_code
        elif sheet_name =='派送':
            territory_code = self.deliver_territory_code
        else:
            territory_code = self.pick_territory_code

        #遍历所有数据
        n = 0
        for row in sheet.rows:
            n+=1
            if (n > 1) and (row[0].value !=None):
                short_name = row[2].value  #机构简称
                #拼接详细地址
                address = ''
                province_name = row[3].value
                if province_name!=None:
                    address='%s%s' %(address,province_name.strip())
                city_name = row[4].value
                if city_name!=None:
                    address='%s%s' %(address,city_name.strip())                
                country_name = row[5].value
                if country_name!=None:
                    address='%s%s' %(address,country_name.strip())    
                town_name = row[6].value
                if town_name!=None:
                    address='%s%s' %(address,town_name.strip())    
                print(address)
                #在t_area表查询standard_addr_code
                standard_addr_code = self.queryArea(short_name,territory_code)
                
                if standard_addr_code != None:
                    # 查询standard_addr_detail
                    standard_addr_detail = self.queryStandardAddrDetail(short_name,standard_addr_code)
                    if standard_addr_detail != None and standard_addr_detail== address :
                        print('{' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '}'+ '%s文件%s中的%s机构原始四级地址和数据库中四级地址一致\n' % (file_name,sheet_name,short_name))
                    else:
                        log('%s[%s]中,机构=%s,地址=%s,数据库地址=%s' % (file_name,sheet_name,short_name,address,standard_addr_detail))
                else:
                    log('%s文件%s中的%s机构在Area表中不存在' % (file_name,sheet_name,short_name))


    def run(self,filename):
        self.excel_compare_db('全部版图', filename)  #全部版图的数据
        self.excel_compare_db('派送',filename) #派送版图的数据
        self.excel_compare_db('自提',filename) #自提版图的数据

# 程序入口
if __name__ == '__main__':
    # 实例化执行
    print('开始执行……')
    t= CompareArea()
    #将EXCEL文件中的机构信息与Area数据进行对比
    excel_data = ['加盟门店数据.xlsx','直营门店数据.xlsx','偏线机构数据.xlsx','平台机构数据.xlsx' ]
    for x in excel_data:
        t.run(x)
    #t.run('加盟门店数据.xlsx')
    print('对比结束，请查看对比日志……')
