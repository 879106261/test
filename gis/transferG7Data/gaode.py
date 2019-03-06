#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests

def get_gd_location(address):
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
        else:
            print('请求失败，返回状态是%s' % load_dict['status'])
    else:
        print('请求失败，响应码非200')      
    return [formatted_address,location]

def get_gd_path_by_strategy(origin,destination,strategy):
    '''
         根据策略，计算两组经纬度之间的路径规划
    '''
    path_list=[]  #返回的路径规划列表
    url = 'https://restapi.amap.com/v3/direction/driving?origin=%s&destination=%s&strategy=%s&extensions=base&key=8d15af1f728e51175a3ac859f8b5cf4d' %(origin,destination,strategy)
    response = requests.get(url=url)
    if str(response.status_code)=='200':
        response.encoding = 'utf-8'
        html = response.text     
        load_dict = json.loads (html)
        if str(load_dict['status'])=='1':
            paths = load_dict['route']['paths']
            for path  in paths:
                distance=path['distance']  #行车距离
                duration=path['duration']  #行车时间
                tolls=path['tolls']  #收费
                steps=path['steps'] #行车路径
                polyline_list=[]
                for step in steps:
                    polyline =step['polyline']
                    polyline_list.append(polyline)
                polyline_str=';'.join(polyline_list)  #行车路径的经纬度
                path_list.append([distance,duration,tolls,polyline_str])
        else:
            print('请求失败，返回状态是%s' % load_dict['status'])
    else:
        print('请求失败，响应码非200')
    print(strategy)
    print(path_list)
    return path_list

