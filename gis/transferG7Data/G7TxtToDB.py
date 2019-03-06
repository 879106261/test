# -*- coding: utf-8 -*-
import sys
sys.path.append('./entity')
import json
import os
from datetime import datetime
from  entity.G7Entity import session, Station
     
class ToDB(object):

    def __init__(self):
        # 地址
        self.__folder__ = '../data/制图数据'
  
    def toStation(self):
        '''
           将抓取的服务范围数据导入数据库中
        '''
        #遍历目录下所有的文本文件
        dirpath= self.__folder__
        files = os.listdir(dirpath)
        for file in files:
            #if file == '四川省.txt':
                filepath = os.path.join(dirpath,file)
                with open(filepath, 'r', encoding='utf-8') as load_f:
                    #将文本文件的内容加载成json格式
                    print("读取文件" + filepath)
                    load_dict = json.load(load_f)
                    #取出其中的制图范围数据
                    dataArray = load_dict['data']['result']
                    #所有数据插入数据库
                    for  data in dataArray:
                        #处理部分数据没有bound的情况
                        if 'bound' in data.keys():
                            tmp_bound = data['bound']
                        else:
                            tmp_bound = ''
                        #处理机构名称中的(未审核)字样
                        tmp_name = data['name'].replace('(未审核)','').strip()
                        
                        #向表中插入数据
                        obj = Station(
                                id = data['id'],
                                orgcode = data['orgcode'],
                                code =  data['code'],
                                types = data['types'],  
                                name  =  tmp_name, 
                                address  =  data['address'], 
                                lat  =  data['lat'],
                                lng  =  data['lng'], 
                                radius  =  data['radius'], 
                                linkman  =  data['linkman'], 
                                phone  =  data['phone'], 
                                #createtime  =  data['createtime'], 
                                #updatetime  =  data['updatetime'], 
                                bounded  =  data['bounded'], 
                                area  =  data['area'], 
                                used  =  data['used'], 
                                issync  =  data['issync'], 
                                parentid  =  data['parentid'], 
                                provinceid  = data['provinceid'], 
                                cityid  = data['cityid'], 
                                partid  =  data['partid'],   
                                remark  =  data['remark'], 
                                color  =  data['color'], 
                                maxlat  =  data['maxlat'], 
                                maxlng  =  data['maxlng'], 
                                minlat  =  data['minlat'], 
                                minlng  =  data['minlng'], 
                                maptype  =  data['maptype'], 
                                operateid = data['operateid'], 
                                areadesc = data['areadesc'], 
                                orgcheck = data['orgcheck'], 
                                issignlist = data['issignlist'], 
                                isEdit = data['isEdit'], 
                                orgcheck_opt = data['orgcheck_opt'], 
                                orgname = data['orgname'], 
                                bound =  tmp_bound
                            )
                        session.add(obj)
                        session.commit()

if __name__ == '__main__':
    print('开始执行……')
    toDB = ToDB()
    toDB.toStation()
    print('程序执行结束！')
