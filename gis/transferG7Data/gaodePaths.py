#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('./entity')
import os
from  entity.GISEntity import gisSession, AreaRelease
from gaode import get_gd_location,get_gd_path_by_strategy
from tools import log
import openpyxl

class Gaode_paths(object):
    '''
         计算不同高德不同策略的路径
    '''
    def __init__(self):
        # 地址
        self.__folder__ = '../data'
        self.__data_folder__='路径规划'

    def get_store_location(self,store):
        '''
             获取门店的经纬度
        '''
        lng=None  #经度
        lat =None  #纬度
        result = gisSession.query(AreaRelease).filter_by(org_short_name=store).first()
        if result!=None:
            lng=result.area_lng
            lat=result.area_lat
        else:
            print('未找到%s的数据'%store)
        return '%s,%s'%(str(lng),str(lat))

    def get_gd_all_path(self,customer,store,strategy_list):
        '''
             根据策略，客户地址和门店之间的所有路径规划
        '''
        path_dict={}
        #获取客户的高德经纬度
        customer_location=get_gd_location(customer)[1]
        #获取门店的高德经纬度
        store_location=self.get_store_location(store)

        #根据不同策略获取两个地址之间的所有的路径规划
        for strategy in strategy_list:
            path_list=get_gd_path_by_strategy(store_location,customer_location,strategy)
            path_dict[strategy]=path_list
        return path_dict

    def get_gd_path(self,customer,store,strategy):
        '''
             根据策略，客户地址和门店之间指定策略的路径规划
        '''
        #获取客户的高德经纬度
        customer_location=get_gd_location(customer)[1]
        #获取门店的高德经纬度
        store_location=self.get_store_location(store)

        #根据不同策略获取两个地址之间的路径规划
        path_list=get_gd_path_by_strategy(store_location,customer_location,strategy)
        return path_list

    def show_path(self,customer,store,strategy_list=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']):
        '''
             所有路径规划,转换为可在页面显示的数据
             例如，执行show_path('北京西城区牛街西里二区十号楼10-2','N北京P0')方法，就可以生成对应的规划路径页面
        '''
        new_path_dict={}
        path_dict=self. get_gd_all_path(customer,store,strategy_list)
        for key in path_dict:
            path_list=path_dict[key]
            n=0  #一个规则下返回的路径的数量
            for path in path_list:
                distance=path[0]   #行车距离
                #将行车路径的经纬度从字符串格式转换为列表格式
                new_location_list=[]  #路径的经纬度列表
                location_list=path[3].split(';')
                for location in location_list:
                    lng,lat=location.split(',')
                    new_location_list.append([lng,lat])
                new_path_dict[key]=new_location_list
                #生成的保存数据文件夹的完整路径
                sc_path='%s_%s'%(store,customer)
                sc_folder_path=os.path.join(self.__folder__, self.__data_folder__,sc_path)
                if not os.path.exists(sc_folder_path):
                    os.mkdir(sc_folder_path)
                #展示路径文件的完整路径
                new_filename='%s_%s_%s.html'%(key,str(n),distance)
                new_filepath=os.path.join(sc_folder_path,new_filename)
                #生成展示路径的文件
                self.write_path_file(new_filepath,str(new_location_list))
                n+=1
        return new_path_dict

    def write_path_file(self,new_filepath,data):
        '''
             生成展示路径数据的页面
        '''
        template_filepath=os.path.join(self.__folder__, '显示路径模板.html')
        with open(template_filepath, 'r', encoding='utf-8') as file:
            html=file.read()
            new_html=html.replace('#route#',data)
        with open(new_filepath, 'w', encoding='utf-8') as new_file:
            new_file.write(new_html)

    def diff_distance(self,custormer,g7_distance,store_location,customer_location,strategy):
        '''
           比较不同策略和G7返回的距离之间的差异
        '''
        new_distance=0
        new_diff=0
        try:
            path_list=get_gd_path_by_strategy(store_location,customer_location,strategy)
            if len(path_list)==1:
                path=path_list[0]
                new_distance=path[0]   #行车距离
                new_diff=abs(int(g7_distance)-int(new_distance))
            elif len(path_list)==0:
                log('%s策略%s返回路径数量为0'%(strategy,custormer))                               
            else:
                log('%s策略%s返回路径数量大于1个'%(strategy,custormer))
        except:
            log('%s策略%s请求异常'%(strategy,custormer))
        return [new_distance,new_diff]
                        
    def diff_paths(self,filename):
        '''
           从excel中读取数据，比较所有数据不同策略和G7返回的距离之间的差异
        '''
        filepath= os.path.join(self.__folder__, filename)
        wb = openpyxl.load_workbook(filepath)
        sheet = wb['第三次匹配结果']

        #遍历所有数据
        n = 0
        for row in sheet.rows:
            n+=1
            if n > 1 and (row[3].value !=None) and (row[14].value==None):
                    if row[2].value!=None:
                        g7_distance  = row[2].value  #G7送货距离
                    else:
                        g7_distance=0
                    store  = row[3].value  #门店
                    custormer=row[29].value  #客户地址  
                    customer_location = row[32].value    #高德返回客户的经纬度
                    
                    #获取门店的高德经纬度
                    store_location=self.get_store_location(store)
                    
                    #策略0产生的路径规划
                    #distance_0=0  #策略0规划路径的距离
                    #diff_0 =0     #策略0规划路径的距离与G7距离的差值
                    #distance_0,diff_0=self.diff_distance(custormer,g7_distance,store_location,customer_location,'0')

                    #策略1产生的路径规划
                    #distance_1=0  #策略1规划路径的距离
                    #diff_1=0      #策略1规划路径的距离与G7距离的差值
                    #distance_1,diff_1=self.diff_distance(custormer,g7_distance,store_location,customer_location,'1')

                    #策略5产生的路径规划
                    distance_5=0  #策略5规划路径的距离
                    diff_5=0      #策略5规划路径的距离与G7距离的差值
                    distance_5,diff_5=self.diff_distance(custormer,g7_distance,store_location,customer_location,'5')

                    #策略6产生的路径规划
                    distance_6=0  #策略5规划路径的距离
                    diff_6=0      #策略5规划路径的距离与G7距离的差值
                    distance_6,diff_6=self.diff_distance(custormer,g7_distance,store_location,customer_location,'6')

                    #策略7产生的路径规划
                    distance_7=0  #策略5规划路径的距离
                    diff_7=0      #策略5规划路径的距离与G7距离的差值
                    distance_7,diff_7=self.diff_distance(custormer,g7_distance,store_location,customer_location,'7')
                    
                    #策略0和策略1的路径取优
                    '''
                    distance=0  #最终的距离
                    diff=0   #最终的差距
                    if int(distance_1)==0:
                        distance=int(distance_0)
                        diff=diff_0
                    elif int(distance_0)==0:
                        distance=int(distance_1)
                        diff=diff_1
                    elif (int(distance_1)-int(distance_0))>10000:
                        distance=int(distance_0)
                        diff=diff_0
                    else:
                        distance=int(distance_1)
                        diff=diff_1

                    #写入
                    row[8].value = distance
                    row[9].value = diff
                    row[10].value = distance_0
                    row[11].value = diff_0
                    row[12].value = distance_1
                    row[13].value = diff_1
                    print(store,customer_location,custormer,distance_0,diff_0,distance_1,diff_1,distance,diff)
                    '''
                    row[14].value = distance_5
                    row[15].value = diff_5
                    row[16].value = distance_6
                    row[17].value = diff_6
                    row[18].value = distance_7
                    row[19].value = diff_7
                    print(store,customer_location,custormer,distance_5,diff_5,distance_6,diff_6,distance_7,diff_7)
        #保存excel
        wb.save(filepath)                    
                        
        
if __name__ == '__main__':
    # 实例化执行
    a = Gaode_paths()
    #a.diff_paths('第三次匹配结果.xlsx')
    address = "浙江省绍兴市诸暨市枫桥镇钟山村梓塘61号"
    org_name_gis ='N杭州21'
    org_name_g7 = 'N杭州24'
    print(org_name_gis)
    a.show_path(address,org_name_gis)
    print(org_name_g7)
    a.show_path(address, org_name_g7)
    print('game over')

    
