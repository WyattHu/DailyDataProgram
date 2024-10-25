import datetime
import time
import requests
import pandas as pd
import os
from bs4 import BeautifulSoup

folder_name = 'DailyData/' + str(datetime.date.today())  # 判断当天文件夹是否存在
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

time_now = datetime.datetime.now()  # 获取当前时间
today = datetime.datetime.today()   # 今天日期

# 当前时间未到当天晚上21：30时，进入循环
while time_now < datetime.datetime(today.year, today.month, today.day, 21, 30, 00):
    time_now = datetime.datetime.now()
    time.sleep(0.1)

# CoinGecko API 的 URL
url = 'https://api.coingecko.com/api/v3/coins/markets'

# 请求参数
params = {
    'vs_currency': 'usd',  # 要对比的货币
    'per_page': 250,     # 每页数量
    'page': 1           # 第一页
}

# 发送 GET 请求
response = requests.get(url, params=params)
# 检查请求是否成功
if response.status_code == 200:
    data = response.json()
    # 前250币种
    data_df1 = pd.DataFrame(data)
    data_df1 = data_df1[['name', 'symbol', 'current_price', 'price_change_percentage_24h']]
    data_df1['current_price'] = data_df1['current_price'].apply(lambda x: round(x, 2))
    # print(data_df1)
else:
    print('从 API 获取市值前二百五币种数据失败')

# 请求参数
params = {
    'vs_currency': 'usd',  # 要对比的货币
    'per_page': 250,    # 每页数量
    'page': 2          # 第二页
}

# 发送 GET 请求
response = requests.get(url, params=params)
# 检查请求是否成功
if response.status_code == 200:
    data = response.json()
    # 250-500币种
    data_df2 = pd.DataFrame(data)
    data_df2 = data_df2[['name', 'symbol', 'current_price', 'price_change_percentage_24h']]
    data_df2['current_price'] = data_df2['current_price'].apply(lambda x: round(x, 2))
    # print(data_df2)
else:
    print('从 API 获取市值二百五至五百币种数据失败')

df = pd.concat([data_df1,data_df2], ignore_index=True)
df['symbol'] = df['symbol'].apply(lambda x: x.upper())
df = df.sort_values(by=['price_change_percentage_24h'], ascending=False)
df['price_change_percentage_24h'] = df['price_change_percentage_24h'].apply(lambda x: str(round(x, 2)) + '%')
# print(df)
df_top10 = pd.concat([df[:15],df[-15:]],ignore_index=True)
# print(df_top10)
df_top10.to_csv(folder_name+'/DailyDataTop15-'+str(datetime.date.today())+'.csv')
