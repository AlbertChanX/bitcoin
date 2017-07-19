# coding:utf-8
from request_tools import my_req
import time
from openpyxl import Workbook
import pandas as pd
from timetools import get_time
from timetools import ts2time
from DBHelper import DBHelper
import logger
import math

log = logger.get_logger('1hash-txinfo.py')


class Data(object):
    def __init__(self):
        self.url = 'https://chain.api.btc.com/v3/address' \
                  '/1F1xcRt8H8Wa623KqmkEontwAAVqDSAWCV/tx?page=%s'

    def get_page(self):
        url = self.url % (str(1))
        js = my_req(url)
        count = js['data']['total_count']
        pagesize = js['data']['pagesize']
        page = int(math.ceil(1.0*count/pagesize))
        log.info('getting pages = %s, total_count: %s' % (page, count))
        return page

    def get_latest(self, type='tx'):
        if type == 'tx':
            sql = 'select * from INCOME order by time desc limit 1'
            t = DBHelper().select(sql)
            return t
        else:
            return None

    def get_tx(self):
        tx_list = []
        pages = self.get_page()
        latest = self.get_latest(type='tx')[0][1]
        if len(latest) == 0:
            latest = None
        for i in range(pages):
            url = self.url % (i+1)
            log.info('get blockinfo, page: %s' % (i+1))
            flag = 0
            # session = requests.Session()
            # session.trust_env = False
            js = my_req(url)
            log.info('requesting: %s' % url)
            time.sleep(1.5)
            for tx in js['data']['list']:
                tmp = []
                ts = ts2time(tx['block_time'])
                if ts > latest:
                    # print('latest ', latest)
                    txid = tx['hash']
                    balance_diff = tx['balance_diff']/100000000.0
                    # print ts, txid, balance
                    is_cb = tx['is_coinbase']
                    outputs = tx['outputs_count']
                    if is_cb:
                        is_cb = 1
                    else:
                        is_cb = 0
                    fee = balance_diff - 12.5
                    tmp.append(ts)
                    tmp.append(txid)
                    tmp.append(balance_diff)
                    tmp.append(fee)
                    # print(fee)
                    tmp.append(is_cb)
                    tmp.append(outputs)
                    tx_list.append(tuple(tmp))
                else:
                    flag = 1
                    break
                # tmp.append(ts)
                # tmp.append(txid)
                # tmp.append(balance)
                # print(tmp)
            if flag == 1:
                break
        return tx_list

    def update_tx(self, value_list):
        sql = "insert into income " \
              "(time, txid, balance_diff, fee, is_coinbase, outputs_count) " \
              "VALUES (?,?,?,?,?,?);"
        DBHelper().batch_insert(sql, value_list)
        log.info('updated %s tx' % len(value_list))

    def get_block_info(self):
        pass

    def group_result(self, year=None):
        special = ['f821d41e7840f7c9122793a80399c2e79b543de79653eedcd3f89a44fad4038d',
                   'acc8a78ec434cdfa259edbea5befb186ab3e569e8e7c0d466714d3b477d4148e',
                   '82923bff6443459c4039f6e66b651703c7b0528a7e6bab933d6c47d8673a3f41',
                   '2d74f0c4deb7f250fe0e526fe1c63b0534b7d659ee96d9db4235cc3b363f11bd',
                   '5d97f3052edaa9676add54e5c7b4aa3549370083beb5035dfabf64d209e1f258']
        con = DBHelper().get_con()
        sql = 'select time, txid, balance_diff, ' \
              'fee, is_coinbase, outputs_count from income'
        df = pd.read_sql(sql, con)
        df = df.set_index(pd.DatetimeIndex(df['time']))
        con.close()

        # 出块数量/ 块总收入/ 块手续费收入

        df_s = df[(df['is_coinbase'] == 1)]
        [['time', 'balance_diff', 'fee', 'is_coinbase']]
        if year is not None:
            df_s = df_s[year]
        # df_s = df_coinbase.sort_index(ascending=False)  # sort --> df_s
        df_month = df_s.resample('M').sum()

        # 支付总数
        df_pay = df[(df['is_coinbase'] == 0) & (df['balance_diff'] < 0) &
                    (-df['txid'].isin(special))][['time', 'balance_diff']]
        if year is not None:
            df_pay = df_pay[year]
        df_pay = df_pay.resample('M').sum()
        df_month['payout'] = df_pay['balance_diff']
        # print(df_month)

        # block_monthly
        from request_tools import get_block_num_monthly
        block_monthly = []
        for month in df_month.index:
            num = get_block_num_monthly(str(month)[:10])
            block_monthly.append(num)
        df_month['block_monthly'] = block_monthly
        log.info('add block_monthly success: num is %s' % len(block_monthly))

        # 流水明细
        df_detail = df.sort_index()
        print(df_detail)
        df_detail = df_detail.drop(['is_coinbase', 'outputs_count'], axis=1)
        df_detail['balance'] = df_detail['balance_diff'].cumsum()

        # save to excel
        writer = pd.ExcelWriter('1hash_tx_dada_%s.xlsx' % get_time())
        df_month.to_excel(writer, sheet_name=u'汇总结果')
        df_detail.to_excel(writer, sheet_name=u'流水明细表')
        writer.save()

        return df_month


def save_tx(tx_list):
    wb = Workbook()
    # 获取当前活跃的worksheet,默认就是第一个worksheet
    ws = wb.active
    title = ['time', 'is_coinbase', 'block_revenue', 'fee']
    ws.append(title)
    for tx in tx_list:
        ws.append(tx)
        print(tx)
    wb.save(filename="1hash_tx2.xlsx")


if __name__ == "__main__":
    # Data().get_latest()
    # Data().group_result()
    v_list = Data().get_tx()
    # print(len(v_list))
    Data().update_tx(v_list)
    # df = pd.read_excel("/Users/cyc/Documents/mypy/1hashtxdata/1hash_tx.xlsx", sheetname=['Sheet'])['Sheet']
    # df.columns = ['time', 'balance', 'fee']
    # df = df.set_index('time2')
    # print(df.groupby('time2'))
    # print('ok')
    # df_groupby = df.resample('1M').sum()   # ??? month

    # df_groupby = df.groupby(['time2']).sum()
    # df_groupby.reset_index()
    # get_bar(df_groupby)
    # select
    # print(df[df['fee'] > 2])
    # print(df.columns)
    # print(df[['fee', 'quant']])   # [ ]

    #
    # 计算各列数据总和并作为新列添加到末尾
    # df['Col_sum'] = df.apply(lambda x: x.sum(), axis=1)
    # 计算各行数据总和并作为新行添加到末尾
    #
    # df.loc['Row_sum'] = df.apply(lambda x: x.sum())













