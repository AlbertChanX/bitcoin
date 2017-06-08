# coding:utf-8
import requests
import time
from openpyxl import Workbook


# url = 'https://chain.api.btc.com/v3/address/1F1xcRt8H8Wa623KqmkEontwAAVqDSAWCV/tx?page='
def ts2time(ts):
    timeArray = time.localtime(ts)
    return time.strftime("%Y/%m/%d %H:%M:%S", timeArray)

tx_list = []
for i in range(1000):
    url = 'https://chain.api.btc.com/v3/address/1F1xcRt8H8Wa623KqmkEontwAAVqDSAWCV/tx?page=%s' % (i+1)
    flag = 0
    # session = requests.Session()
    # session.trust_env = False
    js = requests.get(url).json()
    time.sleep(2)

    for tx in js['data']['list']:
        tmp = []
        ts = ts2time(tx['block_time'])
        txid = tx['hash']
        balance = tx['balance_diff']/100000000.0
        print ts, txid, balance
        if ts <'2017/04/11':
            flag = 1
            break
        tmp.append(ts)
        tmp.append(txid)
        tmp.append(balance)
        tx_list.append(tmp)
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






