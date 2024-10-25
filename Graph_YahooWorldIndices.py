import datetime
import os

import pandas as pd
import yfinance as yf
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

import openpyxl
from openpyxl.drawing.image import Image
from PIL import Image as PILImage


def get_yahooworldindices():
    folder_name = 'DailyData/' + str(datetime.date.today()) + '/Graph/'

    #^GSPC ^IXIC ^VIX GC=F ^TNX
    #^GSPC ^IXIC 实时更新
    #^VIX 延迟15分钟更新
    #GC=F 延迟10分钟更新
    #^TNX
    tickers = ['^GSPC', '^IXIC','^VIX', 'GC=F', '^TNX', 'DX-Y.NYB', 'ETH-USD', 'COIN', 'WGMI', 'JPY=X']
    names = ['标普500指数', '纳斯达克指数', 'VIX', '黄金价格', '10年期美债收益率', '美元指数（DXY）', '以太坊价格', 'Coinbase(COIN)价格', 'WGMI', 'USDJPY']
    val = []
    index = 0
    for i in tickers:
        ret = yf.download(i, period='30d', interval='1d', group_by='ticker',prepost= True)
        ret = ret.reset_index()
        ret = ret[ret['Date'] >= datetime.datetime.now()-relativedelta(months=1)-relativedelta(days=1)]
        if datetime.date.today().weekday() in [0, 1, 2, 3, 4]:
            ret = ret.iloc[:-1]
        # ret['Datetime'] = ret['Datetime'].apply(lambda x: x.tz_convert("Asia/Shanghai"))
        ret.to_csv(folder_name+'Rowdata/'+names[index]+'.csv')
        plt.cla()
        plt.figure(figsize=(2, 0.35))
        plt.plot(ret['Date'], ret['Close'], color='r')
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.yticks([])
        plt.xticks([])
        plt.savefig(folder_name+names[index]+'.jpg')
        print('Graph: ' + names[index] + ' finished!')
        # ret.to_csv(names[index]+'.csv')
        index += 1


if __name__ == '__main__':
    get_yahooworldindices()
