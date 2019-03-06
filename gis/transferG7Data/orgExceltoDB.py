# -*- coding: utf-8 -*-
import sys
sys.path.append('./entity')
import os
import openpyxl
from openpyxl import load_workbook
from  entity.authEntity import authSession,Org
from tools import log, codeGenerator

class OrgToDB(object):
    """
        将EXCEL文件中的机构信息导入数据库中
    """
    def __init__(self):
        # 地址
        self.__folder__ = '../data'
        self.__code__={} #机构编码与机构名称的对应关系表
        self.__parent_code__={}  #每条记录的机构编码与上级机构名称的对应关系表

    def add(self, name, short_name, numb, parent_name, level, linkman='', mobile_phone='', telephone=''):
        '''
            向数据库中插入机构信息
        '''
        #解析级别数据字典
        if level=='平台':
            tmp_level = 'PLATFORM'
        elif level=='门店':
            tmp_level = 'STORE'
        elif level=='偏线':
            tmp_level = 'OFFSET_LINE'
        else:
            tmp_level = 'TOP_LEVEL'            
            
        orgObj = Org(
            code = codeGenerator(),  #机构编码
            name = name,  #机构名称
            short_name = short_name.strip(),    #机构简称
            numb = numb,  #机构编号
            level = tmp_level,  #机构级别
            parent_code = parent_name,  #上级机构编码,暂时为空
            linkman = linkman, #联系人
            mobile_phone = mobile_phone, #手机号
            telephone = telephone #固定电话
            )
        authSession.add(orgObj)
        authSession.commit()
        print(name, short_name, numb, level, parent_name, linkman, mobile_phone, telephone)

        #将机构名称与机构编码的关系保存
        if name in self.__code__:
            log('机构名称%s已存在' % name)
        else:
            self.__code__[name] = orgObj.code

        #每条记录的机构编码与上级机构名称的对应关系保存
        self.__parent_code__[orgObj.code] = parent_name            
        
        authSession.close()

    def update_parent(self):
        '''
             更新数据库表中的父级机构代码
        '''
        #查询机构数据
        results = authSession.query(Org).all()
        n = 0
        for r in results:
            n+=1           
            #将机构名称与机构编码的关系保存
            if r.short_name in self.__code__:
                log('机构简称%s已存在' % r.short_name)
            else:
                self.__code__[r.short_name] = r.code

            #每条记录的机构编码与上级机构名称的对应关系保存，此时parent_code存放的是上级机构名称
            self.__parent_code__[r.code] = r.parent_code    
        authSession.close()
        
        #在上级机构代码字段中加入新的机构代码
        for key in self.__parent_code__:
            parent_name =self.__parent_code__[key]  #取出父级机构名称
            if parent_name!=None:
                print('key=%s,parent_name=%s'%(key,parent_name))
                if parent_name in self.__code__:
                    parent_code = self.__code__[parent_name]  #取出父级机构代码
                    #更新父级机构代码
                    obj = authSession.query(Org).filter_by(code = key).first()
                    obj.parent_code = parent_code
                    authSession.add(obj)
                    authSession.commit()
                else:
                    log('父级机构%s不存在' % parent_name)
     
        
    def to_db(self,filename):
        '''
             将EXCEL文件中的机构信息导入数据库中
        '''
        #获取excel对象
        filepath= os.path.join(self.__folder__, filename)
        wb = openpyxl.load_workbook(filepath)
        sheet = wb['机构信息']

        #遍历所有数据
        n = 1
        for row in sheet.rows:
            if n > 1 and (row[0].value !=None):
                self.add(
                    short_name = row[0].value, #机构简称
                    numb = row[1].value, #机构编号                    
                    name = row[2].value,  #机构名称
                    parent_name = row[3].value,  #上级机构名称
                    level = row[4].value,  #机构类型
                    linkman = row[5].value, #联系人
                    mobile_phone = row[6].value,  #手机号
                    telephone = row[7].value  #固定电话
                    )
            n = n + 1
        

if __name__ == '__main__':
    todb = OrgToDB()
    #插入机构信息
    #todb.to_db('场站、中转平台.xlsx')
    #todb.to_db('平台机构数据.xlsx')
    #todb.to_db('加盟门店数据.xlsx')
    #todb.to_db('直营门店数据.xlsx')
    #todb.to_db('偏线机构数据.xlsx')
    #todb.to_db('平台补充数据.xlsx')
    #todb.to_db('门店补充数据.xlsx')
    
    #更新机构的父级编码，单独执行
    #todb.update_parent()
    print("转换结束")

