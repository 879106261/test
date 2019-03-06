# -*- coding: utf-8 -*-

from datetime import datetime
import jpype

def log(context):
    '''
        写入日志信息
    '''
    filepath= 'log.txt'
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = '{' + time +'}' +context+'\n'
    with open(filepath, 'a', encoding='utf-8') as file:
        file.write(message)
        print(message)

def initJVM():
    '''
        初始化java虚拟机
    '''
    jvmPath = jpype.getDefaultJVMPath()
    jvmArg = '-Djava.class.path=./lib;./lib/plus-util-1.0.0.jar;./lib/commons-lang3-3.8.1.jar;./lib/spring-data-commons-2.1.4.RELEASE.jar'
    if not jpype.isJVMStarted():
         jpype.startJVM(jvmPath, jvmArg)

def codeGenerator():
    '''
        生成唯一编码
    '''
    code = ''
    codeGenerator=jpype.JClass("com.anji.plus.util.CodeGenerator")
    code = codeGenerator.getCodeStr()  #生成编码
    return code

def hoauGd2bd(lng,lat):
    '''
    高德坐标转换为华宇使用的坐标
    '''
    CoodinateCovertor=jpype.JClass("com.coordinate.CoodinateCovertor")
    PointPo=jpype.JClass("com.coordinate.PointPo")
    point = PointPo(lng,lat)
    new_point =CoodinateCovertor.hoauGd2bd(point)
    new_lng = new_point.getX()
    new_lat = new_point.getY()
    return [new_lng,new_lat]

def bd2gd(lng,lat):
    '''
    百度坐标转高德坐标
    '''
    CoodinateCovertor=jpype.JClass("com.coordinate.CoodinateCovertor")
    PointPo=jpype.JClass("com.coordinate.PointPo")
    point = PointPo(lng,lat)
    new_point =CoodinateCovertor.bd2gd(point)
    new_lng = new_point.getX()
    new_lat = new_point.getY()
    return [new_lng,new_lat]
    
def hoauGdBorder2bdBorder(border):
    '''
    高德坐标范围转换为华宇使用的坐标范围
    '''
    CoodinateCovertor=jpype.JClass("com.coordinate.CoodinateCovertor")
    return CoodinateCovertor.hoauGdBorder2bdBorder(border)

def getmaxminlonlat(poyline):
    '''
    根据坐标范围计算出最大、最小经纬度
    '''
    CheckPoylinePoint=jpype.JClass("com.coordinate.CheckPoylinePoint")
    point_dict = CheckPoylinePoint.getmaxminlonlat(poyline)
    min_lng = point_dict['minlng']
    min_lat = point_dict['minlat']
    max_lng = point_dict['maxlng']
    max_lat = point_dict['maxlat']
    return [float(min_lng),float(min_lat),float(max_lng),float(max_lat)]

#初始化JAVA虚拟机
initJVM()

if __name__ == '__main__':
    print(bd2gd(119.94343167667479,31.672903473648443))
