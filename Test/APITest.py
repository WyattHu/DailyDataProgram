# import json
# from datetime import date
# import yfinance as yf
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
#
# url = 'https://www.binance.com/en/trade/BTC_USDT?ref=40896146&type=spot'
#
#
# response = requests.get(url)
# print(response.status_code)
# # print(response.text)
# soup = BeautifulSoup(response.text, 'html.parser')
# # print(soup)
# #
# # volume = soup.find_all(class_='tickerPriceText')[0]
# # print(volume.text)
#
# df = pd.read_excel('BTC_ETH_Ratio.xlsx')
# print(df.iloc[-1])
#

# import datetime
#
# import yfinance as yf
# from dateutil.relativedelta import relativedelta
#
# ret = yf.download('JPY=X', period='30d', interval='1d', group_by='ticker', prepost=True)
# ret = ret.reset_index()
# ret = ret[ret['Date'] >= datetime.datetime.now() - relativedelta(months=1)]
# print(ret)

from email.mime.text import MIMEText
import smtplib

#发件人列表
to_list=["124779203@qq.com",'wyatt.huyue@gmail.com']
#对于大型的邮件服务器，有反垃圾邮件的功能，必须登录后才能发邮件，如126,163
mail_server="smtp.126.com"   # 126的邮件服务器
mail_login_user="huyue428@126.com" #必须是真实存在的用户，这里我测试的时候写了自己的126邮箱
mail_passwd=""    #必须是对应上面用户的正确密码，我126邮箱对应的密码

def send_mail(to_list,sub,content):
     # to_list:发给谁
     # sub:主题
     # content:内容
     # send_mail("aaa@126.com","sub","content")
    me =''
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = mail_login_user
    msg['To'] = ";".join(to_list)
    try:
        print(1)
        s = smtplib.SMTP_SSL(mail_server,port=465)
        print(2)
        # s.connect(mail_server,port=465)
        print(3)
        s.login(mail_login_user,mail_passwd)
        s.sendmail(mail_login_user, to_list, msg.as_string())
        s.close()
        return True
    except Exception as e:
        print (e)
        return False


if __name__ == '__main__':
    send_mail(to_list,"subject","content")
