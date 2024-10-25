import datetime
import json
import pandas as pd
import requests


def run():
    folder_name = 'DailyData/' + str(datetime.date.today()) + '/Table/'
    try:
        url = "https://open-api-v3.coinglass.com/api/index/fear-greed-history"
        headers = {
            "accept": "application/json",
            "CG-API-KEY": "5ef2d7b19ff6412bb56a63077f2bd42b"
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        df = pd.DataFrame(data['data'])
        df['dates'] = df['dates'].apply(lambda x: datetime.datetime.fromtimestamp(x / 1000).strftime('%Y-%m-%d'))
        print('----------------------------------------------------------------')
        print('Table : Fear&Greed finished!')
        print('----------------------------------------------------------------')

        df.drop('prices', axis=1).to_csv(
            folder_name + 'FearAndGreed-' + str(datetime.date.today()) + '.csv')
    except:
        pass


if __name__ == '__main__':
    run()
