# -*- coding: utf-8 -*-
import sys
sys.path.append('./entity')
from entity.authEntity import authSession, Org
from entity.GISEntity import Area,AreaRelease,OrgRelease,gisSession
from tools import log, codeGenerator
from sqlalchemy import func

class Transfer(object):
    '''
       利用数据库，将AreaRelease数据转换为OrgRelease数据
    '''

    def queryAreaRelease(self,short_name):
        '''
         查询是否有简称相同的记录
        '''
        results = gisSession.query(func.count('1')).filter(OrgRelease.short_name==short_name).all()
        gisSession.close()
        return results[0][0]

    def queryArea(self,area_code):
        '''
         area_code查询t_area表，或者详细地址信息
        '''
        results = gisSession.query(Area.detail_add).filter_by(area_code = area_code).first()
        gisSession.close()
        if results == None:
            # 记录AreaFeatureRelease表和Area表不一致的数据
            log('机构%s在Area表中不存在' % (area_code))
        else:
            return results[0]

    def addOrgRelease(self):
        '''
            向OrgRelease数据库插入机构数据
        '''
        # 从Area表查询需要插入OrgRelease表中的数据
        results = gisSession.query(AreaRelease)
        gisSession.close()
        for r in results:            
            area_code = r.area_code
            address = self.queryArea(area_code)
            if address!= None :
                orgrReleaseCount=self.queryAreaRelease(r.org_short_name)
                if orgrReleaseCount ==0:
                    orgObj = OrgRelease(
                        code = r.org_code,#自动生成编码
                        name  = r.org_name,  #公司名称
                        short_name = r.org_short_name,    #公司简称
                        address  = address,      #地址
                        area_lng = r.area_lng,    #经度
                        area_lat  = r.area_lat,     #纬度
                        telephone = r.org_telephone    #固定电话
                    )                    
                    gisSession.add(orgObj)
                    gisSession.commit()
                    print('完成机构%s的转换' % r.org_short_name)
                else:
                    print('已经存在机构%s的数据' % r.org_short_name)                    


if __name__ == '__main__':
    # 注意：OrgRelease的id需要设置自增长，address长度需要设置512
    print('开始执行……')
    t = Transfer()
    t.addOrgRelease()
    print('程序执行结束！')
