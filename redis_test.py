import redis
#开发环境
#r =redis.Redis(host="10.108.10.17",port=6379,password="")
#测试环境
#r =redis.Redis(host="10.108.10.46",port=6379,password="Allways_123")
#老王
# r =redis.Redis(host="121.199.13.222",port=6379,password="")
#gis压测环境
r =redis.Redis(host="10.108.2.217",port=6379,password="gis@1234")

#oms订单修改和状态
print(r.geopos("SITE_DELIVERY","259927679009075200"))

# print(r.hgetall("SITE_DELIVERY"))
print("***********************************************************************")
# print(r.hget("oms_order","\xac\xed\x00\x05t\x00\x18cainiao_AL10000000089708"))
# r.delete("oms_order")
# r.save()


#TMS运单修改和状态
print("***********************************************************************")
# print(r.hgetall("CUSTOMER_PICK_UP"))
# print(r.hget("TMS_WAYBILL","TMS_WAYBILL_AL17082300225709_cainiao"))
# r.delete("TMS_WAYBILL")
# r.save()
#print(r.hget("TMS_WAYBILL","TMS_WAYBILL_AP180323000015_cainiao"))

#TMS运单轨迹
print("***********************************************************************")
#print(r.hget("TMS_TRACE","TMS_TRACE_180208000001"))
# print(r.hgetall("TMS_TRACE"))
# #
# r.delete("TMS_TRACE")
# r.save()


