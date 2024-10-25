import datetime

from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import re
from multiprocessing import Pool
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
from itertools import product
import pandas as pd
import os
import sys
from multiprocessing import Pool
from bs4 import BeautifulSoup
import sqlite3
import random


class Spy(object):
    def __init__(self):
        self.imgList = []
        self.df = pd.DataFrame()
        self.handle=''
        self.skuPrice = 0
        self.salePrice = 0
        self.tags = ''
        self.option1_name = ''
        self.option2_name = ''
        self.info=[]

    def creatWin(self):
        chrome_driver_path = '/Users/admin/Downloads/Wyatt/DailyDataProgram/chromedriver'
        # 禁用通知
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")

        prefs = {
            "profile.default_content_setting_values.geolocation": 2,  # 2表示拒绝无提示
        }
        chrome_options.add_experimental_option("prefs", prefs)
        # chrome_options.add_argument("--headless")
        # prefs = {"profile.managed_default_content_settings.images": 2}  # 这会禁止图片加载
        # chrome_options.add_experimental_option("prefs", prefs)
        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # driver.set_window_size(1920, 1080)
        # driver.get(url)
        # self.closeDialog(driver)
        return driver

    def get_element_by_xpath(self, driver, xpath, timeout=10):
        element= WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element

    def get_elements_by_xpath(self, driver, xpath):
        element= WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        return element

    def get_element_by_class_name(self, driver, class_name, timeout=10):
        element= WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
        return element

    def get_elements_by_class_name(self, driver, class_name):
        element= WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
        )
        return element

    def get_element_by_tag(self, driver, tag_name, timeout= 10):
        element= WebDriverWait(driver, timeout).until(
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

    def test(self, driver):
        action = ActionChains(driver)
        canvas = self.get_element_by_xpath(driver, './/canvas[@data-zr-dom-id="zr_0"]')
        data_list = []
        total_list = []
        # n = 0
        # empty = 0
        # while True:
        #     try:
        #         action.move_to_element_with_offset(canvas, n, 0).perform()
        #         target = self.get_element_by_class_name(driver, 'cg-toolti-box', 0.1)
        #         if target.text.split('\n')[0]:
        #             if target.text not in total_list:
        #                 data_list.append(target.text.split('\n'))
        #                 total_list.append(target.text)
        #         else:
        #             empty+=1
        #         if empty ==2:
        #             data_list.reverse()
        #             break
        #         n -= 1
        #     except:
        #         data_list.reverse()
        #         break

        n = 240
        empty = 0
        while True:
            try:
                action.move_to_element_with_offset(canvas, n, 0).perform()
                target = self.get_element_by_class_name(driver, 'cg-toolti-box', 0.1)
                if target.text.split('\n')[0]:
                    if target.text not in total_list:
                        data_list.append(target.text.split('\n'))
                        total_list.append(target.text)
                else:
                    empty += 1
                if empty == 2:
                    break
                n += 1
            except:
                break
        return data_list


def run():
    go = Spy()
    ls_df = []
    names = ['Binance', 'OKX', 'Bybit']
    folder_name = 'DailyData/' + str(datetime.date.today()) + '/Graph/'
    for epoch in range(3):
        driver = go.creatWin()
        driver.get('https://www.coinglass.com/zh/pro/i/MarginFeeChart')
        time.sleep(15)
        ret = go.test(driver)
        # print(ret)
        data = []
        for d in ret:
            data.append([datetime.datetime.strptime(d[0], '%Y-%m-%d %H:%M'), float(d[2].replace('%', '')) / 100])
        df = pd.DataFrame(data, columns=['datetime', 'value'])
        df = df[df['datetime'] >= datetime.datetime.now() - relativedelta(months=1)]
        df.to_csv(folder_name + 'Rowdata/' +'USDT杠杆借贷年利率-' + names[epoch] + '.csv')
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

