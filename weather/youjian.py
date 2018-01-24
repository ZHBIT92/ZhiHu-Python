#coding: utf-8
import smtplib
from email import encoders     #用于base64编码
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart   #附件
from email.mime.base import MIMEBase    #文件格式基类，定义一个文件类型，文件类型不是按后缀名来


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

sender = '13676077914@163.com'
receiver = '843731066@qq.com'
subject = 'python email test'
smtpserver = 'smtp.163.com'
username = '13676077914@163.com'
password = 'wxk5895821'

msg = MIMEMultipart()
msg['From'] = _format_addr('锴锴同学 <%s>' % sender)
msg['To'] = _format_addr('<%s>' % receiver)
msg['Subject'] = Header('来自锴锴同学的问候……', 'utf-8').encode()

# 邮件正文是MIMEText:
msgText = MIMEText('<html><body><h1>Hello</h1>' +
    '<p><img src="cid:0"></p>' +
    '</body></html>', 'html', 'utf-8')
msg.attach(msgText)

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

# SMTP协议默认端口是25
server = smtplib.SMTP(smtpserver, 25)
server.starttls()
server.set_debuglevel(1)
server.login(username, password)
server.sendmail(sender, receiver, msg.as_string())
server.quit( )