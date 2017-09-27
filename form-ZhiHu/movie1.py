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
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')

    # 读取
    sum_list = soup.find('ul', attrs={'class': 'picList clearfix'})

    # 用open的w+模式覆盖文件
    with open('movie_list.csv', 'w+') as f:
            f.write("")

    # 找到全部小说名字，发现她们全部都包含在li标签中
    movie_list = sum_list.find_all('li')
    # 循环遍历每一个电影的名字以及链接
    for movie in movie_list:

        name = movie.span.a.text
        #这里做一个异常捕获，防止没有上映时间的出现
        try:
            time = movie.find('span', class_='sIntro').text
        except:
            time = "暂无上映时间"
        link = 'http:' + movie.a['href']
        #找到影片简介
        intro = movie.find('p', class_='pTxt pIntroShow').text
        print("片名：{}\t{}\n{}\n{}\n \n ".format(name, time, link, intro))

        # 这里使用a模式,防止清空文件
        with open('movie_list.csv', 'a') as f:
            f.write("电影名: {:<} \t {}\n 电影地址: {:<} \n".format(name, time, link))

def main():

   base_url= 'http://dianying.2345.com/top/'
   get_movie(base_url)

if __name__ == '__main__':
    main()