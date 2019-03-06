#coding=utf-8

import sys

class data():
    def __init__(self):
        channelNo = ""
        waybill = ""

    def creatData(n):
        fsave = open('redisProtocol', 'a+')

        db = "TMS_TRACE"
        key = "TMS_TRACE_18890100" + str(n)
        value ='{"channelNo":"he201808300062","requestId":"180901000027","waybillStatus":61,"logisticCompanyID":"123456","flowLogs":[{"waybillNo":"180901000027","waybillStatus":61,"handleType":"61","handleDeptId":10184,"handleDeptName":"合肥转运中心","handleDeptAttribute":1,"handleTime":null,"handleTimeFormat":"1535793925000","remark":"感谢您使用安吉快运服务, 期待下次继续为您服务","city":"合肥市","contacter":null,"contacterPhone":null,"nextCity":null,"nextNodeCode":null,"nextNodeName":null},{"waybillNo":"180901000027","waybillStatus":31,"handleType":"31","handleDeptId":10184,"handleDeptName":"合肥转运中心","handleDeptAttribute":1,"handleTime":null,"handleTimeFormat":"1535793870000","remark":"【合肥市】合肥转运中心已发出","city":"合肥市","contacter":"骆忠院","contacterPhone":"13564454140","nextCity":null,"nextNodeCode":null,"nextNodeName":null},{"waybillNo":"180901000027","waybillStatus":23,"handleType":"23","handleDeptId":10184,"handleDeptName":"合肥转运中心","handleDeptAttribute":1,"handleTime":null,"handleTimeFormat":"1535793367000","remark":"【合肥市】快递已到达合肥转运中心","city":"合肥市","contacter":null,"contacterPhone":null,"nextCity":null,"nextNodeCode":null,"nextNodeName":null},{"waybillNo":"180901000027","waybillStatus":22,"handleType":"22","handleDeptId":10005,"handleDeptName":"上海浦西转运中心","handleDeptAttribute":1,"handleTime":null,"handleTimeFormat":"1535793302000","remark":"【上海城区】上海浦西转运中心已发出，准备送往合肥转运中心","city":"上海城区","contacter":null,"contacterPhone":null,"nextCity":"合肥市","nextNodeCode":"T0551","nextNodeName":"合肥转运中心"},{"waybillNo":"180901000027","waybillStatus":23,"handleType":"23","handleDeptId":10005,"handleDeptName":"上海浦西转运中心","handleDeptAttribute":1,"handleTime":null,"handleTimeFormat":"1535793174000","remark":"【上海城区】快递已到达上海浦西转运中心","city":"上海城区","contacter":null,"contacterPhone":null,"nextCity":null,"nextNodeCode":null,"nextNodeName":null},{"waybillNo":"180901000027","waybillStatus":22,"handleType":"22","handleDeptId":10240,"handleDeptName":"青浦华新移动营业部","handleDeptAttribute":2,"handleTime":null,"handleTimeFormat":"1535793113000","remark":"【上海城区】青浦华新移动营业部已发出，准备送往上海浦西转运中心","city":"上海城区","contacter":null,"contacterPhone":null,"nextCity":"上海城区","nextNodeCode":"T021","nextNodeName":"上海浦西转运中心"},{"waybillNo":"180901000027","waybillStatus":5,"handleType":"5","handleDeptId":10240,"handleDeptName":"青浦华新移动营业部","handleDeptAttribute":2,"handleTime":null,"handleTimeFormat":"1535793007000","remark":"【上海城区】安吉快运青浦华新移动营业部已揽收","city":"上海城区","contacter":null,"contacterPhone":null,"nextCity":null,"nextNodeCode":null,"nextNodeName":null}],"waybillNo":"180901000027"}'
        fsave.write('*4' + '\r\n')
        fsave.write('$4' + '\r\n')
        fsave.write('hset' + '\r\n')
        fsave.write('$%d' % len(db) + '\r\n')
        fsave.write(db + '\r\n')

        fsave.write('$6' + '\r\n')
        fsave.write(key + '\r\n')
        fsave.write('$%d' % len(key) + '\r\n')
        fsave.write(value + '\r\n')
        fsave.write('\r\n')
        fsave.close()




if __name__ =="__main__":
    for n in range(6000):
        print(n)
        x = data.creatData(n)





