#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('./entity')
import json
import os
from datetime import datetime
import time
import requests
import openpyxl
from tools import bd2gd
from entity.testAnalyse_gis import  TestAnalyse,session

class DiffGaoBd(object):
    '''
         获取高德和百度的经纬度，并且比高德和百度的差异
    '''
    def get_gd(self,address):
        '''
             根据地址获取高德经纬度
        '''
        url = 'https://restapi.amap.com/v3/geocode/geo?address=%s&key=8d15af1f728e51175a3ac859f8b5cf4d'%address     
        response = requests.get(url=url)
        formatted_address=None   #高德请求后返回的纠正地址
        location = None      #高德返回的经纬度
        if str(response.status_code)=='200':
            response.encoding = 'utf-8'
            html = response.text     
            load_dict = json.loads (html)
            if str(load_dict['status'])=='1':
                geocodes =load_dict['geocodes']
                if len(geocodes)>0:
                    geocode= geocodes[0]
                    formatted_address= geocode['formatted_address']
                    location=geocode['location']
                    print(formatted_address,location)
            else:
                print('请求失败，返回状态是%s' % load_dict['status'])
        return [formatted_address,location]
   
    def get_all_gd(self):
        '''
             根据数据库中所有的数据，获取对应的高德经纬度
        '''
        results = session.query(TestAnalyse).all()
        for r in results:
            if r.gd_location==None:
                formatted_address,location= self.get_gd(r.address )
                r.gd_address=formatted_address
                r.gd_location=location
                session.add(r)
                session.commit()

    def get_bd(self,address):
        '''
             根据地址获取百度经纬度
        '''
        bd_location=None  #百度经纬度
        url = 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=M1cesG4z5hwGlbQrPvTaRhLnm5rM9muG'%address
        response = requests.get(url=url)      
        if str(response.status_code)=='200':
            response.encoding = 'utf-8'
            html = response.text
            print(html)
            load_dict = json.loads (html)
            if str(load_dict['status'])=='0':
                    location=load_dict['result']['location']
                    lng =location['lng']
                    lat = location['lat']
                    print(lng,lat)
                    bd_location='%s,%s'%(lng,lat)
        return bd_location
        
    def get_all_bd(self):
        '''
             根据数据库中所有的数据，获取对应的百度经纬度
        '''
        results = session.query(TestAnalyse)
        for r in results:
            if r.bd_location==None:                
                r.bd_location=self.get_bd(r.address)
                session.add(r)
                session.commit()

    def diff_ge_db(self,gd_location,bd_location):
        '''
             先将百度经纬度转换为高德经纬度，然后对比两个经纬度的差距
        '''
        gd_lng,gd_lat=gd_location.split(',')
        bd_lng,bd_lat=bd_location.split(',')
        #将百度坐标转换为高德坐标
        tmp_bd_lng,tmp_bd_lat=bd2gd(float(bd_lng),float(bd_lat))
        diff_lng= float(gd_lng)-tmp_bd_lng
        diff_lat = float(gd_lat)-tmp_bd_lat
        return [diff_lng,diff_lat]
                        
    def run_diff(self):
        '''
             根据数据库所有的数据，对比百度经纬度和高德度的差距
        '''        
        results = session.query(TestAnalyse).all()
        for r in results:
            gd_location = r.gd_location
            bd_location=r.bd_location
            if gd_location==None and bd_location==None:
                r.remark = '高德/百度无法解析地址'
            else:
                if gd_location==None:
                    r.remark = '高德无法解析地址'
                else:
                    if bd_location==None:
                        r.remark = '百度无法解析地址'
                    else:
                        diff_lng,diff_lat=self.diff_ge_db(r.gd_location,r.bd_location)
                        print(diff_lng,diff_lat)
                        r.diff_lng=diff_lng
                        r.diff_lat=diff_lat  
                        #填写备注
                        remark=''
                        if abs(diff_lng)>0.1:
                            remark='经度差距大于0.1度'
                        elif abs(diff_lng)>0.01:
                            remark='经度差距在0.01~0.1度之间'
                        
                        if abs(diff_lat)>0.1:
                            remark='%s%s'%(remark,'纬度差距大于0.1度')                        
                        elif abs(diff_lat)>0.01:
                            remark='%s%s'%(remark,'纬度差距在0.01~0.1度之间')                        
                        r.remark=remark
            session.add(r)
            session.commit()

    def save_excel(self):
        write_wb = openpyxl.Workbook()
        write_sheet = write_wb.active
        results = session.query(TestAnalyse).all()
        for r in results:
            address=r.address
            if r.gd_address==None:
                gd_address=''
            else:
                gd_address=r.gd_address
            if r.gd_location==None:
                gd_location=''
            else:
                gd_location=r.gd_location            
            if r.bd_location==None:
                bd_location=''
            else:
                bd_location=r.bd_location
            if r.diff_lng==None:
                diff_lng=''
            else:
                diff_lng=r.diff_lng
            if r.diff_lat==None:
                diff_lat=''
            else:
                diff_lat=r.diff_lat
            if r.remark==None:
                remark=''
            else:
                remark=r.remark     
            write_sheet.append([address,gd_address,gd_location,bd_location,diff_lng,diff_lat,remark])
        write_wb.save('对比数据.xlsx')
        print('保存完毕')
        
if __name__ == '__main__':
    # 实例化执行
    a = DiffGaoBd()
    a.run_diff()
    print('game over')

    
