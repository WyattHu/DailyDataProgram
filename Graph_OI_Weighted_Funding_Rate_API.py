import json
import pandas as pd
import requests
import datetime
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt


def run():
    names=['BTC','ETH']
    for i in names:
        url = 'https://open-api-v3.coinglass.com/api/futures/fundingRate/oi-weight-ohlc-history?symbol='+i+'&interval=8h'
        headers = {
            "accept": "application/json",
            "CG-API-KEY": "5ef2d7b19ff6412bb56a63077f2bd42b"
        }

        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        df = pd.DataFrame(data['data'])
        # print(df)
        df = df[['t', 'o']]
        df.rename(columns={'t':'datetime','o':'value'},inplace=True)
        # print(df)
        df['datetime'] = df['datetime'].apply(
            lambda x: datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=x))
        df = df[df['datetime'] >= datetime.datetime.now() - relativedelta(months=1)-relativedelta(days=1)]
        df['value'] = df['value'].apply(lambda x: float(x)/100)
        plt.figure(figsize=(2, 0.35))
        plt.plot(df['datetime'], df['value'], color='r')
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.yticks([])
        plt.xticks([])
        folder_name = 'DailyData/' + str(datetime.date.today()) + '/Graph/'
        plt.savefig(folder_name + '/持仓加权资金费率-' + i + '.jpg')
        df.to_csv(folder_name + '/Rowdata/持仓加权资金费率-' + i + '.csv')
        print('Graph: ' + '持仓加权资金费率-' + i + ' finished!')


if __name__ == '__main__':
    run()
