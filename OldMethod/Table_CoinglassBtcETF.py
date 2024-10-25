# -*- coding: utf-8 -*-
# @time : 2024/3/13 22:06
import os
import time

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

    def data_format(self, str):
        str = str.replace('$', '')
        if '亿' in str:
            return float(str.replace('亿', ''))
        elif '万' in str:
            return round(float(str.replace('万', ''))/10000, 2)
        else:
            return str

    def main(self, driver):
        # driver.get('https://www.coinglass.com/zh/bitcoin-etf')

        folder_name = 'DailyData/' + str(datetime.date.today()) +'/Table/'

        driver.get('https://www.coinglass.com/zh/bitcoin-etf')
        tables = self.get_elements_by_xpath(driver,self.classes_name('tr', 'ant-table-row ant-table-row-level-0'))
        ls1 = []
        for i in tables[:11]:
            str1 = i.text.split('\n')[1:-2]
            ls1.append(str1)
            # print(str1)
        button = self.get_elements_by_xpath(driver, self.classes_name('button','MuiTab-root MuiTab-horizontal MuiTab-variantPlain MuiTab-colorNeutral cg-style-1cunwlv'))[1]
        action = ActionChains(driver)
        action.move_to_element(button).click().perform()
        tables = self.get_elements_by_xpath(driver, self.classes_name('tr', 'ant-table-row ant-table-row-level-0'))
        ls2 = []
        for i in tables[:11]:
            str1 = i.text.replace(' -\n', '\n0\n').split('\n')[1:-3]
            ls2.append(str1)
            # print(str1)

        df1 = pd.DataFrame(ls1, columns=['交易代码', '币种', 'ETF名称', '价格(美元)', '价格变化', '价格变化百分比', '成交额(亿美元)', '成交量', '换手率', '流通股', '资产管理规模(亿美元)', '市值(亿美元)', '费用率'])
        df2 = pd.DataFrame(ls2, columns=['交易代码', '币种', 'ETF名称', '价格', '价格变化', '价格变化百分比', '溢价/折价', '持有比特币总量(个)', '每日持有变化（个）', '每日持有变化百分比', '持有变化（7天）', '持有变化百分比（7天）', '每股净资产'])
        df2 = df2.drop(['交易代码', '币种', 'ETF名称', '价格', '价格变化', '价格变化百分比'], axis=1)
        # print(df1)
        # print(df2)
        df_total = pd.concat([df1, df2], axis=1, sort=False)
        df_total = df_total.drop(['币种','价格变化','成交量','流通股', '持有变化（7天）', '持有变化百分比（7天）', '每股净资产'],axis = 1)
        df_total['价格(美元)'] = df_total['价格(美元)'].apply(lambda x: self.data_format(x))
        df_total['成交额(亿美元)'] = df_total['成交额(亿美元)'].apply(lambda x: self.data_format(x))
        # df_total['成交额(亿美元)'] = df_total['成交额(亿美元)'].apply(lambda x: '$'+str(x))
        df_total['资产管理规模(亿美元)'] = df_total['资产管理规模(亿美元)'].apply(lambda x: self.data_format(x))
        # df_total['资产管理规模(亿美元)'] = df_total['资产管理规模(亿美元)'].apply(lambda x: '$'+str(x))
        df_total['市值(亿美元)'] = df_total['市值(亿美元)'].apply(lambda x: self.data_format(x))
        # df_total['市值(亿美元)'] = df_total['市值(亿美元)'].apply(lambda x: '$'+str(x))
        df_total['持有比特币总量(个)'] = df_total['持有比特币总量(个)'].apply(lambda x: format(int(float(x.replace(',',''))),','))
        df_total['每日持有变化（个）'] = df_total['每日持有变化（个）'].apply(lambda x: format(int(float(x.replace(',',''))),','))


        # print(df_total)
        top3 = self.get_elements_by_class_name(driver, 'ant-space-item')
        for i in top3[:3]:
            print(i.text.split('\n'))
        driver.quit()
        df_total[df_total['交易代码']!='BITO'].to_csv(folder_name+'Coinglass_BTC-ETF-'+str(datetime.date.today())+'.csv')


if __name__ == '__main__':
    run = Spy()
    driver = run.creatWin()
    run.main(driver)

def get_coinglassbtcetf():
    run = Spy()
    driver = run.creatWin()
    run.main(driver)
