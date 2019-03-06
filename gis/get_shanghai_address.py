#-*- coding:utf-8 -*-
"""
created on 2019年2月24日
@author: 周迎春

"""
import  requests
from bs4 import BeautifulSoup



class GetAdressInfo(object):
    def __init__(self,url):
        self.url = url
        self.pagenum = 4000
        self.urls = self.getUrls(self.pagenum)
        self.items = self.spider(self.urls)
        self.pipLines(self.items)

    def getUrls(self,pagenum):
        urls = []
        urls.append(self.url)
        pns = [str(i) for i in range(2,pagenum)]
        for pn in pns:
            url = self.url + "/" + pn
            urls.append(url)
        return urls

    def spider(self,urls):
        adress = []
        for url in urls:
            html_content = self.getResponseContent(url)
            soup = BeautifulSoup(html_content, 'lxml')
            # tagsli = soup.select('.sheng_weizhi_con  ul')
            tagsli = soup.find_all('ul',attrs = {'class': 'sheng_weizhi_lb'})
            for tag in tagsli:
                company_adress = tag.find_all('li')[1].get_text().strip()
                company_adress1 = company_adress.split("：\r\n\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t")
                if len(company_adress1) == 2:
                    print(company_adress1)
                    self.pipLines(company_adress1[1])
                else:
                    pass

        return adress

    def pipLines(self,items):
        fileName = "上海地址.txt".encode("utf-8")
        with open(fileName, 'a', encoding='utf-8') as file:
            file.write(items + '\n')

    def getResponseContent(self,url):
        """
        返回页面返回值
        :param url:
        :return:
        """
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.33 Safari/537.36'
        }
        try:
            response = requests.get(url=url)
        except:
            print("返回url:%s 数据失败"%url)
        else:
            print("返回url:%s 数据成功"%url)
            response.encoding = 'utf-8'
            return response.text




if __name__ == "__main__":
    url = "http://book.youboy.com/sh"
    GTI =  GetAdressInfo(url)
