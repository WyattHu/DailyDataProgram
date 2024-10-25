import json
import pandas as pd
import requests
import datetime
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt


def run():
    url = "https://open-api-v3.coinglass.com/api/spot/takerBuySellVolume/history?exchange=Binance&symbol=BTCUSDT&interval=1d"
    headers = {
        "accept": "application/json",
        "CG-API-KEY": "5ef2d7b19ff6412bb56a63077f2bd42b"
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    df = pd.DataFrame(data['data'])
    # df['time'] = df['time'].apply(
    #     lambda x: datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=x))
    print(df)


    # df['value'] = df['value'].apply(lambda x: float(x)/100)
    # plt.figure(figsize=(2, 0.35))
    # plt.plot(df['datetime'], df['value'], color='r')
    # plt.gca().spines['right'].set_visible(False)
    # plt.gca().spines['top'].set_visible(False)
    # plt.gca().spines['left'].set_visible(False)
    # plt.gca().spines['bottom'].set_visible(False)
    # plt.yticks([])
    # plt.xticks([])
    # folder_name = 'DailyData/' + str(datetime.date.today()) + '/Graph/'
    # plt.savefig(folder_name + '/持仓加权资金费率-' + i + '.jpg')
    # df.to_csv(folder_name + '/Rowdata/持仓加权资金费率-' + i + '.csv')
    # print('Graph: ' + '持仓加权资金费率-' + i + ' finished!')


if __name__ == '__main__':
    run()
