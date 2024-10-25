import datetime
import time
import os
import pandas as pd
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import requests
from bs4 import BeautifulSoup


def get_cryptotop10():
    folder_name = 'DailyData/' + str(datetime.date.today()) + '/Table/'

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'500',
      'convert':'USD',
      'sort_dir':'desc'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'c3189f52-161e-4781-8d67-287bdff425df'
    }
    top10data = []

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      for i in range(500):
        top10data.append([data['data'][i]['symbol'],
               round(data['data'][i]['quote']['USD']['price'], 2),
               data['data'][i]['quote']['USD']['percent_change_24h'],
               data['data'][i]['quote']['USD']['last_updated']])
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)


    df_top10data = pd.DataFrame(top10data, columns=['symbol', 'price', 'percent_change_24h', 'last_updated'])
    df = df_top10data.sort_values(by=['percent_change_24h'], ascending=False)
    df['percent_change_24h'] = df['percent_change_24h'].apply(lambda x: str(round(x, 2)) + '%')
    df_top10 = pd.concat([df[:15],df[-15:]],ignore_index=True)
    print('----------------------------------------------------------------')
    print(df_top10)
    print('Table : CryptoTop10 finished!')
    print('----------------------------------------------------------------')
    df_top10.drop(['price', 'last_updated'], axis=1).to_csv(folder_name+'CryptoTop10-'+str(datetime.date.today())+'.csv')


if __name__ == '__main__':
    get_cryptotop10()
