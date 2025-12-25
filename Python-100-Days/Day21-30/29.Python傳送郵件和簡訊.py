#!/usr/bin/env python3
"""
從 29.Python发送邮件和短信.md 提取的 Python 範例代碼
"""

# === 範例 1 ===
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 建立郵件主體物件
email = MIMEMultipart()
# 設定發件人、收件人和主題
email['From'] = 'xxxxxxxxx@126.com'
email['To'] = 'yyyyyy@qq.com;zzzzzz@1000phone.com'
email['Subject'] = Header('上半年工作情況彙報', 'utf-8')
# 新增郵件正文內容
content = """據德國媒體報道，當地時間9日，德國火車司機工會成員進行了投票，
定於當地時間10日起進行全國性罷工，貨運交通方面的罷工已於當地時間10日19時開始。
此後，從11日凌晨2時到13日凌晨2時，德國全國範圍內的客運和鐵路基礎設施將進行48小時的罷工。"""
email.attach(MIMEText(content, 'plain', 'utf-8'))

# 建立SMTP_SSL物件（連線郵件伺服器）
smtp_obj = smtplib.SMTP_SSL('smtp.126.com', 465)
# 透過使用者名稱和授權碼進行登入
smtp_obj.login('xxxxxxxxx@126.com', '郵件伺服器的授權碼')
# 傳送郵件（發件人、收件人、郵件內容（字串））
smtp_obj.sendmail(
    'xxxxxxxxx@126.com',
    ['yyyyyy@qq.com', 'zzzzzz@1000phone.com'],
    email.as_string()
)
# === 範例 2 ===
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import quote

# 建立郵件主體物件
email = MIMEMultipart()
# 設定發件人、收件人和主題
email['From'] = 'xxxxxxxxx@126.com'
email['To'] = 'zzzzzzzz@1000phone.com'
email['Subject'] = Header('請查收離職證明檔案', 'utf-8')
# 新增郵件正文內容（帶HTML標籤排版的內容）
content = """<p>親愛的前同事：</p>
<p>你需要的離職證明在附件中，請查收！</p>
<br>
<p>祝，好！</p>
<hr>
<p>孫美麗 即日</p>"""
email.attach(MIMEText(content, 'html', 'utf-8'))
# 讀取作為附件的檔案
with open(f'resources/王大錘離職證明.docx', 'rb') as file:
    attachment = MIMEText(file.read(), 'base64', 'utf-8')
    # 指定內容型別
    attachment['content-type'] = 'application/octet-stream'
    # 將中文檔名處理成百分號編碼
    filename = quote('王大錘離職證明.docx')
    # 指定如何處置內容
    attachment['content-disposition'] = f'attachment; filename="{filename}"'

# 建立SMTP_SSL物件（連線郵件伺服器）
smtp_obj = smtplib.SMTP_SSL('smtp.126.com', 465)
# 透過使用者名稱和授權碼進行登入
smtp_obj.login('xxxxxxxxx@126.com', '郵件伺服器的授權碼')
# 傳送郵件（發件人、收件人、郵件內容（字串））
smtp_obj.sendmail(
    'xxxxxxxxx@126.com',
    'zzzzzzzz@1000phone.com',
    email.as_string()
)
# === 範例 3 ===
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import quote

# 郵件伺服器域名（自行修改）
EMAIL_HOST = 'smtp.126.com'
# 郵件服務埠（通常是465）
EMAIL_PORT = 465
# 登入郵件伺服器的賬號（自行修改）
EMAIL_USER = 'xxxxxxxxx@126.com'
# 開通SMTP服務的授權碼（自行修改）
EMAIL_AUTH = '郵件伺服器的授權碼'


def send_email(*, from_user, to_users, subject='', content='', filenames=[]):
    """傳送郵件
    
    :param from_user: 發件人
    :param to_users: 收件人，多個收件人用英文分號進行分隔
    :param subject: 郵件的主題
    :param content: 郵件正文內容
    :param filenames: 附件要傳送的檔案路徑
    """
    email = MIMEMultipart()
    email['From'] = from_user
    email['To'] = to_users
    email['Subject'] = subject

    message = MIMEText(content, 'plain', 'utf-8')
    email.attach(message)
    for filename in filenames:
        with open(filename, 'rb') as file:
            pos = filename.rfind('/')
            display_filename = filename[pos + 1:] if pos >= 0 else filename
            display_filename = quote(display_filename)
            attachment = MIMEText(file.read(), 'base64', 'utf-8')
            attachment['content-type'] = 'application/octet-stream'
            attachment['content-disposition'] = f'attachment; filename="{display_filename}"'
            email.attach(attachment)

    smtp = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
    smtp.login(EMAIL_USER, EMAIL_AUTH)
    smtp.sendmail(from_user, to_users.split(';'), email.as_string())
# === 範例 4 ===
import random

import requests


def send_message_by_luosimao(tel, message):
    """傳送簡訊（呼叫螺絲帽簡訊閘道器）"""
    resp = requests.post(
        url='http://sms-api.luosimao.com/v1/send.json',
        auth=('api', 'key-註冊成功後平臺分配的KEY'),
        data={
            'mobile': tel,
            'message': message
        },
        timeout=10,
        verify=False
    )
    return resp.json()


def gen_mobile_code(length=6):
    """生成指定長度的手機驗證碼"""
    return ''.join(random.choices('0123456789', k=length))


def main():
    code = gen_mobile_code()
    message = f'您的簡訊驗證碼是{code}，打死也不能告訴別人喲！【Python小課】'
    print(send_message_by_luosimao('13500112233', message))


if __name__ == '__main__':
    main()
