import datetime
import time

import pandas
import pandas as pd
from matplotlib import pyplot as plt


# df = pd.read_excel('BTC_ETH_Ratio.xlsx')
# print(df['日期'])
# print(df.loc[df['日期']==datetime.date.today()])
# plt.cla()
# plt.figure(figsize=(2, 0.35))
# plt.plot(df['比特币占比'], color='r')
# plt.gca().spines['right'].set_visible(False)
# plt.gca().spines['top'].set_visible(False)
# plt.gca().spines['left'].set_visible(False)
# plt.gca().spines['bottom'].set_visible(False)
# plt.yticks([])
# plt.xticks([])
# plt.savefig('BTC' + '.jpg')
#
# plt.cla()
# plt.figure(figsize=(2, 0.35))
# plt.plot(df['以太坊占比'], color='r')
# plt.gca().spines['right'].set_visible(False)
# plt.gca().spines['top'].set_visible(False)
# plt.gca().spines['left'].set_visible(False)
# plt.gca().spines['bottom'].set_visible(False)
# plt.yticks([])
# plt.xticks([])
# plt.savefig('ETH' + '.jpg')


df1 = pd.read_excel('LUACTRUU.xlsx')
# print(df1)
plt.cla()
plt.figure(figsize=(2, 0.35))
plt.plot(df1['PX_LAST'], color='r')
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.yticks([])
plt.xticks([])
plt.savefig('LUACTRUU' + '.jpg')


# df = pd.read_csv('WGMI.csv')
# # print(df['日期'])
# # print(df.loc[df['日期']==datetime.date.today()])
# plt.cla()
# plt.figure(figsize=(2, 0.35))
# plt.plot(df['Close'], color='r')
# plt.gca().spines['right'].set_visible(False)
# plt.gca().spines['top'].set_visible(False)
# plt.gca().spines['left'].set_visible(False)
# plt.gca().spines['bottom'].set_visible(False)
# plt.yticks([])
# plt.xticks([])
# plt.savefig('WGMI' + '.jpg')
