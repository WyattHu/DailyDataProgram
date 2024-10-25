import datetime
import pandas as pd
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import telebot
import time
from telebot import types
import threading

bot = telebot.TeleBot("7195657479:AAHFfuzk4-5nwf40UckqgJQqTqJ8XSPcUT4", parse_mode=None)

# bot.send_message(chat_id=-1002080189959, text='可')
# document = open('Test.xlsx', 'rb')
# bot.send_document(chat_id=-1002080189959, document=document)

dict_alreadySend = {}
threshold_up_top50 = 3
threshold_down_top50 = -3
threshold_up_other = 5
threshold_down_other = -5


def getMarketData():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'200',
      'convert':'USD',
      'sort_dir':'desc'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'c3189f52-161e-4781-8d67-287bdff425df'
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        df = pd.DataFrame(data['data'])
        # print(df.columns)
        # print(df.iloc[0]['quote'])
        df['price'] = df['quote'].apply(lambda x: x['USD']['price'])
        df['percent_change_1h'] = df['quote'].apply(lambda x: round(float(x['USD']['percent_change_1h']), 2))
        # print(df.columns)
        # print(df.iloc[0])
        df = df[['symbol', 'price', 'percent_change_1h', 'last_updated']]
        # df = df.sort_values(by=['percent_change_1h'], ascending=False)
        df_top50 = df.iloc[:50]
        df_Alert_top50 = pd.concat([df_top50[df_top50['percent_change_1h'] >= threshold_up_top50], df_top50[df_top50['percent_change_1h'] <= threshold_down_top50]])
        df_top200 = df.iloc[50:]
        df_Alert_top200 = pd.concat([df_top200[df_top200['percent_change_1h'] >= threshold_up_other],
                                    df_top200[df_top200['percent_change_1h'] <= threshold_down_other]])
        df_Alert = pd.concat([df_Alert_top50, df_Alert_top200])
        msg_send = '价格异动提醒：\n'
        bAlert = False
        for i in range(len(df_Alert)):
            if df_Alert.iloc[i]['symbol'] not in dict_alreadySend.keys():
                dict_alreadySend[df_Alert.iloc[i]['symbol']] = datetime.datetime.now()
                msg_send = msg_send + df_Alert.iloc[i]['symbol'] + ' 过去一小时涨跌幅：' + str(df_Alert.iloc[i]['percent_change_1h'])+'%, 当前价格：' + str(round(df_Alert.iloc[i]['price'], 3)) +'\n'
                bAlert = True
        if bAlert:
            print(msg_send)
            bot.send_message(chat_id=-1002080189959, text=msg_send)
            # bot.send_message(chat_id=-4236335720, text=msg_send)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


while 1:
    ls_keys = list(dict_alreadySend.keys())
    for k in ls_keys:
        if (datetime.datetime.now() - dict_alreadySend[k]).seconds >= 3600:
            dict_alreadySend.pop(k)
    getMarketData()
    time.sleep(300)
