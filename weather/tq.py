#coding: utf-8
import requests
import re
import smtplib
from email import encoders     #用于base64编码
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart   #附件
from email.mime.base import MIMEBase    #文件格式基类，定义一个文件类型，文件类型不是按后缀名来

API="https://api.seniverse.com/v3/weather/daily.json?"
def fetchWeather(location):
    content = requests.get(API, params={
        'key': "aixt85w0075i4ln5",
        'location': location,
        'language': "zh-Hans",
        'unit': "c",
        'start': "0",
        'days': "2",
    }, timeout=1).text
    print(content)
    #使用正则提取字段
    # 日期
    date = re.findall(r'"date":"(.*?)",', content)
    text_day = re.findall(r'"text_day":"(.*?)",', content)
    code_day = re.findall(r'"code_day":"(.*?)",', content)
    text_night = re.findall(r'"text_night":"(.*?)",', content)
    high = re.findall(r'"high":"(.*?)",', content)
    low = re.findall(r'"low":"(.*?)",', content)
    r =int(low[0])-int(low[1])
    print(r)
    tqi_list = []
    tqi_list.append(date[1])
    tqi_list.append(text_day[1])
    tqi_list.append(text_night[1])
    tqi_list.append(high[1])
    tqi_list.append(low[1])
    tqi_list.append(r)
    print(tqi_list)
    if(r>=2):
        k = 1
        youjian(k, tqi_list)
        print("明天会降温")
    if(int(code_day[1])>4):
        k = 2
        youjian(k, tqi_list)
        print("明天会下雨")
    else:
        k = 3
        youjian(k, tqi_list)
        print("正常播放天气")


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def youjian(k, tqi_list):
    sender = '13676077914@163.com'
    receiver = '843731066@qq.com'
    smtpserver = 'smtp.163.com'
    username = '13676077914@163.com'
    password = 'wxk5895821'
    msg = MIMEMultipart()
    msg['From'] = _format_addr('锴锴同学 <%s>' % sender)
    msg['To'] = _format_addr('<%s>' % receiver)
    msg['Subject'] = Header('来自锴锴同学的问候……', 'utf-8').encode()

    text_day = tqi_list[1]
    text_night = tqi_list[2]
    high = tqi_list[3]
    low = tqi_list[4]
    r = tqi_list[5]
    if k == 1:
        # 邮件正文是MIMEText:
        msgText = MIMEText('<html><body><h1>明天会降温'+r+'度，早上记得穿多一件哦</h1>' +
        # '<p><img src="cid:0"></p>' +
        '</body></html>', 'html', 'utf-8')
        msg.attach(msgText)
    if k == 2:
        # 邮件正文是MIMEText:
        msgText = MIMEText('<html><body><h1>明天会下雨'+k+'，记得带伞出门哦</h1>'
        '<p>明天白天天气：'+text_day+'</p>' +
        '<p>明天晚上天气：'+text_night+'</p>' +
        '<p>明天最高温：'+high+'</p>' +
        '<p>明天最低温：'+low+'</p>' +
        # '<p><img src="cid:0"></p>' +
        '</body></html>', 'html', 'utf-8')
        msg.attach(msgText)
    if k == 3:
        # 邮件正文是MIMEText:
        msgText = MIMEText('<html><body>'
        '<p>明天白天天气：'+text_day+'</p>' +
        '<p>明天晚上天气：'+text_night+'</p>' +
        '<p>明天最高温：'+high+'</p>' +
        '<p>明天最低温：'+low+'</p>' +
        # '<p><img src="cid:0"></p>' +
        '</body></html>', 'html', 'utf-8')
        msg.attach(msgText)
    '''
    # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
    with open('dog.jpg', 'rb') as f:
        # 设置附件的MIME和文件名，这里是png类型:
        mime = MIMEBase('image', 'png', filename='dog.jpg')
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename='dog.jpg')
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)
    '''
    # SMTP协议默认端口是25
    server = smtplib.SMTP(smtpserver, 25)
    server.starttls()
    server.set_debuglevel(1)
    server.login(username, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit( )

if __name__ == '__main__':
    location ="zhuhai"
    fetchWeather(location)
