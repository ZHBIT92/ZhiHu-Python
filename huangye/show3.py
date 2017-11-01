# coding:utf-8
import requests
from lxml import etree
from xlrd import open_workbook
from xlutils.copy import copy
from xlwt import *
from random import choice
import time
import os
import re
from selenium import webdriver
from multiprocessing import Pool

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

def get_qiye(url, filename):
    # 342汽摩 363广告传媒 372建材
    '''
    diqu_url = ['342.htm', '363.htm', '372.htm']
    for url1 in diqu_url:
        link = url+'/search/'+url1
        print(link)
        fanye(link, filename)
        time.sleep(2)
    '''
    # 11739  商务
    diqu_url1 = ['11739.htm']
    for url1 in diqu_url1:
        link = url+'/search/'+url1
        print(link)
        fanye1(link, filename)
        time.sleep(2)

def fanye(url, filename1):
    html = get_html(url)
    selector = etree.HTML(html)

    # 爬取过快时通过selenium模拟浏览器点击事件继续爬取
    onclick_list = selector.xpath('//a/text()')
    for onclick1 in onclick_list:
        if onclick1 == '点击继续':
            onclick(url)
            html1 = get_html(url)
            selector = etree.HTML(html1)
            print('翻页点击成功')

    # 新建公司类型文件并保存
    title = selector.xpath('//div[@class="navleft"]/a[last()]/text()')
    print(title[0])
    filename = filename1+'/'+title[0]
    if os.path.exists(filename):
        print('爬取'+title[0])
    else:
        print('创建'+title[0])
        os.mkdir(filename)
    w = Workbook(encoding='utf-8')
    w.add_sheet('xlwt was here')
    w.save(filename+'/company_list.xls')

    # 获得最大页数
    fanye_list = selector.xpath('//div[@class="pages"]/a[last()]/@href')
    if fanye_list:
        maxpage = re.search(r'\d+\-\d+', str(fanye_list)).group(0)
        maxpage1 = maxpage[5:]
        print(maxpage1)
        for page in range(1,int(maxpage1)+1):
           j = (page-1)*100+1
           print(page)
           if page == 1:
               time.sleep(1)
               get_content(url, filename, j)
           else:
               time.sleep(1)
               next_url = url[:-4]+'-'+str(page)+'.htm'
               get_content(next_url, filename, j)
           # 格式化成2016-03-20 11:45:39形式
           print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    else:
        j = 1
        time.sleep(1)
        get_content(url, filename, j)
    time.sleep(1)

def fanye1(url, filename1):
    html = get_html(url)
    selector = etree.HTML(html)

    # 爬取过快时通过selenium模拟浏览器点击事件继续爬取
    onclick_list = selector.xpath('//a/text()')
    for onclick1 in onclick_list:
        if onclick1 == '点击继续':
            onclick(url)
            html1 = get_html(url)
            selector = etree.HTML(html1)
            print('翻页点击成功')

    # 新建公司类型文件并保存
    title = selector.xpath('//div[@class="navleft"]/a[last()]/text()')
    print(title[0])
    filename = filename1+'/'+title[0]
    if os.path.exists(filename):
        print('爬取'+title[0])
    else:
        print('创建'+title[0])
        os.mkdir(filename)
    w = Workbook(encoding='utf-8')
    w.add_sheet('xlwt was here')
    w.save(filename+'/company_list.xls')

    # 获得最大页数
    fanye_list = selector.xpath('//div[@class="pages"]/a[last()]/@href')
    if fanye_list:
        maxpage = re.search(r'\d+\-\d+', str(fanye_list)).group(0)
        maxpage1 = maxpage[6:]
        print(maxpage1)
        for page in range(1, int(maxpage1)+1):
           j = (page-1)*100+1
           print(page)
           if page == 1:
               time.sleep(1)
               get_content(url, filename, j)
           else:
               time.sleep(1)
               next_url = url[:-4]+'-'+str(page)+'.htm'
               get_content(next_url, filename, j)
           # 格式化成2016-03-20 11:45:39形式
           print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    else:
        j = 1
        time.sleep(1)
        get_content(url, filename, j)
    time.sleep(1)

def get_content(url, filename3, j):
    rb = open_workbook(filename3+'/company_list.xls')
    wb = copy(rb)
    ws = wb.get_sheet(0)
    '''
    xlrd只能读
    xlwt可以写但会覆盖文件
    使用第三方库xlutils来可以实现追写Excel
    主体思想就是先复制一份Sheet然后再次基础上追加并保存到一份新的Excel文档中去
    '''
    time.sleep(1)
    html = get_html(url)
    selector = etree.HTML(html)
    print(j)
    '''
      爬取过快时通过selenium模拟浏览器点击事件继续爬取
    '''
    onclick_list = selector.xpath('//a/text()')
    for onclick1 in onclick_list:
        if onclick1=='点击继续':
            onclick(url)
            html1 = get_html(url)
            selector = etree.HTML(html1)
            print('获取地址点击')
    company1_list = selector.xpath('//div[@class="box"]/div[@class="boxcontent"]/ul[@class="companylist"]/li//div[@class="f_l"]/h4/a')
    for company in company1_list:
        link = company.xpath('@href')
        title = company.xpath('@title')
        href = 'http:'+link[0]+'#contact'

        content1_list = get_content1(href)
        # 判断list是否为空
        if content1_list:
            ws.write(j, 0, title[0])
            for i in range(len(content1_list)):
                ws.write(j, i+1, content1_list[i])
        else:
            break
        wb.save(filename3+'/company_list.xls')
        j = j+1

def get_content1(url):
    time.sleep(1)
    html = get_html(url)
    selector = etree.HTML(html)
    '''
      爬取过快时通过selenium模拟浏览器点击事件继续爬取
    '''
    onclick_list = selector.xpath('//a/text()')
    for onclick1 in onclick_list:
        if onclick1=='点击继续':
             onclick(url)
             html1 = get_html(url)
             selector = etree.HTML(html1)
             print('获取详细信息点击')
    onclick1_list = selector.xpath('//dl[@class="codl"]//dd/a')
    content1_list = selector.xpath('//div[@id="contact"]//dl[@class="codl"]/dd/text()')
    people = []
    phone = []
    phone1 = []
    data = []
    content_list = []
    if onclick1_list:
        a = onclick1_list[0]
        onclick1 = a.get('onclick')
        phone_list = re.search(r'phone/[0-9]*', str(onclick1))
        if phone_list:
           phone1_list = phone_list.group()[6:]
           phone = phone1_list[1::2]

    if content1_list:
        data = content1_list[0]
        phone1 = content1_list[1]
        people = content1_list[2]
    content_list.append(people)
    content_list.append(phone)
    content_list.append(phone1[5:])
    content_list.append(data[5:])
    return content_list

def onclick(url):
    driver = webdriver.PhantomJS()
    driver.get(url)
    driver.find_element_by_xpath('//a').click()
    driver.quit()
    time.sleep(1)
    print('点击成功')

def main():
   # 全部
   sum_url ='http://b2b.11467.com/'
   # 地区
   diqu_url = 'http://www.11467.com/shenyang/'
   #   辽宁 黑龙江 贵州
   diqu_url1 =['shenyang', 'dalian', 'anshan', 'dandong', 'jinzhou', 'yingkou', 'tieling', 'huludao', 'benxi',  'chaoyang' ,'fushun', 'panjin', 'liaoyang', 'fuxin',
               'jiamusi', 'jixi', 'heihe',  'yichunshi', 'qitaihe', 'daxinganling', 'haerbin', 'qiqihaer', 'mudanjiang', 'daqing', 'suihua', 'hegang', 'shuangyashang',
               'guiyang', 'zunyi', 'qiandongnan', 'liupanshui', 'qiannan', 'bijie', 'anshun',  
               #差两个
               ]
   diqu_url11 =['tongren', 'qianxinan']
   #  湖南
   hunan_url =['changsha', 'zhuzhou', 'yueyang', 'changde', 'hengyang', 'shaoyang',
               'xiangtan', 'chenzhou', 'huaihua',  'yiyang', 'yongzhou', 'loudi', 'xianxi', 'zhangjiajie'
               ]
   # 四川
   sichuang_url =['chengdu', 'mianyang', 'deyang', 'yibin', 'nanchong', 'zigong','neijiang',
                  'luzhou', 'leshan',  'dazhou', 'guangyuan', 'panzhihua', 'meishan', 'liangshan',
                  'guangan', 'ziyang', 'suining', 'yaan', 'bazhong', 'aba', 'ganzi'
                  ]
   diqu_url = diqu_url11
   # 地区类型
   base_url= 'http://www.11467.com/guangzhou/search/340.htm'
   # 单页面
   qiye_url ='http://guangzhou52221863.cn.cnlinfo.net/lianxiwomen/'
   base_dir = os.getcwd()
   sum = base_dir + '/湖南四川企业名录'
   #sum = base_dir + '/贵州企业名录'
   if os.path.exists(sum):
       print('开始爬取湖南四川企业名录')
   else:
       os.mkdir(sum)

   for i in range(len(diqu_url)):
       diqu_url2 = 'http://www.11467.com/'+diqu_url[i]
       sum1 = sum+'/'+diqu_url[i]
       if os.path.exists(sum1):
          print('开始爬取'+diqu_url[i])
       else:
          os.mkdir(sum1)
       get_qiye(diqu_url2, sum1)

   #get_qiye1(base_url, sum)
   # get_qiye2(diqu_url, sum)
   # fanye(base_url, sum)
   # get_content1(qiye_url)
   # qiye1_url ='http://www.11467.com/guangzhou/co/120676.htm#contact'
   # get_content1(qiye1_url)
   '''
   p = Pool(2)
   for i in len(diqu_url1):
       diqu_url2 = 'http://www.11467.com/'+diqu_url1[i]
       print(diqu_url2)
       p.apply_async(get_qiye2, args=(diqu_url2,sum))
   p.close()
   p.join()
   '''
if __name__ == '__main__':
    main()

