import json
import pandas as pd
import requests
import datetime
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt


def run():
    folder_name = 'DailyData/' + str(datetime.date.today()) + '/Graph/'
    names=['Binance','OKX','Bybit']
    ls_df = []
    for i in names:
        url = 'https://open-api-v3.coinglass.com/api/borrowInterestRate/history?exchange='+i+'&symbol=USDT&interval=1d'

        headers = {
            "accept": "application/json",
            "CG-API-KEY": "5ef2d7b19ff6412bb56a63077f2bd42b"
        }

        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        df = pd.DataFrame(data['data'])
        df['time'] = df['time'].apply(
            lambda x: datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=x))
        df = df[df['time'] >= datetime.datetime.now() - relativedelta(months=1)-relativedelta(days=1)]
        df['interestRate'] = df['interestRate'].apply(lambda x: x*365/100)
        df.rename(columns={'time':'datetime','interestRate':'value'},inplace=True)
        df.to_csv(folder_name + 'Rowdata/' +'USDT杠杆借贷年利率-' + i + '.csv')
        ls_df.append(df)
    df_avg = ls_df[0]
    df_avg['value'] = round((ls_df[0]['value'] + ls_df[1]['value'] + ls_df[2]['value']) / 3, 4)
    plt.figure(figsize=(2, 0.35))
    plt.plot(df_avg['datetime'], df_avg['value'], color='r')
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.yticks([])
    plt.xticks([])
    plt.savefig(folder_name + 'USDT杠杆借贷年利率-平均.jpg')
    df_avg.to_csv(folder_name + 'Rowdata/' + 'USDT杠杆借贷年利率-平均.csv')
    print('Graph: USDT杠杆借贷年利率-平均 finished!')


if __name__ == '__main__':
    run()
