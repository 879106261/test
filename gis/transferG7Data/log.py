# -*- coding: utf-8 -*-

from datetime import datetime

def log(context):
    '''
        写入日志信息
    '''
    filepath= 'log.txt'
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = '{' + time +'}' +context+'\n'
    with open(filepath, 'a', encoding='utf-8') as file:
        file.write(message)
        print(message)
