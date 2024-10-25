# -*- coding: utf-8 -*-
# @time : 2024/3/13 22:06
import os
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import pandas as pd
import datetime

class Spy(object):

    def __init__(self):
        None

    def creatWin(self):
        chrome_driver_path = '/Users/admin/Downloads/Wyatt/DailyDataProgram/chromedriver'
        # 禁用通知
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        # chrome_options.add_argument("--headless")
        # prefs = {"profile.managed_default_content_settings.images": 2}  # 这会禁止图片加载
        # chrome_options.add_experimental_option("prefs", prefs)
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # driver.get(url)
        # self.closeDialog(driver)
        return driver

    def get_element_by_xpath(self, driver, xpath):
        element= WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element

    def get_elements_by_xpath(self, driver, xpath):
        element= WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        return element

    def get_element_by_class_name(self, driver, class_name):
        element= WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
        return element

    def get_elements_by_class_name(self, driver, class_name):
        element= WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
        )
        return element

    def get_element_by_tag(self, driver, tag_name):
        element= WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, tag_name))
        )
        return element

    def get_elements_by_tag(self, driver, tag_name):
        element= WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, tag_name))
        )
        return element

    def classes_name(self, tag,str):
        str_list = str.split(' ')
        xpath = f'//{tag}['
        for i in str_list:
            xpath = xpath + f'contains(@class,"{i}") and '
        return xpath.strip('and ')+']'

    def main(self):
        # driver.get('https://www.coinglass.com/zh/bitcoin-etf')

        folder_name = 'DailyData/' + str(datetime.date.today()) +'/Table/'

        cex_names = ['Binance', 'Coinbase-Exchange', 'Bybit', 'OKX', 'Upbit']

        cex_BTCETH_volume = []
        cex_total_volume = []

        for cex in cex_names:
            driver = self.creatWin()
            driver.get('https://coinmarketcap.com/exchanges/'+cex)
            time.sleep(1)

            response = requests.get('https://coinmarketcap.com/exchanges/' + cex)
            # print(response.status_code)
            # print(response.text)
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup)

            volume = soup.find_all(class_='sc-4984dd93-0 cwfNhn priceText')
            cex_total_volume.append([cex.replace('-',' '), format(int(float(volume[0].text.replace('$','').replace(',',''))),',')])

            for i in range(1):
                buttons = self.get_elements_by_xpath(driver,
                                           self.classes_name('button', 'sc-2861d03b-0 iqkKeD sc-d36bb8b9-11 hQuCHd'))
                # print(len(buttons))
                button = buttons[len(buttons)-1]
                action = ActionChains(driver)
                action.move_to_element(button).click().perform()
                time.sleep(7)

            el = self.get_element_by_xpath(driver, self.classes_name('table', 'sc-14cb040a-3 ldpbBC cmc-table'))
            target = self.get_element_by_tag(el, 'tbody')
            trs = self.get_elements_by_xpath(target, './tr')
            print(len(trs))
            # ls1 = []
            top100_volume = 0
            pair_btc = []
            pair_eth = []
            btc_volume = 0
            eth_volume = 0
            for i in trs:
                row = i.text.split('\n')
                vol = int(row[-3].replace(',','').replace('$',''))
                top100_volume = top100_volume + vol
                if 'BTC/' in row[2] :
                    pair_btc.append([cex.replace('-',' '), row[2], row[-3]])
                    btc_volume = btc_volume + vol
                if 'ETH/' in row[2]:
                    pair_eth.append([cex.replace('-',' '), row[2], row[-3]])
                    eth_volume = eth_volume + vol

            cex_BTCETH_volume += pair_btc
            cex_BTCETH_volume += pair_eth
            cex_total_volume[-1].append(format(btc_volume, ','))
            cex_total_volume[-1].append(format(eth_volume, ','))
            cex_total_volume[-1].append(top100_volume)

            # print(len(cex_BTCETH_volume))
            driver.quit()

        df_cex_BTCETH_volume = pd.DataFrame(cex_BTCETH_volume, columns=['Exchanges', 'Pair', 'Volume'])
        df_cex_total_volume = pd.DataFrame(cex_total_volume, columns=['交易所', '24小时总交易量（美元）', '24小时比特币总交易量（美元）', '24小时以太坊总交易量（美元）', 'Top100 Volume'])
        print(df_cex_BTCETH_volume)
        totalVolume = df_cex_total_volume['24小时总交易量（美元）'].apply(lambda x: int(x.replace(',',''))).sum()
        totalBTC = df_cex_total_volume['24小时比特币总交易量（美元）'].apply(lambda x: int(x.replace(',',''))).sum()
        totalETH = df_cex_total_volume['24小时以太坊总交易量（美元）'].apply(lambda x: int(x.replace(',',''))).sum()
        df_cex_BTCETH_volume.to_csv(folder_name+'CEX Pair Volume(24h)-'+ str(datetime.date.today()) +'.csv')
        df_cex_total_volume.to_csv(folder_name+'CEX Volume(24h)-'+ str(datetime.date.today()) +'.csv')
        # df_BTC_ETH_Ratio = pd.read_excel('/Test/BTC_ETH_Ratio.xlsx')
        # df_BTC_ETH_Ratio['日期']
        # df_BTC_ETH_Ratio.()
        print('----------------------------------')
        print(totalBTC/totalVolume)
        print(totalETH/totalVolume)


if __name__ == '__main__':
    run = Spy()
    run.main()

def get_cexvolume():
    run = Spy()
    run.main()
