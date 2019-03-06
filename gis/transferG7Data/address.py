# -*- coding: utf-8 -*-
import sys
sys.path.append('./entity')
from  entity.addressEntity import addressSession, StandardAddr, StandardAddrDetail
from tools import log, codeGenerator
from sqlalchemy import or_
from countryEntity import session,Country

class Address(object):
    '''
       将标准地址编码转入GIS系统
    '''
    def to_addr(self):
        '''
            将4级标准地址码转换到GIS系统
        '''
        #获取4级标准地址库
        country_dict = {}
        results = session.query(Country).filter(Country.level != '5')
        for r in results:
            #将地址级别转换为t_standard_addr表定义的数据字典
            if r.level =='1':
                tmp_level = 'province'
            elif r.level =='2':
                tmp_level = 'city'
            elif r.level =='3':
                tmp_level = 'district'
            elif r.level =='4':
                tmp_level = 'street'
            else:
                tmp_level = ''

            #向t_standard_addr表中添加数据
            obj = StandardAddr(
                code = codeGenerator(),  #标准地址记录编码
                adcode = r.id,   #国内标准地址编码
                name = r.name,      #地址名称
                level  = tmp_level,      #地址级别
                parent_code = r.parent_id      #上级地址编码
                )
            addressSession.add(obj)
            addressSession.commit()
            print(r.id, r.name, r.level, r.parent_id)
        session.close()
  
    def to_addr_detail(self):
        '''
            向t_standard_addr_detail表中添加数据
        '''
        #获取省级标准地址库
        province_dict = {}
        results = session.query(Country).filter_by(level = '1')
        for r in results:
            province_dict[r.id] = r.name

        #获取市级标准地址库
        city_dict = {}
        results = session.query(Country).filter_by(level = '2')
        for r in results:
            city_dict[r.id] = [r.name,r.parent_id]

        #获取县级级标准地址库
        country_dict = {}
        results = session.query(Country).filter_by(level = '3')
        for r in results:
            country_dict[r.id] = [r.name,r.parent_id]

        #获取省、市、县、乡镇级4级标准地址库
        all_dict = {}
        results = session.query(Country).filter(or_(Country.level == '1', Country.level == '2', Country.level == '3', Country.level == '4'))
        for r in results:
            all_dict[r.id] = [r.name, r.level, r.parent_id ]

        #遍历所有的4级地址
        for key in all_dict:
            value_list =  all_dict[key]
            code = key     #地址编码
            name = value_list[0]  #地址名称
            level = value_list[1]   #级别
            parent_id = value_list[2]  #父级编码

            if level =='1':
                  #省级
                  self.add_addr_detail(pcode = code, pname = name)
            elif  level =='2':
                  #市级
                  province_name = province_dict[parent_id]
                  self.add_addr_detail(pcode = parent_id, pname= province_name, ccode = code, cname= name)
            elif level =='3':
                  #县级
                  city = city_dict[parent_id]
                  city_name = city[0]  #市级名称
                  province_code = city[1]  #市级的父级ID，省级ID
                  province_name = province_dict[province_code] #省级名称
                  self.add_addr_detail(pcode = province_code, pname= province_name, ccode = parent_id, cname= city_name, dcode = code, dname= name)
            elif level =='4':
                  #乡镇
                  if  parent_id in country_dict:
                      #乡镇的上级机构是区县
                      country =  country_dict[parent_id]
                      country_code = parent_id  #县级编码
                      country_name = country[0] #县级名称
                      city_code =country[1]  #县级的父级ID，市级ID  
                  else:
                      #乡镇的上级机构是地级市
                      country_code = None
                      country_name = None
                      city_code = parent_id                                  
                  city = city_dict[city_code]  
                  city_name = city[0]  #市级名称
                  province_code = city[1]  #市级的父级ID，省级ID
                  province_name = province_dict[province_code] #省级名称                  
                  self.add_addr_detail(pcode = province_code, pname= province_name, ccode = city_code, cname= city_name, dcode = country_code, dname= country_name, scode = code, sname= name)
            else:
                log('%s级别是%s' %(name,level))

    def query_standard_addr(self,pcode,ccode=None,dcode=None,scode=None):
        '''
                标准地址记录编码取最低级的地址编码
        '''
        standard_addr_code=None
        if scode!=None:
            results = addressSession.query(StandardAddr).filter(StandardAddr.adcode == scode)
        elif dcode!=None:
            results = addressSession.query(StandardAddr).filter(StandardAddr.adcode == dcode)
        elif ccode!=None:
            results = addressSession.query(StandardAddr).filter(StandardAddr.adcode == ccode)
        else:
            results = addressSession.query(StandardAddr).filter(StandardAddr.adcode == pcode)
        if results.count() ==0:
            log('无法找到地址编码记录,%s,%s,%s,%s' %(pcode,ccode,dcode,scode))
        elif results.count() ==1:
            standard_addr_code = results[0].code
        else:
            log('找到多个地址编码记录,%s,%s,%s,%s' %(pcode,ccode,dcode,scode))            
        return standard_addr_code

    def  add_addr_detail(self, pcode,pname,ccode=None,cname=None,dcode=None,dname=None,scode=None,sname=None):
        '''
            向t_standard_addr_detail表中添加数据
        '''
        #拼接全部地址字符串
        cname_str = ''
        if  cname!=None:
            cname_str = cname
        dname_str = ''
        if  dname!=None:
            dname_str = dname
        sname_str = '' 
        if  sname!=None:
            sname_str = sname
        standard_addr_detail = '%s%s%s%s' %(pname,cname_str,dname_str,sname_str)
        print('省=%s,市=%s,区县=%s,乡镇=%s' % (pname,cname_str,dname_str,sname_str))
        

        standard_addr_code=self.query_standard_addr(pcode,ccode,dcode,scode)
            
        #插入数据            
        obj = StandardAddrDetail(
            standard_addr_code = standard_addr_code,  #标准地址记录编码
            standard_addr_detail = standard_addr_detail,   #包含上级地址的地址信息
            pcode = pcode,      #省级地址编码
            pname  = pname,      #省级地址名称
            ccode = ccode,      #市级地址编码
            cname  = cname,      #市级地址名称
            dcode = dcode,      #县级地址编码
            dname  = dname,      #县级地址名称
            scode = scode,      #乡镇级地址编码
            sname  = sname      #乡镇级地址名称
            )
        addressSession.add(obj)
        addressSession.commit()


if __name__ == '__main__':
    print('开始执行……')
    t= Address()
    #t.to_addr()
    t.to_addr_detail()
    print('程序执行结束！')
