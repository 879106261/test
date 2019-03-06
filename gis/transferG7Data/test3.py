#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

sys.path.append('./entity')
import json
import requests
import openpyxl
from tools import bd2gd
from entity.testAnalyse_gis import TestAnalyse, session
import threading

class DiffGaoBd(object):
    '''
         获取高德、百度、腾讯的经纬度，并且比三者之间的差距
    '''

    def get_gis(self, address, city):
        '''
             根据地址获取GIS经纬度
        '''
        url = 'http://10.108.2.112/hoau/gis/queryExactlyArea'
        headers = {"Content-Type": "application/json"}
        data = {
                  "reqId": "3asr23ar455ds56st56strt34tyd678g",
                  "reqTime": "2018-12-30 15:15:15 999",
                  "reqData": {
                    "serviceType": "SITE_DELIVERY",
                    "address": address,
                    "lat": "",
                    "lng": "",
                    "pcode": "121212121211",
                    "ccode": city+"000000",
                    "dcode": "121212121222",
                    "scode": "121212121212",
                    "vcode": "121212121212"
                  }
                }
        print(data)
        response = requests.post(url,  json=data, headers=headers)
        gis_location = None #GIS返回的经纬度
        remark = None
        print(response.status_code)
        print(response.text)
        if str(response.status_code) == '200':
            print('GIS开始地址解析：%s' % address)
            response.encoding = 'utf-8'
            html = response.text
            load_dict = json.loads(html)
            if str(load_dict['resultCode']) == '000000':
                destLng = load_dict['repData']['destLng']
                destLat = load_dict['repData']['destLat']
                Lng = destLng - 0.006
                Lat = destLat -0.0065
                gis_location = '%s,%s' % (Lng, Lat)
            else:
                remark = load_dict['resultMsg']
        return [gis_location,remark]

    def get_gd(self, address, city):
        '''
             根据地址获取高德经纬度
        '''
        url = 'https://restapi.amap.com/v3/geocode/geo?key=8d15af1f728e51175a3ac859f8b5cf4d&address=%s&city=%s' % (
        address, city)
        response = requests.get(url=url)
        formatted_address = None  # 高德请求后返回的纠正地址
        location = None  # 高德返回的经纬度
        if str(response.status_code) == '200':
            print('高德开始地址解析：%s' % address)
            response.encoding = 'utf-8'
            html = response.text
            load_dict = json.loads(html)
            if str(load_dict['status']) == '1':
                geocodes = load_dict['geocodes']
                if len(geocodes) > 0:
                    geocode = geocodes[0]
                    formatted_address = geocode['formatted_address']
                    location = geocode['location']
            else:
                print('请求失败，返回状态是%s' % load_dict['status'])
        return [formatted_address, location]

    def get_bd(self, address):
        '''
             根据地址获取百度经纬度
        '''
        bd_location = None  # 百度经纬度
        url = 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=M1cesG4z5hwGlbQrPvTaRhLnm5rM9muG' % address
        response = requests.get(url=url)
        if str(response.status_code) == '200':
            print('百度开始地址解析：%s' % address)
            response.encoding = 'utf-8'
            html = response.text
            # print(html)
            load_dict = json.loads(html)
            if str(load_dict['status']) == '0':
                location = load_dict['result']['location']
                lng = location['lng']
                lat = location['lat']
                # 将百度坐标转换为高德坐标
                tmp_bd_lng, tmp_bd_lat = bd2gd(float(lng), float(lat))
                bd_location = '%s,%s' % (tmp_bd_lng, tmp_bd_lat)
        return bd_location

    def get_tx(self, address):
        '''
             根据地址获取腾讯经纬度
        '''
        tx_location = None  # 腾讯经纬度
        url = 'https://apis.map.qq.com/ws/geocoder/v1/?address=%s&key=SXUBZ-J5T3G-BJOQW-I6MAZ-ON2PJ-PWFPN' % address
        response = requests.get(url=url)
        if str(response.status_code) == '200':
            print('腾讯开始地址解析：%s' % address)
            response.encoding = 'utf-8'
            html = response.text
            load_dict = json.loads(html)
            if str(load_dict['status']) == '0':
                location = load_dict['result']['location']
                lng = location['lng']
                lat = location['lat']
                tx_location = '%s,%s' % (lng, lat)
        return tx_location

    def get_all_location(self):
        '''
             根据数据库中所有的数据，获取对应的经纬度
        '''
        results = session.query(TestAnalyse).all()
        for r in results:
            # 获取高德经纬度
            if r.gd_location == None:
                r.gd_address, r.gd_location = self.get_gd(r.address, r.city)
            # 获取百度经纬度
            if r.bd_location == None:
                r.bd_location = self.get_bd(r.address)
            # 获取腾讯经纬度
            if r.tx_location == None:
                r.tx_location = self.get_tx(r.address)
            #获取GIS经纬度
            if r.gis_location == None:
                r.gis_location,r.remark = self.get_gis(r.address,r.city)
            session.add(r)
            session.commit()

    def diff_distance(self,origin_location,destination_location):
        '''
             调用高德接口，使用经纬度测距
        '''
        distance = None  # 距离
        url = 'https://restapi.amap.com/v3/distance?key=8d15af1f728e51175a3ac859f8b5cf4d&origins=%s&destination=%s&type=0'%(origin_location,destination_location)
        response = requests.get(url=url)
        if str(response.status_code) == '200':
            response.encoding = 'utf-8'
            html = response.text
            print(html)
            load_dict = json.loads(html)
            if str(load_dict['status']) == '1':
                distance = load_dict['results'][0]['distance']
        return distance

    def run_diff(self):
        '''
             根据数据库所有的数据，对比高德、百度、腾讯的坐标距离
        '''
        threads = []
        results = session.query(TestAnalyse).all()
        for r in results:
            gd_location = r.gd_location
            bd_location = r.bd_location
            tx_location = r.tx_location
            gis__location = r.gis_location
            if r.id > 8846:
                print(r.id)
                if r.gis_gd_diff == None:
                    #对比gis和高德距离
                    r.gis_gd_diff = self.diff_distance(gis__location,gd_location)
                    # 对比gis和腾讯距离
                    r.gis_tx_diff = self.diff_distance(gis__location,tx_location)
                    # 对比gis和百度距离
                    r.gis_bd_diff = self.diff_distance(gis__location,bd_location)
                session.add(r)
                session.commit()
        print('gis、高德、百度、腾讯的坐标距离对比完毕')

    def save_excel(self):
        write_wb = openpyxl.Workbook()
        write_sheet = write_wb.active
        results = session.query(TestAnalyse).all()
        for r in results:
            address = r.address
            if r.city ==None:
                city = ''
            else:
                city = r.city
            if r.gd_address == None:
                gd_address = ''
            else:
                gd_address = r.gd_address
            if r.gd_location == None:
                gd_location = ''
            else:
                gd_location = r.gd_location
            if r.bd_location == None:
                bd_location = ''
            else:
                bd_location = r.bd_location

            if r.tx_location == None:
                tx_location = ''
            else:
                tx_location = r.tx_location

            if r.gis_location == None:
                gis_location = ''
            else:
                gis_location = r.gis_location

            if r.gis_gd_diff == None:
                gis_gd_diff = ''
            else:
                gis_gd_diff = r.gis_gd_diff

            if r.gis_tx_diff == None:
                gis_tx_diff = ''
            else:
                gis_tx_diff = r.gis_tx_diff

            if r.gis_bd_diff == None:
                gis_bd_diff = ''
            else:
                gis_bd_diff = r.gis_bd_diff

            # if r.diff_lng == None:
            #     diff_lng = ''
            # else:
            #     diff_lng = r.diff_lng
            # if r.diff_lat == None:
            #     diff_lat = ''
            # else:
            #     diff_lat = r.diff_lat
            if r.remark == None:
                remark = ''
            else:
                remark = r.remark

            # write_sheet.append([address, gd_address, gd_location, bd_location, diff_lng, diff_lat, remark])
            write_sheet.append([city,address, gd_address, gd_location, bd_location, tx_location, gis_location,gis_gd_diff,gis_tx_diff,gis_bd_diff, remark])
        write_wb.save('GIS对比数据.xlsx')
        print('保存完毕')

if __name__ == '__main__':
    # 实例化执行
    a = DiffGaoBd()
    # a.run_diff()
    a.save_excel()
    print('game over')

