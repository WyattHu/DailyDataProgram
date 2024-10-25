import pandas as pd
import datetime
import time
import os
import Table_CryptoTop5
import Table_CryptoTop10
import Table_YahooWorldIndices
import Table_CoinglassBtcETF_API
import Table_CoinglassBtcETF_flow_history_API
import Table_CEXVolume_Request
import Summary
import Graph_YahooWorldIndices
import Graph_USDT_Margin_Borrow_Interest_Rate_API
import Graph_Total_Bitcoin_Spot_ETF_Net_Inflow_API
import Graph_OI_Weighted_Funding_Rate_API
import Table_Coinglass_FearGreed
import Graph_LUACTRUU

bTrigger1 = True
bTrigger2 = True
bTrigger3 = True


while(1):
    time.sleep(1)
    folder_name = 'DailyData/' + str(datetime.date.today())  # 判断当天文件夹是否存在
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        os.mkdir(folder_name+'/Graph')
        os.mkdir(folder_name+'/Table')
        os.mkdir(folder_name+'/Graph/Rowdata')

    time_now = datetime.datetime.now()  # 获取当前时间
    today = datetime.datetime.today()   # 今天日期

    if time_now > datetime.datetime(today.year, today.month, today.day, 21, 25, 00) and bTrigger1:
        Table_CoinglassBtcETF_API.get_coinglassbtcetf()
        Graph_Total_Bitcoin_Spot_ETF_Net_Inflow_API.run()
        Graph_OI_Weighted_Funding_Rate_API.run()
        Graph_USDT_Margin_Borrow_Interest_Rate_API.run()
        Table_CoinglassBtcETF_flow_history_API.get_coinglassbtcetf_flowhistory()
        Table_Coinglass_FearGreed.run()
        bTrigger1 = False

    if time_now > datetime.datetime(today.year, today.month, today.day, 21, 31, 30) and bTrigger2:
        Table_CryptoTop5.get_cryptotop5()
        Table_CryptoTop10.get_cryptotop10()
        Table_CEXVolume_Request.get_cexvolume()
        bTrigger2 = False

    b_isWeekday = datetime.date.today().weekday() != 5 and datetime.date.today().weekday() != 6

    if (((time_now > datetime.datetime(today.year, today.month, today.day, 21, 48, 00) and b_isWeekday)
            or (time_now > datetime.datetime(today.year, today.month, today.day, 21, 33, 00) and not b_isWeekday))
            and bTrigger3):
        Table_YahooWorldIndices.get_yahooworldindices()
        Graph_YahooWorldIndices.get_yahooworldindices()
        Graph_LUACTRUU.run()
        Summary.summary()
        bTrigger3 = False

    if not bTrigger1 and not bTrigger2 and not bTrigger3:
        print('Finished!')
        date_today = datetime.date.today()
        break

    # if datetime.date.today() != date_today:
    #     bTrigger1 = True
    #     bTrigger2 = True
    #     bTrigger3 = True

