import requests
import bs4

def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        # r.encoding = r.apparent_encoding
        # r.encoding = 'utf-8'
        r.encoding = 'gbk'
        return r.text
    except:
        return " Something Wrong！ "

def get_movie(url):
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

    # 读取
    sum_list = soup.find('ul', attrs={'class': 'picList clearfix'})

    # 用open的w+模式覆盖文件
    with open('movie_list.csv', 'w+') as f:
            f.write("")

    for sum in sum_list:

        # 找到全部小说名字，发现她们全部都包含在li标签中
        movie_list = sum_list.find_all('li')
        # 循环遍历每一个电影的名字以及链接
        for movie in movie_list:
            link = 'http:' + movie.a['href']
            title = movie.span.a.text
            print(title)
            # 将所有电影的url地址保存在一个列表变量里
            url_list.append(link)
            # 这里使用a模式,防止清空文件
            with open('movie_list.csv', 'a') as f:
                f.write("电影名: {:<} \t 电影地址: {:<} \n".format(title, link))

    return url_list

def main():

   base_url= 'http://dianying.2345.com/top/'
   url_list = get_movie(base_url)

if __name__ == '__main__':
    main()

