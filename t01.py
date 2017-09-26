import requests
LOGIN_URL = 'http://b2b.huangye88.com/guangdong/wenduyibiao31/'
headers = {}
data = {}
headers['User-Agent'] = 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'

res = requests.get(LOGIN_URL, headers=headers)

def main():
     for i in range(1, 3):
       if i == 1:
           base_url= 'http://b2b.huangye88.com/guangdong/wenduyibiao31'
       else:
           base_url= 'http://b2b.huangye88.com/guangdong/wenduyibiao31/pn'+str(i+1)+'/'
       print(base_url)

if __name__ == '__main__':
    main()