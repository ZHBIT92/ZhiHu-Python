import requests
import bs4


def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        # r.encoding = r.apparent_encoding
        r.encoding = 'utf-8'
        return r.text
    except:
        return " Something Wrong！ "

def get_content(url):
    '''
    爬取每一类型小说排行榜，
    按顺序写入文件，
    文件内容为 小说名字+小说链接
    将内容保存到列表
    并且返回一个装满url链接的列表
    '''
    url_list = []
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')

    # 看到历史类和完本类的小说与其他小说不在一个div，分开读取
    category_list = soup.find_all('div', attrs={'class': 'index_toplist mright mbottom'})
    # 匹配历史和完本类别的数目
    history_finished_list = soup.find_all('div', attrs={'class': 'index_toplist mbottom'})

    # 用open的w+模式覆盖文件
    with open('novel_list.csv', 'w+') as f:
            f.write("")

    for cate in category_list:
        name = cate.find('div', class_='toptab').span.string
        # 打开文件,open中a+模式表示可读可写，不存在则创建
        with open('novel_list.csv', 'a+') as f:
            f.write("\n小说种类：{} \n".format(name))
        # 通过id来对总排行榜进行定位,
        general_list = cate.find(style='display: block;')
        # 找到全部小说名字，发现她们全部都包含在li标签中
        book_list = general_list.find_all('li')
        # 循环遍历每一个小说的名字以及链接
        for book in book_list:
            link = 'http://www.qu.la/' + book.a['href']
            title = book.a['title']
            # 将所有文章的url地址保存在一个列表变量里
            url_list.append(link)
            # 这里使用a模式,防止清空文件
            with open('novel_list.csv', 'a') as f:
                f.write("小说名: {:<} \t 小说地址: {:<} \n".format(title, link))

    for cate in history_finished_list:
        name = cate.find('div', class_='toptab').span.string
        with open('novel_list.csv', 'a+') as f:
            f.write("\n小说种类：{} \n".format(name))


        general_list = cate.find(style='display: block;') #找到总排行榜
        book_list = general_list.find_all('li')
        for book in book_list:
            link = 'http://www.qu.la/' + book.a['href']
            title = book.a['title']
            url_list.append(link)
            with open('novel_list.csv', 'a') as f:
                f.write("小说名：{:<} \t 小说地址：{:<} \n".format(title, link))
                f.close()
    return url_list

def main():

   base_url= 'http://www.qu.la/paihangbang/'
   url_list = get_content(base_url)

if __name__ == '__main__':
    main()

