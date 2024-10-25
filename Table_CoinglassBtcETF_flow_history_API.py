import datetime
import pandas as pd
import requests
import json


def get_coinglassbtcetf_flowhistory():
    url = "https://open-api-v3.coinglass.com/api/bitcoin/etf/flow-history"

    headers = {
        "accept": "application/json",
        "CG-API-KEY": "5ef2d7b19ff6412bb56a63077f2bd42b"
    }

    holidays = []
    holidays.append(1716768000000)

    response = requests.get(url, headers=headers)

    # print(response.text)
    data = json.loads(response.text)
    # print(data['data'][0])

    for i in range(len(data['data'])):
        # print(data['data'][i])
        for j in data['data'][i]['list']:
            ticker = j['ticker']
            try:
                changeUsd = j['changeUsd']
            except:
                changeUsd = 0
            # print(i)
            data['data'][i][ticker] = round(float(changeUsd)/1000000, 1)
    df = pd.DataFrame(data['data'])
    df = df[df['date'] != holidays[0]]
    df['date'] = df['date'].apply(lambda x:  datetime.datetime.fromtimestamp(x/1000).strftime('%Y-%m-%d %H:%M:%S'))
    df['changeUsd'] = df['changeUsd'].apply(lambda x: round(float(x)/1000000, 1))
    df = df.drop(['price', 'list'], axis=1)
    df.rename(columns={'changeUsd': 'Total'}, inplace=True)
    if datetime.date.today().weekday() != 5 and datetime.date.today().weekday() != 6:
        df.drop(index=df.index[-1], axis=0, inplace=True)
    folder_name = 'DailyData/' + str(datetime.date.today()) + '/Table/'
    df.to_csv(folder_name+'Coinglass_BTC-ETF-FlowHistory-'+str(datetime.date.today())+'.csv')
    print('Table : Coinglass_BTC-ETF-FlowHistory finished!')


if __name__ == '__main__':
    get_coinglassbtcetf_flowhistory()
