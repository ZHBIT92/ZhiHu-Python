import requests
import bs4
import logging

def get_html(url):
    try:
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'
        res = requests.get(url, headers=headers)
        return res.text
    except:
        return " Something Wrong！ "

def get_content(url):

    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')

    # 找到公司名字，发现她们全部都包含在a标签中
    company4_list = soup.find_all('div', attrs={'class': 'box'})

    for test in company4_list:
          # name = test.find('div', class_='tit tit2').h3.string
          # 打开文件,open中a+模式表示可读可写，不存在则创建
          #with open('company_list.csv', 'a+') as f:
          #    f.write("\n公司种类：{} \n".format(name))

          company_list = test.find_all('dl')

          for company in company_list:
              try:
                title = company.a['title']
                link = company.h4.a['href']
                txt = company.find('dd', class_='txt').text

                print("公司名：{}\t{}\n{}\n\n ".format(title, link, txt))
                # 这里使用a模式,防止清空文件
                with open('company_list.csv', 'a') as f:
                    f.write("公司: {:<} \t 公司url: {:<} \n 公司简介: {:<} \n ".format(title, link, txt))
              except Exception as e:
                   logging.exception(e)

def main():
   with open('company_list.csv', 'w+') as f:
            f.write("")
   i= 1
   for page in range(1, 500):
       if page == 1:
           base_url= 'http://b2b.huangye88.com/guangdong/wenduyibiao31'
           get_content(base_url)
           i = i+1
       else:
           base_url= 'http://b2b.huangye88.com/guangdong/wenduyibiao31/pn'+str(page)+'/'
           get_content(base_url)
           i = i+1
   print(i)

if __name__ == '__main__':
    main()

