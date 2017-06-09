# coding:utf-8
import requests
import time
from openpyxl import Workbook
import pandas as pd


# url = 'https://chain.api.btc.com/v3/address/1F1xcRt8H8Wa623KqmkEontwAAVqDSAWCV/tx?page='
def ts2time(ts):
    timeArray = time.localtime(ts)
    return time.strftime("%Y/%m/%d %H:%M:%S", timeArray)

tx_list = []
for i in range(1000):
    url = 'https://chain.api.btc.com/v3/address/1F1xcRt8H8Wa623KqmkEontwAAVqDSAWCV/tx?page=%s' % (i+1)
    print url
    flag = 0
    # session = requests.Session()
    # session.trust_env = False
    js = requests.get(url).json()
    time.sleep(2.5)

    for tx in js['data']['list']:
        tmp = []
        ts = ts2time(tx['block_time'])
        print ts
        # txid = tx['hash']
        balance = tx['balance_diff']/100000000.0
        # print ts, txid, balance
        is_cb = tx['is_coinbase']
        print is_cb
        if ts >= '2017/03/01' and ts < '2017/06/01' and is_cb:
            print(ts, is_cb)
            tmp.append(ts)
            tmp.append(is_cb)
            tmp.append(balance)
            tmp.append(balance-12.5)
            tx_list.append(tmp)
        elif ts < '2017/03/01':
            flag = 1
            break
        # tmp.append(ts)
        # tmp.append(txid)
        # tmp.append(balance)
        # print(tmp)
    if flag == 1:
       break

wb = Workbook()
# 获取当前活跃的worksheet,默认就是第一个worksheet
ws = wb.active
for tx in tx_list:
    ws.append(tx)
    print(tx)
wb.save(filename="1hash_tx.xlsx")

df = pd.read_excel("1hash_tx.xlsx")
df.columns = ['time', 'balance', 'fee']












