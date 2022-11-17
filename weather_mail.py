import smtplib
import requests
from bs4 import BeautifulSoup
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

# 南京
url = "http://www.weather.com.cn/weather/101190101.shtml"
# 广水
# url = "http://www.weather.com.cn/weather/101201302.shtml"
header = {"User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 "
          "Safari/537.36"}  # 设置头部信息

# opener = urllib.request.build_opener()  # 修改头部信息
# opener.addheaders = [header]  # 修改头部信息
# request = urllib.request.Request(url)  # 制作请求
# response = urllib.request.urlopen(request)  # 得到请求的应答包
# html = response.read()  # 将应答包里面的内容读取出来
# html = html.decode('utf-8')  # 使用utf-8进行编码，不重新编码就会成乱码

# 注意这里的请求头是字典的格式 目的进行UA伪装
response = requests.get(url=url, headers=header)
response.encoding = response.apparent_encoding
html = response.text
# print(response.text)

bs = BeautifulSoup(html, 'html.parser')
body = bs.body
data = body.find('div', {'id': '7d'})
ul = data.find('ul')
li = ul.find_all('li')


# print(li)


def get_cd_weather():
    global li  # 声明全局变量li
    weather_data = []
    for i in li:
        strs = ''
        date = i.find('h1').string  # 找到第一个h1 获取每一天的日期信息字符串
        strs += str(time.strftime('%Y', time.localtime(time.time()))) + '年' + str(
            time.strftime('%m', time.localtime(time.time()))) + '月' + date + '\t'
        weather = i.find('p').string
        strs += weather + '\t'
        max_c = i.find('span').string  # 获取最大温度
        min_c = i.find('i').string  # 获取最小温度
        if max_c is None:
            max_c = ''
        elif min_c is None:
            min_c = ''
        C = max_c + '\\' + min_c
        # print(date, weather, max_c, min_c)
        strs += C
        weather_data.append(strs)
    return weather_data


weather = get_cd_weather()

receiver = ['1465791433@qq.com']  # to my girlfriend
# 1465791433

# 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息
subject = '南京天气预报'
subject = Header(subject, 'utf-8').encode()
# 构造邮件对象MIMEultipart 对象
# 下面的主题、发件人、收件人、日期显示在邮件页面上
msg = MIMEMultipart('mixed')  # 创建信息对象
msg['Subject'] = subject
msg['From'] = 'Shamming Wang'
msg['To'] = ';'.join(receiver)
msg['Date'] = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))


# 写出html的基本骨架
html = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>天气预报</title>
</head>
<body>
<center>
<font size="5" font-family: "Arial","Microsoft YaHei","黑体","宋体",sans-serif;>南京一周的天气情况，请查收哦小家伙</font>
<br>
</center>
<table border="0" align="center">
  <tr>
    <td>%s</td>
  </tr>
  <tr>
    <td>%s</td>
  </tr>
  <tr>
    <td>%s</td>
  </tr>
  <tr>
    <td>%s</td>
  </tr>
  <tr>
    <td>%s</td>
  </tr>
  <tr>
    <td>%s</td>
  </tr>
  <tr>
    <td>%s</td>
  </tr>
</table>
</body>
</html>
''' % (weather[0], weather[1], weather[2], weather[3], weather[4], weather[5], weather[6])
text_html = MIMEText(html, 'html', 'utf-8')
# smtp 通过MIMEText类 发送HTML格式的邮件
msg.attach(text_html)  # 把生成的html丢入发送的信息中

# 最后一个模块是登录并发送邮件
# 注意这里是要在QQ邮箱开启smtp才可以代理发送

sender = '1685087768@qq.com'
user_name = '1685087768@qq.com'
password = ''  # 这个是QQ邮箱开启smtp之后给你生成的授权码

smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
smtp.login(user_name, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()

