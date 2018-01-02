#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 18-1-2

@author: Xu
"""

import requests,re

#引入解码器
import codecs
from bs4 import BeautifulSoup

#从OpenPyXl引入Workbook这个类
from openpyxl import Workbook

#调用
Excel = Workbook()
fileName = '51job.xlsx'

#调用得到正在运行的工作表
excel = Excel.active

#工作表的名字
excel.title = '51job'

#定义爬虫的方法
def spider(job,page):

    my_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.3397.16 Safari/537.36'
    }
    workName = []
    company = []
    address = []
    pay = []
    print page,type(page)
    page = int(page)+1


    try:
        for i in range(1,page):
            url = 'http://search.51job.com/list/020000,000000,0000,00,9,99,'+job+',2,' + str(i) + '.html'
            #获取url地址内容，伪造请求头

            data = requests.get(url,headers=my_headers).content
            print('得到网页html数据')

            #设置html解析器
            soup = BeautifulSoup(data,'html.parser')
            soup1 = soup.find('div',class_='dw_table')
            content = soup1.find_all('div','el')

            for i in content[1:]:
                # print(i)
                workna = i.find('p', attrs={'class': 't1'})
                work_name = workna.find('span').get_text().strip().replace('/n/r', '')  # 职位名字
                compa = i.find('span', attrs={'class': 't2'}).get_text()  # 公司名
                addre = i.find('span', attrs={'class': 't3'}).get_text()  # 工作地点
                payy = i.find('span', attrs={'class': 't4'}).get_text()  # 薪资
                print(work_name, compa, addre, payy)

                if payy:
                    pay.append(payy)
                else:
                    pay.append('面议')

                workName.append(work_name)
                company.append(compa)
                address.append(addre)

        for (w,c,a,p) in zip(workName,company,address,pay):
            col_A = 'A%s'%(workName.index(w) + 1)
            col_B = 'B%s'%(workName.index(w) + 1)
            col_C = 'C%s'%(workName.index(w) + 1)
            col_D = 'D%s'%(workName.index(w) + 1)
            excel[col_A] = w
            excel[col_B] = c
            excel[col_C] = a
            excel[col_D] = p
            #保存到excel文件
            print('开始保存数据')
            Excel.save(filename=fileName)
    except Exception as e:
        print(e)
if __name__ == '__main__':
    job = raw_input('请输入你要爬取的岗位名称：')
    page = raw_input('请输入你要爬取的页码数量：')
    spider(job,page)
