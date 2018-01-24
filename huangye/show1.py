import requests
from lxml import etree
from xlrd import open_workbook
from xlutils.copy import copy
from xlwt import *
from random import choice
import time
import datetime
import os

def get_html(url):
    try:
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'
        res = requests.get(url, headers=headers)
        return res.text
    except:
        return " Something Wrong！ "

def fanye(url, filename1):
    '''
    新建一个Excel文件并保存
    '''
    html = get_html(url)
    selector = etree.HTML(html)
    title2 = selector.xpath('//div[@class="head clearfix"]//h1/text()')
    print(title2[0])
    filename = filename1+'/'+title2[0]
    if os.path.exists(filename):
         print('爬取'+title2[0])
    else:
         print('创建'+title2[0])
         os.mkdir(filename)

    w = Workbook(encoding='utf-8')
    w.add_sheet('xlwt was here')
    w.save(filename+'/company_list.xls')

    for page in range(1,120):
       j = (page-1)*37+1
       print(page)
       if page == 1:
           get_content(url, filename, j)
       else:
           url1= url+'/p'+str(page)
           get_content(url1, filename, j)
       time.sleep(5)

def get_content(url, filename3, j):
    html = get_html(url)
    selector = etree.HTML(html)
    '''
    xlrd只能读
    xlwt可以写但会覆盖文件
    使用第三方库xlutils来可以实现追写Excel
    主体思想就是先复制一份Sheet然后再次基础上追加并保存到一份新的Excel文档中去
    '''
    rb = open_workbook(filename3+'/company_list.xls')
    wb = copy(rb)
    ws = wb.get_sheet(0)
    print(j)

    company_list = selector.xpath('//li[@class="clearfix"]//p[@class="shop_unit_contact"]/a[last()]')
    for company in company_list:
        link = company.xpath('.//@href')
        content_list = get_content1(link[0])
        # 判断list是否为空
        if content_list:
            for i in range(len(content_list)):
                ws.write(j, i, content_list[i])
                wb.save(filename3+'/company_list.xls')
        else:
            break
        j = j+1

def get_content1(url):

    html = get_html(url)
    selector = etree.HTML(html)
    content_list = []
    content1_list = selector.xpath('//div[@class="gs-lxwm"]/ul/li/span[@class="lxwm-value"]/text()')
    title_list = selector.xpath('//div[@id="ctl00_GongsiDangan"]/ul/li/span[@class="gs-da-value"]/text()')
    key_list = selector.xpath('//div[@class="gs-lxwm"]/ul/li/span[@class="lxwm-key"]/text()')
    people = []
    title = []
    phone = []
    phone1 = []
    data = []
    if content1_list:
        title = title_list[0]
        for i in range(len(key_list)):
           if(key_list[i]=='联系人：'):
              people = content1_list[i]
           elif(key_list[i]=='联系手机：'):
              phone = content1_list[i]
           elif(key_list[i]=='联系电话：'):
              phone1 = content1_list[i]
           elif(key_list[i]=='公司地址：'):
              data = content1_list[i]
    content_list.append(title)
    content_list.append(people)
    content_list.append(phone)
    content_list.append(phone1)
    content_list.append(data)
    print(content_list)
    return content_list

def main():
   base_url= 'http://www.cnlinfo.net/jianzhujiancai-gongsi/'
   # 单页面
   qiye_url ='http://guangzhou52221863.cn.cnlinfo.net/lianxiwomen/'
   base_dir = os.getcwd()
   sum = base_dir + '/企业名录test'
   if os.path.exists(sum):
       print('开始爬取企业名录')
   else:
       os.mkdir(sum)

   fanye(base_url, sum)
   # get_content1(qiye_url)

if __name__ == '__main__':
    main()

