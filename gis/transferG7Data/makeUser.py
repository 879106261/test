# -*- coding: utf-8 -*-
import sys
sys.path.append('./entity')
from entity.authEntity import authSession,Org,User,UserOrg,UserRole
from tools import log, codeGenerator
from openpyxl import load_workbook
import os

class MakeUser(object):
    '''
       为每个平台、直营门店生成默认用户
    '''
    def __init__(self):
        self.__folder__ = '../data'   #数据文件位置
        self.__password__='827e9c07048e7b7b91c76aead083826b'    #密码 hy@88888
        self.__sys_code__='248300776082198528'   #GIS系统的编码
        self.__role_code__='248311166052651008'  #平台、门店操作员角色编码
        self.__role_code_2__='257357293737750528'  #大区偏线管理员角色        

    def query_org_code(self,short_name):
        '''
           根据机构简称查询机构编码
        '''
        org_code = None
        results = authSession.query(Org).filter(Org.short_name==short_name)
        if results.count() ==0:
            log('机构%s不存在'%short_name)
        elif results.count() ==1:
            org_code= results[0].code
        else:
            log('机构%s查询到多条记录'%short_name)            
        return org_code;
        
    def run(self):
        '''
           为每个平台、直营门店生成默认用户
        '''
        #获取excel对象
        filepath= os.path.join(self.__folder__, '默认用户数据.xlsx')
        wb = load_workbook(filepath)
        sheet = wb['机构信息']

        #遍历所有数据
        n = 0
        for row in sheet.rows:
            n+=1
            if n > 1 and (row[0].value !=None):
                short_name = row[0].value  #机构简称
                org_level_name  = row[4].value  #机构类型
                org_code = self.query_org_code(short_name)
              
                #插入t_user表数据
                if org_level_name == '偏线':
                    tmp_name = '%s偏线' % short_name
                else:
                    tmp_name = short_name
                userObj = User(
                    code = codeGenerator() ,  #用户编码
                    name = tmp_name,    #用户名称
                    login_name  = tmp_name,   #登录名
                    password  = self.__password__,  #密码
                    org_code  =org_code    #所属机构编码
                    )
                authSession.add(userObj)
                authSession.commit()                

                #插入t_user_role表数据
                if org_level_name == '平台':
                    org_level = 'PLATFORM'
                elif org_level_name == '偏线':
                    org_level = 'OFFSET_LINE'                    
                else:
                    org_level = None                    
                userOrgObj = UserOrg(
                    user_code = userObj.code,  #用户编码
                    sys_code = self.__sys_code__,    #系统编码
                    org_level  = org_level,   #组织类别
                    org_code  = org_code  #组织编码集合
                    )
                authSession.add(userOrgObj)
                authSession.commit()

                #查询t_user_role表数据
                if org_level_name == '偏线':
                    userRoleObj = UserRole(
                        user_code = userObj.code,  #用户编码
                        role_code = self.__role_code_2__    #角色编码
                        )
                else:    
                    userRoleObj = UserRole(
                        user_code = userObj.code,  #用户编码
                        role_code = self.__role_code__    #角色编码
                        )
                authSession.add(userRoleObj)
                authSession.commit()

                print(short_name,org_level_name,org_code)


if __name__ == '__main__':
    print('开始执行……')
    t = MakeUser()
    t.run()
    print('程序执行结束！')
