#!/usr/bin/env python3.4
# encoding: utf-8
"""
Created on 18-1-2

@author: Xu
"""
import requests,re
import codecs   #引入解码器
import random

from bs4 import BeautifulSoup
from openpyxl import Workbook  #从openpyxl引入Workbook
from fake_useragent import UserAgent  #引入userAgent

Excel = Workbook() #调用
fileName = 'zl.xlsx'

excel = Excel.active  #调用运行的工作表
excel.title = ('zj')


#定义爬虫的方法
def spider(job,page,add):
    ua = UserAgent()
    my_headers = {
        'user-agent':ua.random
    }

    name = []     #定义岗位名称
    percent = []  #定义反馈率
    company = []  #定义公司名称
    salary = []   #定义职位月薪
    position = [] #定义工作地点
    page = int(page)+1
    try:
        for i in range(1,page):
            url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl='+ add +'&kw=' + job + '&sm=0&p=' + str(i)
            # data = {
            #     'jl':'上海',
            #     'kw':job,
            #     'p':i
            # }
            data = requests.get(url,headers=my_headers).content

            #设置htmL解析器
            soup = BeautifulSoup(data,'html.parser')
            soup1 = soup.find('div',class_='newlist_list_content')
            content = soup1.find_all('table',class_="newlist")

            for i in content[1:]:
                print i
                na = i.find('td',attrs={'class':'zwmc'}).find('a').get_text().strip().replace('/n/r', '')#岗位名
                perc = i.find('td',attrs={'class':'fk_lv'}).find('span').get_text()  #反馈率
                comp = i.find('td',attrs={'class':'gsmc'}).find('a').get_text()   #公司名
                sala = i.find('td',attrs={'class':'zwyx'}).get_text()  #职位月薪
                positi = i.find('td',attrs={'class':'gzdd'}).get_text()  #工作地点

                print na,perc,comp,sala,positi

                if perc:
                    percent.append(perc)
                else:
                    percent.append('空')

                name.append(na)
                company.append(comp)
                salary.append(sala)
                position.append(positi)
        for (n, p, c, s, p) in zip(name, percent, company, salary, position):
            col_A = 'A%s' % (name.index(n) + 1)
            col_B = 'B%s' % (name.index(n) + 1)
            col_C = 'C%s' % (name.index(n) + 1)
            col_D = 'D%s' % (name.index(n) + 1)
            col_E = 'E%s' % (name.index(n) + 1)
            excel[col_A] = n
            excel[col_B] = p
            excel[col_C] = c
            excel[col_D] = s
            excel[col_E] = p

            # 保存到excel文件
            print('开始保存数据')
            Excel.save(filename=fileName)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    print '◆我是一只小爬虫◆'
    job = raw_input('请输入您想要的到的岗位名称：')
    page = raw_input('请输入您想要得到的页码数量：')
    add = raw_input('请输入您想要哪个城市的招聘信息：')
    spider(job,page,add)
