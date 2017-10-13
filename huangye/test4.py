import requests
from lxml import etree
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

def get_qiye1(url, sum):

    html = get_html(url)
    selector = etree.HTML(html)
    # xpath返回的是一个list
    company_list = selector.xpath('//div[@class="ad_list"]/a')
    for company in company_list:
        title1 = company.xpath('.//@title')
        link = company.xpath('.//@href')
        print(title1[0])
        filename = sum+'/'+title1[0]
        if os.path.exists(filename):
            print('爬取'+title1[0])
        else:
            print('创建'+title1[0])
            os.mkdir(filename)
        get_qiye2(link[0], filename)

def get_qiye2(url, filename1):
    html = get_html(url)
    selector = etree.HTML(html)
    company_list = selector.xpath('//div[@class="box ad_L"]//ul[@class="clearfix"]/li')
    for company in company_list:
        title2 = company.xpath('.//@title')
        link = company.xpath('.//@href')
        filename = filename1+'/'+title2[0]
        if os.path.exists(filename):
             print('爬取'+title2[0])
        else:
             print('创建'+title2[0])
             os.mkdir(filename)
        fanye(link[0], filename)

def fanye(url, filename2):
    '''
    新建一个Excel文件并保存
    '''
    w = Workbook(encoding='utf-8')
    w.add_sheet('xlwt was here')
    w.save(filename2+'/company_list.xls')
    ''' 获取企业总数并设置爬取页数
    html = get_html(url)
    selector = etree.HTML(html)
    page_list = selector.xpath('//div[@class="tit tit2"]//span/em/text()')
    x = int(page_list[0])/30-1000
    print(int(x))
    '''
    for page in range(1, 250):
       j = (page-1)*20+1
       print(page)
       if page == 1:
           get_content(url, filename2, j)
       else:
           url1= url+'pn'+str(page)
           get_content(url1, filename2, j)

def get_content(url, filename3, j):
    html = get_html(url)
    selector = etree.HTML(html)
    company_list = selector.xpath('//div[@class="mach_list2"]//dt/h4/a')
    print(j)
    '''
    xlrd只能读
    xlwt可以写但会覆盖文件
    使用第三方库xlutils来可以实现追写Excel
    主体思想就是先复制一份Sheet然后再次基础上追加并保存到一份新的Excel文档中去
    '''
    rb = open_workbook(filename3+'/company_list.xls')
    wb = copy(rb)
    ws = wb.get_sheet(0)

    for company in company_list:
        link = company.xpath('.//@href')
        content_list = get_content1(link[0]+'company_contact.html')
        data = get_content2(link[0]+'company_map.html')
        # 判断list是否为空
        if content_list:
           title = content_list[0]
           people = content_list[1]
           phone = content_list[2]
           ws.write(j, 0, title)
           ws.write(j, 1, people)
           ws.write(j, 2, phone)
           ws.write(j, 3, data)
           wb.save(filename3+'/company_list.xls')
        else:
           break

        j = j+1

def get_content1(url):

    html = get_html(url)
    selector = etree.HTML(html)
    content_list = []
    content1_list = selector.xpath('//ul[@class="con-txt"]/li/text()')
    lable_list = selector.xpath('//ul[@class="con-txt"]/li/*/text()')
    people = []
    phone = []
    title = []
    if content1_list:
       # 通过a标签中lable标签的值判断需要爬取的数据（有两种样式）
       if lable_list:
           if(lable_list[0]=='联系人：'):
                if(lable_list[1]=='公司名称：'):
                    people = content1_list[0]
                    title = content1_list[1]
                    if(lable_list[2]=='电话：'):
                        phone = content1_list[2]
                elif(lable_list[1]=='手机：'):
                    people = content1_list[0]
                    phone = content1_list[1]
                    if(lable_list[2]=='公司名称：'):
                        title = content1_list[2]
                elif(lable_list[2]=='手机：'):
                    people = lable_list[1]
                    phone = content1_list[0]
                    if(lable_list[3]=='公司名称：'):
                        title = content1_list[1]
                elif(lable_list[2]=='公司名称：'):
                    people = lable_list[1]
                    title = content1_list[0]
                    if(lable_list[3]=='电话：'):
                        phone = content1_list[1]
                    elif(lable_list[3]=='手机：'):
                        phone = content1_list[1]
           elif(lable_list[0]=='公司名称：'):
                title = content1_list[0]
                if(lable_list[1]=='电话：'):
                        phone = content1_list[1]
           elif(lable_list[0]=='手机：'):
                phone = content1_list[0]
                if(lable_list[1]=='公司名称：'):
                        title = content1_list[1]
    content_list.append(title)
    content_list.append(people)
    content_list.append(phone)
    return content_list

def get_content2(url):

    html = get_html(url)
    selector = etree.HTML(html)
    pydata_list=[]
    company1_list = selector.xpath('//ul[@class="add-txt"]/li/text()')
    if company1_list:
        pydata_list.append(company1_list[0])
    return pydata_list

def main():
   base_url= 'http://b2b.huangye88.com/'

   base_dir = os.getcwd()
   sum = base_dir + '/企业名录'
   if os.path.exists(sum):
       print('开始爬取企业名录')
   else:
       os.mkdir(sum)

   get_qiye1(base_url, sum)


if __name__ == '__main__':
    main()

