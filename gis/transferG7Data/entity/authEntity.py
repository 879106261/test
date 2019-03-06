# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Date, Numeric,Text
from driverForMysql import Base, initSession,admin_code
from datetime import datetime

class  Org(Base):
    '''
       机构
    '''
    __tablename__ = 't_org'
    id = Column(Integer,primary_key=True, nullable=False)      
    code = Column(String, nullable=False)     #机构编码
    name = Column(String, nullable=False)    #机构名称
    short_name = Column(String, nullable=False)    #机构简称
    numb = Column(String, nullable=False)    #机构编号
    level = Column(String, nullable=False)    #机构级别
    type  = Column(String)   #机构类型
    parent_code  = Column(String, nullable=False)  #上级机构code
    linkman = Column(String)  #联系人
    mobile_phone  = Column(String)     #手机号
    telephone  = Column(String)     #固定电话    
    status  = Column(String, nullable=False,default='VALID')    #机构状态
    remark  = Column(String)   #备注
    creator  = Column(String, default = admin_code, nullable=False)  #创建人
    create_time  = Column(Date, default = datetime.now, nullable=False)  #创建时间
    modifier  = Column(String, default = admin_code, nullable=False)   #修改人
    modify_time  = Column(Date, default = datetime.now, nullable=False)  #修改时间

class  User(Base):
    '''
       用户
    '''
    __tablename__ = 't_user'
    id = Column(Integer,primary_key=True, nullable=False)      
    code = Column(String, nullable=False)     #用户编码
    name = Column(String, nullable=False)    #用户名称
    mobile = Column(String)    #手机
    telephone = Column(String)    #电话
    email = Column(String)    #电子邮件
    login_name  = Column(String, nullable=False)   #登录名
    password  = Column(String, nullable=False)  #密码
    status  = Column(String, nullable=False,default='ENABLED')    #状态
    org_code  = Column(String)     #所属机构编码
    remark  = Column(String)   #备注
    creator  = Column(String, default = admin_code, nullable=False)  #创建人
    create_time  = Column(Date, default = datetime.now, nullable=False)  #创建时间
    modifier  = Column(String, default = admin_code, nullable=False)   #修改人
    modify_time  = Column(Date, default = datetime.now, nullable=False)  #修改时间

class  UserRole(Base):
    '''
       用户的功能权限表
    '''
    __tablename__ = 't_user_role'
    id = Column(Integer,primary_key=True, nullable=False)      
    user_code = Column(String, nullable=False)     #用户编码
    role_code = Column(String, nullable=False)     #角色编码
    remark  = Column(String)   #备注
    creator  = Column(String, default = admin_code, nullable=False)  #创建人
    create_time  = Column(Date, default = datetime.now, nullable=False)  #创建时间
    modifier  = Column(String, default = admin_code, nullable=False)   #修改人
    modify_time  = Column(Date, default = datetime.now, nullable=False)  #修改时间

class  UserOrg(Base):
    '''
       用户的数据权限表
    '''
    __tablename__ = 't_user_org'
    id = Column(Integer,primary_key=True, nullable=False)      
    user_code = Column(String, nullable=False)     #用户编码
    sys_code = Column(String, nullable=False)      #系统编码
    org_level = Column(String, nullable=False)      #组织类别
    org_code = Column(String, nullable=False)      #组织编码集合
    remark  = Column(String)   #备注
    creator  = Column(String, default = admin_code, nullable=False)  #创建人
    create_time  = Column(Date, default = datetime.now, nullable=False)  #创建时间
    modifier  = Column(String, default = admin_code, nullable=False)   #修改人
    modify_time  = Column(Date, default = datetime.now, nullable=False)  #修改时间
    
#初始化hoau_auth数据库连接的session信息
authSession = initSession('127.0.0.1','3306','hoau_auth','root','password')

