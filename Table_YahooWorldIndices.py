import datetime
import os

import pandas as pd
import yfinance as yf
#^GSPC ^IXIC ^VIX GC=F ^TNX
#^GSPC ^IXIC 实时更新
#^VIX 延迟15分钟更新
#GC=F 延迟10分钟更新
#^TNX

def get_yahooworldindices():
    tickers = ['^GSPC', '^IXIC','^VIX', 'GC=F', '^TNX']
    names = ['S&P500', 'NASDAQ', 'VIX', 'Gold(XAU)', 'US10yr']
    val = []
    index = 0
    for i in tickers:
        if datetime.date.today().weekday() != 5 and datetime.date.today().weekday() != 6:
            ret = yf.download(i, period='2d', interval='1m', group_by='ticker',prepost= True)
            ret = ret.reset_index()
            ret['Datetime'] = ret['Datetime'].apply(lambda x: x.tz_convert("Asia/Shanghai"))
            ret = ret[ret['Datetime'] >= pd.to_datetime(str(datetime.date.today())+' 21:30:00+08:00')]
            if len(ret) > 0:
                previousClose = yf.Ticker(i).info['previousClose']
                Open = ret.iloc[0]['Open']
                print(ret.iloc[0])
                val.append([names[index], round(Open, 2), round(previousClose, 2), str(round(100*(Open-previousClose)/previousClose, 2))+'%'])
        else:
            val.append([names[index], round(yf.Ticker(i).fast_info['lastPrice'], 2), round(yf.Ticker(i).fast_info['lastPrice'], 2), 'n.a.'])
        index += 1
    df = pd.DataFrame(val, columns=['Names', 'Price', 'PreviousClose', 'PercentChange'])

    print(df)

    folder_name = 'DailyData/' + str(datetime.date.today())+ '/Table/'

    df.drop('PreviousClose', axis=1).to_csv(folder_name+'WorldIndices-' + str(datetime.date.today()) + '.csv')


if __name__ == '__main__':
    get_yahooworldindices()
