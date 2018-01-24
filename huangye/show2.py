import requests
from lxml import etree
from xlrd import open_workbook
from xlutils.copy import copy
from xlwt import *
from random import choice
import time
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

def get_html(url):
    try:
        headers = {}
        headers['User-Agent'] = choice(USER_AGENTS)
        res = requests.get(url, headers=headers)
        return res.text
    except:
        return " Something Wrong！ "

def get_qiye2(url, filename1):
    html = get_html(url)
    selector = etree.HTML(html)
    company_list = selector.xpath('//div[@class="box  huangyecity t5"][last()]//dt/a')
    for company in company_list:
        title2 = company.xpath('.//text()')
        print(title2[0])
        link = company.xpath('.//@href')
        filename = filename1+'/'+title2[0]
        if os.path.exists(filename):
             print('爬取'+title2[0])
        else:
             print('创建'+title2[0])
             os.mkdir(filename)
        fanye(link[0], filename)

def fanye(url, filename1):
    '''
    新建一个Excel文件并保存
    '''
    filename = filename1
    w = Workbook(encoding='utf-8')
    w.add_sheet('xlwt was here')
    w.save(filename+'/company_list.xls')
    for page in range(1,19):
       j = (page-1)*100+1
       print(page)
       if page == 1:
           time.sleep(1)
           get_content(url, filename, j)
       else:
           time.sleep(1)
           url1 = url+'-'+str(page)
           try:
              get_content(url1, filename, j)
           except:
              continue

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
    company1_list = selector.xpath('//div[@class="f_l"]/h4/a')
    if company1_list:
        for company in company1_list:
               link = company.xpath('.//@href')
               href = link[0]+'#contact'
               content1_list = get_content1(href)
               # 判断list是否为空
               if content1_list:
                 print(content1_list)
                 for i in range(len(content1_list)):
                     ws.write(j, i, content1_list[i])
                     wb.save(filename3+'/company_list.xls')
               else:
                 break
        j = j+1

def get_content1(url):
    driver = webdriver.PhantomJS()
    driver.get(url)  
    html = driver.page_source#获取网页的html数据
    left_hold = driver.find_element_by_xpath('/div[@id="contact"]//dl[@class="codl"]/dd/a')
    if left_hold:
        ActionChains(driver).click_and_hold(left_hold).perform()
        html1=driver.page_source#获取网页的html数据
        selector = etree.HTML(html1)
    else:
        selector = etree.HTML(html)

    content_list = []
    content1_list = selector.xpath('//div[@id="contact"]//dl[@class="codl"]/dd/text()')
    title_list = selector.xpath('//div[@class="navleft"]/a[last()]/text()')
    title = title_list[0]
    data = content1_list[0]
    phone1 = content1_list[1]
    people = content1_list[2]
    phone = content1_list[3]
    mail = content1_list[4]
    content_list.append(title)
    if people:
       content_list.append(people)
    else:
       content_list.append(people)
    if phone:
       content_list.append(phone[5:])
    else:
       content_list.append(phone)
    if phone1:
       content_list.append(phone1[5:])
    else:
       content_list.append(phone1)
    if mail:
       content_list.append(mail[5:])
    else:
       content_list.append(mail)
    content_list.append(data[5:])
    return content_list

def main():
   # 全部
   sum_url ='http://b2b.11467.com/'
   # 地区
   diqu_url = 'http://www.11467.com/guangzhou/'
   # 地区类型
   base_url= 'http://www.11467.com/guangzhou/search/340.htm'
   # 单页面
   qiye_url ='http://guangzhou52221863.cn.cnlinfo.net/lianxiwomen/'
   base_dir = os.getcwd()
   sum = base_dir + '/企业名录test1'
   if os.path.exists(sum):
       print('开始爬取企业名录')
   else:
       os.mkdir(sum)
   #get_qiye1(base_url, sum)
   #get_qiye2(diqu_url, sum)
   fanye(base_url, sum)
   # get_content1(qiye_url)

if __name__ == '__main__':
    main()

