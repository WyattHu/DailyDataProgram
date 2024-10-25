import okx.MarketData as MarketData
import pandas as pd

flag = "0"  # 实盘:0 , 模拟盘：1

marketDataAPI =  MarketData.MarketAPI(flag=flag)

# 获取所有产品行情信息
result = marketDataAPI.get_volume(
    #instType="SPOT"
)
print(result['data'])



# import okx.MarketData as MarketData
#
# flag = "0"  # 实盘:0 , 模拟盘：1
#
# marketDataAPI =  MarketData.MarketAPI(flag=flag)
#
# # 获取交易产品历史K线数据
# result = marketDataAPI.get_candlesticks(
#     instId="BTC-DAI",bar='1D'
# )
# print(result['data'])

