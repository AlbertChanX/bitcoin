# coding:utf-8

import requests
import time
import pandas as pd
import numpy as np


def get_kline(type, symbol='ltc_cny'):
    url = 'https://www.okcoin.cn/api/v1/kline.do?size=60&symbol=%s&type=%s' % (symbol, type)
    print(url)
    js = requests.get(url).json()
    return js


js = get_kline('15min')
for i in js:
    print(i)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i[0] / 1000)))
ma = 30
s1 = np.array(js)
df = pd.DataFrame(s1)
df.columns = ['ts', '1', '2', '3', 'close', 'vol']
# use pd's ma calculation
ma_re = pd.rolling_mean(df.close.values, ma).round(2)
print(ma_re[-3:])
