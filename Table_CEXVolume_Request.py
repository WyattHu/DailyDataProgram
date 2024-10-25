import datetime
import os
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt


def get_cexvolume():
    folder_name = 'DailyData/' + str(datetime.date.today()) + '/Table/'

    cex_names = ['Binance', 'Coinbase-Exchange', 'Bybit', 'OKX', 'Upbit']

    cex_BTCETH_volume = []
    cex_total_volume = []

    for cex in cex_names:
        response = requests.get('https://coinmarketcap.com/exchanges/'+cex)
        time.sleep(2)
        # response = requests.get('https://coinmarketcap.com/exchanges/'+cex)
        # print(response.status_code)
        # print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)

        volume = soup.find_all(class_='sc-71024e3e-0 iPzNbd priceText')
        # print(volume)
        cex_total_volume.append(
            [cex.replace('-', ' '), format(int(float(volume[0].text.replace('$', '').replace(',', ''))), ',')])

        tbody = soup.select('table[class="sc-ae0cff98-3 gtujv cmc-table"]>tbody')[0]
        # print(tbody)

        trs = tbody.select('tr') #定位到tr
        if len(trs) == 50:
            print(cex+' : 获取交易所数据 finished!')
        else:
            print(cex+' : 获取交易所数据 failed!')
        top50_volume = 0
        pair_btc = []
        pair_eth = []
        btc_volume = 0
        eth_volume = 0
        for tr in trs:
            tds = tr.select('td')
            vol = int(tds[6].text.replace(',','').replace('$',''))
            top50_volume = top50_volume+vol
            if 'BTC/' in tds[2].text:
                pair_btc.append([cex.replace('-',' '), tds[2].text, tds[6].text])
                btc_volume = btc_volume + vol
            if 'ETH/' in tds[2].text:
                pair_eth.append([cex.replace('-',' '), tds[2].text, tds[6].text])
                eth_volume = eth_volume + vol

        cex_BTCETH_volume += pair_btc
        cex_BTCETH_volume += pair_eth
        cex_total_volume[-1].append(format(btc_volume, ','))
        cex_total_volume[-1].append(format(eth_volume, ','))
        cex_total_volume[-1].append(top50_volume)

    df_cex_BTCETH_volume = pd.DataFrame(cex_BTCETH_volume, columns=['Exchanges', 'Pair', 'Volume'])
    df_cex_total_volume = pd.DataFrame(cex_total_volume,
                                       columns=['交易所', '24小时总交易量（美元）', '24小时比特币总交易量（美元）',
                                                '24小时以太坊总交易量（美元）', 'Top100 Volume'])
    # print(df_cex_BTCETH_volume)
    print('----------------------------------------------------------------')
    print(df_cex_BTCETH_volume)
    print(df_cex_total_volume)
    totalVolume = df_cex_total_volume['24小时总交易量（美元）'].apply(lambda x: int(x.replace(',', ''))).sum()
    totalBTC = df_cex_total_volume['24小时比特币总交易量（美元）'].apply(lambda x: int(x.replace(',', ''))).sum()
    totalETH = df_cex_total_volume['24小时以太坊总交易量（美元）'].apply(lambda x: int(x.replace(',', ''))).sum()
    df_cex_BTCETH_volume.to_csv(folder_name + 'CEX Pair Volume(24h)-' + str(datetime.date.today()) + '.csv')
    df_cex_total_volume.to_csv(folder_name + 'CEX Volume(24h)-' + str(datetime.date.today()) + '.csv')

    df_ratio = pd.read_excel('DailyData/BTC_ETH_Ratio.xlsx')
    df_ratio = df_ratio.drop(columns=['Unnamed: 0'])
    df_ratio = df_ratio.drop(df_ratio[df_ratio['日期']==pd.to_datetime(str(datetime.date.today()))].index)
    # print(df_ratio)
    new_row = pd.DataFrame([[pd.to_datetime(str(datetime.date.today())), totalBTC / totalVolume, totalETH / totalVolume]], columns=df_ratio.columns)
    df_ratio = pd.concat([df_ratio,new_row],ignore_index=True)
    df_ratio.to_excel('DailyData/BTC_ETH_Ratio.xlsx')
    folder_name1 = 'DailyData/' + str(datetime.date.today()) + '/Graph/'
    df_ratio.to_excel(folder_name1 + 'Rowdata/BTC_ETH_Ratio.xlsx')
    plt.cla()
    plt.figure(figsize=(2, 0.35))
    plt.plot(df_ratio['比特币占比'], color='r')
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.yticks([])
    plt.xticks([])
    plt.savefig(folder_name1+'比特币交易量占比.jpg')

    plt.cla()
    plt.figure(figsize=(2, 0.35))
    plt.plot(df_ratio['以太坊占比'], color='r')
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.yticks([])
    plt.xticks([])
    plt.savefig(folder_name1+'以太坊交易量占比.jpg')

    print('----------------------------------------------------------------')
    print('比特币交易量占比：')
    print(totalBTC / totalVolume)
    print('以太坊交易量占比：')
    print(totalETH / totalVolume)
    print('Table : Cex Volume finished!')
    print('----------------------------------------------------------------')


if __name__ == '__main__':
    get_cexvolume()
