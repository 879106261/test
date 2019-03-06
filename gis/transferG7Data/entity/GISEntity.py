# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Date, Numeric,Text
from driverForMysql import Base, initSession,admin_code
from datetime import datetime          

class  Territory(Base):
    '''
       版图表
    '''
    __tablename__ = 't_territory'
    id = Column(Integer,primary_key=True)      
    territory_code = Column(String)  #版图编码
    territory_name = Column(String)   #版图名称
    show_order = Column(Integer)      #显示顺序
    service_type = Column(String)      #服务类型
    remark  = Column(String)   #备注
    creator  = Column(String, default = admin_code)  #创建人
    create_time  = Column(Date, default = datetime.now)  #创建时间
    modifier  = Column(String, default =admin_code)   #修改人
    modify_time  = Column(Date, default = datetime.now)  #修改时间

class  Area(Base):
    '''
       区域
    '''
    __tablename__ = 't_area'
    id = Column(Integer,primary_key=True)      
    area_code = Column(String)     #编码
    area_name = Column(String)    #区域名称
    parent_area =Column(String)    #上级区域
    territory_code  = Column(String)  #所属版图
    area_type  = Column(String)   #区域类型
    conn_entity  = Column(String, nullable=False)  #关联实体
    standard_addr_code  = Column(String)     #标准地址code
    detail_add  = Column(String)  #详细地址
    dead_sts  = Column(String)    #停用启用状态
    status  = Column(String)    #状态
    remark  = Column(String)   #备注
    creator  = Column(String, default = admin_code)  #创建人
    create_time  = Column(Date, default = datetime.now)  #创建时间
    modifier  = Column(String, default = admin_code)   #修改人
    modify_time  = Column(Date, default = datetime.now)  #修改时间

class  AreaFeature(Base):
    '''
       区域要素表
    '''
    __tablename__ = 't_area_feature'
    id = Column(Integer,primary_key=True)      
    code = Column(String)  #编码
    area_code = Column(String)   #区域编码
    area_lng = Column(Numeric(12, 8))  #经度
    area_lat =  Column(Numeric(12, 8))  #纬度
    service_type =Column(String)   #服务类型
    coordinate_system = Column(String)      #坐标系
    feature_type = Column(String)      #要素类型,点或者面
    layer_color = Column(String)      #图层颜色
    border = Column(String)      #范围坐标
    remark  = Column(String)   #备注
    creator  = Column(String, default = admin_code)  #创建人
    create_time  = Column(Date, default = datetime.now)  #创建时间
    modifier  = Column(String, default = admin_code)   #修改人
    modify_time  = Column(Date, default = datetime.now)  #修改时间

class  AreaRelease(Base):
    '''
       区域
    '''
    __tablename__ = 't_area_release'
    id = Column(Integer,primary_key=True)      
    area_code = Column(String)     #编码
    service_type = Column(String)     #服务类型
    org_code =  Column(String)     #机构编码
    org_name = Column(String)    #机构名称
    org_short_name = Column(String)    #机构简称
    org_numb = Column(String)    #机构代码
    org_mobile_phone =  Column(String)    #手机
    org_telephone =  Column(String)    #固定电话
    coordinate_system = Column(String)      #坐标系
    feature_type = Column(String)      #要素类型,点或者面
    layer_color = Column(String)      #图层颜色
    area_lng = Column(Numeric(12, 8))  #经度
    area_lat =  Column(Numeric(12, 8))  #纬度
    bd_area_lng = Column(Numeric(12, 8))  #百度经度
    bd_area_lat =  Column(Numeric(12, 8))  #百度纬度
    border = Column(String)      #范围坐标
    bd_border = Column(String)      #百度范围坐标
    min_lng = Column(Numeric(12, 8))  #最小经度
    min_lat = Column(Numeric(12, 8))  #最小纬度
    max_lng = Column(Numeric(12, 8))  #最大经度
    max_lat = Column(Numeric(12, 8))  #最大纬度
    remark  = Column(String)   #备注
    creator  = Column(String, default = admin_code)  #创建人
    create_time  = Column(Date, default = datetime.now)  #创建时间
    modifier  = Column(String, default = admin_code)   #修改人
    modify_time  = Column(Date, default = datetime.now)  #修改时间

class  OrgRelease(Base):
    '''
       部门地址库
    '''
    __tablename__ = 't_org_release'
    id = Column(Integer,primary_key=True)
    code = Column(String)      #自动生成code
    name  = Column(String)      #公司名称
    short_name = Column(String)      #公司简称
    address  = Column(String)      #地址
    area_lng = Column(Numeric(12, 8))      #经度
    area_lat  = Column(Numeric(12, 8))      #纬度
    telephone = Column(String)      #固定电话
    remark  = Column(String)   #备注
    creator  = Column(String, default = admin_code)  #创建人
    create_time  = Column(Date, default = datetime.now)  #创建时间
    modifier  = Column(String, default = admin_code)   #修改人
    modify_time  = Column(Date, default = datetime.now)  #修改时间

#初始化hoau_auth数据库连接的session信息
gisSession = initSession('10.108.2.217','3306','hoau-gis','gis','Gis@1234')
