import requests
import bs4
import logging
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
                    print("公司名：{}\t{}\n ".format(title2, link))

                    filename = filename1+'/'+title2
                    if os.path.exists(filename):
                        print('爬取'+title2)
                    else:
                        print('创建'+title2)
                        os.mkdir(filename)

                    fanye(link, filename)

def fanye(url, filename2):

    with open(filename2+'/company_list.csv', 'w+') as f:
                    f.write("公司名称 {:<} \t 联系人 {:<} \t 电话 {:<} \t 地址 {:<} \t\n ")

    for page in range(1, 10):
       if page == 1:
           get_content(url, filename2)
       else:
           url= url+'pn'+str(page)
           get_content(url, filename2)

def get_content(url, filename3):

    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')

    # 找到公司名字，发现她们全部都包含在a标签中
    company4_list = soup.find_all('div', attrs={'class': 'box'})
    for test in company4_list:
          company_list = test.find_all('dl')
          for company in company_list:
              try:
                link = company.h4.a['href']
                content_list = get_content1(link+'company_contact.html')
                people = content_list[0]
                phone = content_list[1]
                title = content_list[2]
                data = get_content2(link+'company_map.html')

                print("\t\t\t\t\n ".format(title, people, phone, data))
                # 这里使用a模式,防止清空文件
                with open(filename3+'/company_list.csv', 'a') as f:
                    f.write("\t\t\t\t\n ".format(title, people, phone, data))
              except Exception as e:
                   logging.exception(e)


def get_content1(url):

    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    content_list = []
    txt = []
    company1_list = soup.find_all('div', attrs={'class': 'r-content'})
    for test in company1_list:
          company11_list = test.find_all('li')
          for company in company11_list:
                txt.append(company.text)
    people = txt[0]
    phone = txt[1]
    cy = txt[2]
    content_list.append(people[4:])
    content_list.append(phone[3:])
    content_list.append(cy[5:])
    return content_list

def get_content2(url):

    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')

    company1_list = soup.find_all('ul', attrs={'class': 'add-txt'})

    for test in company1_list:
          data1 = test.text
    pydata = data1[5:]
    print(pydata)
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

