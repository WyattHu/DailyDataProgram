import datetime
import time
import os
import pandas as pd
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import requests
from bs4 import BeautifulSoup

def get_cryptotop5():
    folder_name = 'DailyData/' + str(datetime.date.today()) +'/Table/'

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'200',
      'convert':'USD',
      'sort_dir':'desc'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'c3189f52-161e-4781-8d67-287bdff425df'
    }
    top5data = []

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      for i in [0, 1, 3, 4]:
        top5data.append([data['data'][i]['symbol'],
               round(data['data'][i]['quote']['USD']['price'], 2),
               str(round(data['data'][i]['quote']['USD']['percent_change_24h'], 2))+'%',
               data['data'][i]['quote']['USD']['last_updated']])
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

    df_top5data = pd.DataFrame(top5data, columns=['symbol', 'price', 'percent_change_24h', 'last_updated'])

    try:
        url = "https://open-api-v3.coinglass.com/api/index/fear-greed-history"
        headers = {
            "accept": "application/json",
            "CG-API-KEY": "5ef2d7b19ff6412bb56a63077f2bd42b"
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        df = pd.DataFrame(data['data'])
        # print(df['values'].iloc[-1])

        # ret = requests.get('https://www.binance.com/zh-CN/square/fear-and-greed-index')
        # time.sleep(0.2)
        # ret = requests.get('https://www.binance.com/zh-CN/square/fear-and-greed-index')
        # soup = BeautifulSoup(ret.content, 'html.parser')
        # div1 = soup.find_all(class_='css-cxlpc6')[0]
        # feargreed_today = int(div1.text)
        # div2 = soup.find_all(class_='css-mbfr6e')[0]
        # feargreed_yestoday = int(div2.text)
        feargreed_today = df['values'].iloc[-1]
        feargreed_yestoday = df['values'].iloc[-2]
        df_feargreed = pd.DataFrame({'symbol': ['Fear&Greed'],
                                     'price': [feargreed_today],
                                     'percent_change_24h': [
                                         str(round(100 * (feargreed_today - feargreed_yestoday) / feargreed_yestoday,
                                                   2)) + '%'],
                                     'last_updated': ''})
        df_top5data = pd.concat([df_top5data, df_feargreed], ignore_index=True)
    except:
        pass
    print('----------------------------------------------------------------')
    print(df_top5data)
    print('Table : CryptoTop5 finished!')
    print('----------------------------------------------------------------')

    df_top5data.drop('last_updated', axis=1).to_csv(
            folder_name+'CryptoTop5-' + str(datetime.date.today()) + '.csv')


if __name__ == '__main__':
    get_cryptotop5()
