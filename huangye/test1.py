import requests
import bs4
from lxml import etree
import logging
from xlrd import open_workbook
from xlutils.copy import copy
from xlwt import *
import os

def get_html(url):
    try:
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'
        res = requests.get(url, headers=headers)
        return res.text
    except:
        return " Something Wrong！ "

def get_qiye1(url):

    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')

    sum_list = soup.find_all('div', attrs={'class': 'main'})
    for test in sum_list:
        company_list = test.find_all('div', attrs={'class': 'ad_list'})
        for company in company_list:
             company1_list = company.find_all('a')
             for company1 in company1_list:
                 title1 = company1['title']
                 link = company1['href']
                 base_dir = os.getcwd()
                 filename = base_dir + '/企业名录/'+title1
                 if os.path.exists(filename):
                     print('爬取'+title1)
                 else:
                     print('创建'+title1)
                     os.mkdir(filename)
                 get_qiye2(link, filename)


def get_qiye2(url, filename1):
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')

    sum_list = soup.find_all('div', attrs={'class': 'main'})

    for test in sum_list:
        company_list = test.find_all('div', attrs={'class': 'box ad_L'})
        for company in company_list:
             company1_list = company.find_all('ul', attrs={'class': 'clearfix'})
            #  print(company1_list)

             for company1 in company1_list:
                 company2_list = company1.find_all('li')
                 for company2 in company2_list:
                    title2 = company2.a['title']
                    link = company2.a['href']

                    filename = filename1+'/'+title2
                    if os.path.exists(filename):
                        print('爬取'+title2)
                    else:
                        print('创建'+title2)
                        os.mkdir(filename)

                    fanye(link, filename)

def fanye(url, filename2):
    w = Workbook(encoding='utf-8')
    w.add_sheet('xlwt was here')
    w.save(filename2+'/company_list.xls')
    for page in range(1, 500):
       j = (page-1)*20+1
       if page == 1:
           get_content(url, filename2, j)
       else:
           url1= url+'pn'+str(page)
           get_content(url1, filename2, j)


def get_content(url, filename3, j):
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')

    rb = open_workbook(filename3+'/company_list.xls')
    wb = copy(rb)
    ws = wb.get_sheet(0)

    # 找到公司名字，发现她们全部都包含在a标签中
    company4_list = soup.find_all('div', attrs={'class': 'box'})

    print(j)
    for test in company4_list:
        company_list = test.find_all('dl')
        for company in company_list:
            try:
                link = company.h4.a['href']
                content_list = get_content1(link+'company_contact.html')
                title = content_list[0]
                people = content_list[1]
                phone = content_list[2]
                data = get_content2(link+'company_map.html')
                print(title)
                ws.write(j, 0, title)
                ws.write(j, 1, people)
                ws.write(j, 2, phone)
                ws.write(j, 3, data)
                wb.save(filename3+'/company_list.xls')
                j = j+1
            except Exception as e:
                logging.exception(e)



def get_content1(url):

    html = get_html(url)
    selector = etree.HTML(html)

    lable_list = []
    content_list = []
    content1_list = []
    content2_list = []
    company1_list = selector.xpath('//ul[@class="con-txt"]/li/text()')
    company2_list = selector.xpath('//ul[@class="con-txt"]/li/a/text()')

    for test in company1_list:
           content1_list.append(test)
    for test in company2_list:
           content2_list.append(test)
    for test in selector.xpath('//ul[@class="con-txt"]/li/*/text()'):
           lable_list.append(test)

    if(lable_list[1]=='手机：'):
        people = content1_list[0]
        title = content1_list[2]
        phone = content1_list[1]
    else:
        people = content2_list[0]
        phone = content1_list[0]
        title = content1_list[1]
    content_list.append(title)
    content_list.append(people)
    content_list.append(phone)
    return content_list

def get_content2(url):

    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    company1_list = soup.find_all('ul', attrs={'class': 'add-txt'})

    for test in company1_list:
          data1 = test.text
    pydata = data1[5:]
    return pydata

def main():
   base_url= 'http://b2b.huangye88.com/'

   base_dir = os.getcwd()
   sum = base_dir + '/企业名录'
   if os.path.exists(sum):
       print('开始爬取企业名录')
   else:
       os.mkdir(sum)

   get_qiye1(base_url)


if __name__ == '__main__':
    main()

