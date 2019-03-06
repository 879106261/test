import execjs

def get_des_psswd(data, key):
    jsstr = get_js()
    ctx = execjs.compile(jsstr) #加载JS文件
    return (ctx.call('strEnc', data, key))  #调用js方法  第一个参数是JS的方法名，后面的data和key是js方法的参数



def get_js():
    f = open("./../lib/des.js", 'r', encoding='utf-8') # 打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr+line
        line = f.readline()
    return htmlstr


if __name__ == '__main__':
    print(get_des_psswd('123456', 'RUY2OTdCRUFFRTg0OUQ0Q0E0ODNDRDMxN0YzOEEzREQudG9tY2F0OTQ='))