import requests
import time
from multiprocessing import Pool

def getProxy():
    Proxy = []
    for row in range(10000):
        proxy = {"http" + str(row)}
        Proxy.append(proxy)
    return Proxy

def test(proxy):
    print('baidu')
    time.sleep(1)
    try:
        response = requests.get('http://www.baidu.com', proxies=proxy, timeout=2)
        if response:
            return proxy
    except:
        pass

def test2(proxy):
    print('tengxun')
    time.sleep(1)
    try:
        response = requests.get('http://www.tengxun.com', proxies=proxy, timeout=2)
        if response:
            return proxy
    except:
        pass


if __name__=='__main__':
    proxy=getProxy()
    # IPPool1=[]
    # time1=time.time()
    # for item in proxy:
    #     IPPool1.append(test(item))
    # time2=time.time()
    # print('singleprocess needs '+str(time2-time1)+' s')
    pool=Pool()
    IPPool2=[]
    temp=[]
    time3=time.time()
    for item in proxy:
        temp.append(pool.apply_async(test,args=(item,)))
    pool.close()
    pool.join()
    for item in temp:
        IPPool2.append(item.get())
    time4=time.time()
    print('multiprocess needs '+str(time4-time3)+' s')