import pandas as pd
import requests
import json
import datetime


def get_coinglassbtcetf():
    url = "https://open-api-v3.coinglass.com/api/bitcoin/etf/list"

    headers = {
        "accept": "application/json",
        "CG-API-KEY": "5ef2d7b19ff6412bb56a63077f2bd42b"
    }

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    df_US_BTC_ETF = pd.DataFrame(data['data'])
    df_US_BTC_ETF = df_US_BTC_ETF[df_US_BTC_ETF['type'] == 'Spot']
    df_US_BTC_ETF['溢价/折价'] = df_US_BTC_ETF['assetInfo'].apply(lambda x: str(round(float(x['premiumDiscount']), 2))+'%')
    df_US_BTC_ETF['持有比特币总量（个）'] = df_US_BTC_ETF['assetInfo'].apply(lambda x: format(int(round(float(x['btcHolding']))),','))
    df_US_BTC_ETF['每日持有变化（个）'] = df_US_BTC_ETF['assetInfo'].apply(lambda x: format(int(round(float(x['btcChange1d']))),','))
    df_US_BTC_ETF['每日持有变化百分比'] = df_US_BTC_ETF['assetInfo'].apply(lambda x: str(round(float(x['btcChangePercent1d']),2))+'%')
    df_US_BTC_ETF['priceChangePercent'] = df_US_BTC_ETF['priceChangePercent'].apply(lambda x: str(round(float(x),2))+'%')
    df_US_BTC_ETF['volumeUsd'] = df_US_BTC_ETF['volumeUsd'].apply(lambda x: float(x))
    df_US_BTC_ETF['marketCap'] = df_US_BTC_ETF['marketCap'].apply(lambda x: float(x))
    df_US_BTC_ETF['换手率'] = df_US_BTC_ETF['volumeUsd']/df_US_BTC_ETF['marketCap']
    df_US_BTC_ETF['换手率'] = df_US_BTC_ETF['换手率'].apply(lambda x: str(round(x,4)*100)+'%')

    df_US_BTC_ETF['volumeUsd'] = df_US_BTC_ETF['volumeUsd'].apply(lambda x: round(float(x)/100000000, 2))
    df_US_BTC_ETF['marketCap'] = df_US_BTC_ETF['marketCap'].apply(lambda x: round(float(x)/100000000, 2))
    df_US_BTC_ETF['aum'] = df_US_BTC_ETF['aum'].apply(lambda x: round(float(x)/100000000,2))
    df_US_BTC_ETF['fee'] = df_US_BTC_ETF['fee'].apply(lambda x: str(round(float(x), 2))+'%')

    df_US_BTC_ETF.rename(columns={'ticker': '交易代码', 'name': 'ETF名称','price':'价格(美元)','priceChangePercent':'价格变化百分比',
                                  'volumeUsd':'成交额(亿美元)','aum':'资产管理规模(亿美元)','marketCap':'市值(亿美元)',
                                  'fee':'费用率'}, inplace=True)
    df_US_BTC_ETF = df_US_BTC_ETF[['交易代码','ETF名称','价格(美元)','价格变化百分比','成交额(亿美元)','换手率','资产管理规模(亿美元)',
                                   '市值(亿美元)','费用率','溢价/折价','持有比特币总量（个）','每日持有变化（个）','每日持有变化百分比']]
    df_US_BTC_ETF = df_US_BTC_ETF.sort_values(by=['市值(亿美元)'], ascending=False)
    df_US_BTC_ETF = df_US_BTC_ETF.reset_index(drop=True)
    # print(df_US_BTC_ETF)
    folder_name = 'DailyData/' + str(datetime.date.today()) + '/Table/'
    df_US_BTC_ETF.to_csv(folder_name+'Coinglass_BTC-ETF-'+str(datetime.date.today())+'.csv')
    print('Table : Coinglass_BTC-ETF finished!')

if __name__ == '__main__':
    get_coinglassbtcetf()
