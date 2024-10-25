import datetime
import pandas as pd
import requests
import json
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt


def run():
    url = "https://open-api-v3.coinglass.com/api/bitcoin/etf/flow-history"

    headers = {
        "accept": "application/json",
        "CG-API-KEY": "5ef2d7b19ff6412bb56a63077f2bd42b"
    }

    holidays = []
    holidays.append(datetime.datetime(2024, 5, 27))

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    df_US_BTC_ETF_Inflow = pd.DataFrame(data['data'])
    # df_US_BTC_ETF_Inflow.to_csv('test.csv')
    df_US_BTC_ETF_Inflow = df_US_BTC_ETF_Inflow[['date','changeUsd']]
    df_US_BTC_ETF_Inflow['date'] = df_US_BTC_ETF_Inflow['date'].apply(lambda x: datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=x/1000))
    df_US_BTC_ETF_Inflow = df_US_BTC_ETF_Inflow[df_US_BTC_ETF_Inflow['date'] >= datetime.datetime.now() - relativedelta(months=1)-relativedelta(days=1)]
    df_US_BTC_ETF_Inflow = df_US_BTC_ETF_Inflow[df_US_BTC_ETF_Inflow['date'] != holidays[0]]

    df_US_BTC_ETF_Inflow['changeUsd'] = df_US_BTC_ETF_Inflow['changeUsd'].apply(lambda x: round(float(x)/1000000,2))

    df_US_BTC_ETF_Inflow.rename(columns={'date': 'datetime','changeUsd':'value'},inplace=True)
    if datetime.date.today().weekday() != 5 and datetime.date.today().weekday() != 6:
        df_US_BTC_ETF_Inflow.drop(index=df_US_BTC_ETF_Inflow.index[-1], axis=0, inplace=True)
    plt.figure(figsize=(2, 0.35))
    plt.plot(df_US_BTC_ETF_Inflow['datetime'], df_US_BTC_ETF_Inflow['value'], color='r')
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.yticks([])
    plt.xticks([])
    folder_name = 'DailyData/' + str(datetime.date.today()) + '/Graph/'
    plt.savefig(folder_name + '比特币现货ETF净流入流出.jpg')
    df_US_BTC_ETF_Inflow.to_csv(folder_name + 'Rowdata/比特币现货ETF净流入流出.csv')
    print('Graph: 比特币现货ETF净流入流出 finished!')


if __name__ == '__main__':
    run()
