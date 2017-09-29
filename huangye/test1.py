import requests
import bs4
import re

def get_html(url):
    try:
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'
        res = requests.get(url, headers=headers)
        return res.text
    except:
        return " Something Wrong！ "

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


def main():
  url = 'http://b2b.huangye88.com/qiye2442999/company_contact.html'
  get_content1(url)

if __name__ == '__main__':
    main()