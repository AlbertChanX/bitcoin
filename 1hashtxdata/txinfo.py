# coding:utf-8
from request_tools import my_req
# from openpyxl import Workbook
import pandas as pd
from timetools import get_time
from timetools import ts2time
from dbhelper import DBHelper
import logger
import math

log = logger.get_logger('1hash-txinfo.py')


def subsidy(height):
    return (50 * 100000000 >> (height + 1) // 210000)/100000000.0


def tuple2list(list_t):
    tmp = []
    for i in list_t:
        tmp.append(''.join(i))
    return tmp


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

    def get_latest(self, tx_type='tx'):
        if tx_type == 'tx':
            sql = 'select * from INCOME order by time desc limit 1'
        # get the time for insert the time that not in db
        elif tx_type == 'block':
            sql = 'select time from BLOCK order by time desc'
        # get the time that is_update=0 for update
        elif tx_type == 'block_updating':
            sql = 'select time from BLOCK where is_update=0 order by time desc'
        t = DBHelper().select(sql)
        return t

    def get_tx(self):
        tx_list = []
        pages = self.get_page()
        try:
            latest = self.get_latest(tx_type='tx')[0][1]
            log.info('get latest txinfo: %s' % latest)
        except IndexError:
            latest = 0
        for i in range(pages):
            url = self.url % (i+1)
            log.info('get blockinfo, page: %s' % (i+1))
            flag = 0
            js = my_req(url)
            log.info('requesting: %s' % url)

            for tx in js['data']['list']:
                if tx['block_time'] == 0:
                    continue
                tmp = []
                print('latest ', latest)
                ts = ts2time(tx['block_time'])
                print('ts ', ts)
                if ts > latest:
                    txid = tx['hash']
                    balance_diff = tx['balance_diff']/100000000.0
                    # print ts, txid, balance
                    is_cb = tx['is_coinbase']
                    outputs = tx['outputs_count']
                    if is_cb:
                        is_cb = 1
                        sub = subsidy(tx['block_height'])
                        fee = balance_diff - sub
                    else:
                        is_cb = 0
                        fee = 0
                    tmp.append(ts)
                    tmp.append(txid)
                    tmp.append(balance_diff)
                    tmp.append(fee)
                    tmp.append(is_cb)
                    tmp.append(outputs)
                    tx_list.append(tuple(tmp))
                else:
                    flag = 1
                    break
            if flag == 1:
                break
        return tx_list

    def update_tx(self, value_list):
        sql = "insert into income " \
              "(time, txid, balance_diff, fee, is_coinbase, outputs_count) " \
              "VALUES (?,?,?,?,?,?);"
        DBHelper().batch_insert(sql, value_list)
        print(value_list)
        log.info('updated %s txinfo' % len(value_list))

    def update_block_monthly(self, block_tuple, is_insert=1):
        if is_insert == 1:
            sql = '''
                  insert into block (time, quantity, is_update) VALUES (?,?,?)      
                  '''
        else:
            sql = '''
                update block set quantity =?, is_update=? where time=?     
                  '''
        DBHelper().updateByParam(sql, block_tuple)
        log.info('update block-quantity success: {}{}'.format(sql, block_tuple))

    def group_result(self, year=None):
        special = [
                   '2d74f0c4deb7f250fe0e526fe1c63b0534b7d659ee96d9db4235cc3b363f11bd',
                   '5d97f3052edaa9676add54e5c7b4aa3549370083beb5035dfabf64d209e1f258',
                   'f359467888edb00309c3713566593c1e33ecfc2e26f7f7be1f4052d756e3aed0',
                   'f359467888edb00309c3713566593c1e33ecfc2e26f7f7be1f4052d756e3aed0']
        con = DBHelper().get_con()
        sql = 'select time, txid, balance_diff, ' \
              'fee, is_coinbase from income'
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
        df_pay = df[(df['balance_diff'] < 0) & (-df['txid'].isin(special))]
        df_pay = df_pay[['balance_diff']]
        if year is not None:
            df_pay = df_pay[year]
        print(df_month)
        df_pay_month = df_pay.resample('M').sum()  # assign to other var

        df_pay_month.columns = ['payout']
        print(df_pay_month)
        df_month = df_pay_month.join(df_month)
        # adjust position of column 'payout'
        payout = df_month['payout']
        df_month.drop(labels=['payout'], axis=1, inplace=True)
        df_month['payout'] = payout
        df_month = df_month.fillna(0)
        print(df_month)

        # block_monthly   获取每月出块数量
        from request_tools import get_block_num_monthly
        block_time = self.get_latest(tx_type='block')  # like [tuple]
        block_time = tuple2list(block_time)
        #  get block that is_update = 0
        block_updating = self.get_latest(tx_type='block_updating')
        block_updating = tuple2list(block_updating)
        for month in df_month.index:
            if str(month) not in block_time:
                num, is_update = get_block_num_monthly(str(month)[:10])
                self.update_block_monthly((str(month), num, is_update), is_insert=1)  # insert
            elif str(month) in block_updating:
                num, is_update = get_block_num_monthly(str(month)[:10])
                self.update_block_monthly((num, is_update, str(month)), is_insert=0)  # update
        # get block_monthly from db
        con = DBHelper().get_con()
        sql = 'select time, quantity from block'
        df_block = pd.read_sql(sql, con)
        # df_block = df_block.set_index(pd.DatetimeIndex(df['time']))
        con.close()
        df_month['block_monthly'] = df_block['quantity'].tolist()
        log.info('add block_monthly success: num is %s' % df_block)

        # balance details
        df_detail = df.sort_index()
        df_detail = df_detail.drop(['is_coinbase'], axis=1)
        df_detail['balance'] = df_detail['balance_diff'].cumsum()

        # add Net Profit
        df_month['Net_profit'] = df_month['balance_diff'] + df_month['payout']

        # save to excel
        writer = pd.ExcelWriter('data/1hash_tx_dada_%s.xlsx' % get_time())
        df_month_group = df_month.copy()
        tmp = df_month_group.reset_index(drop=True).sum(axis=0)
        df_month_group.loc['Column_sum'] = tmp
        df_month_group.columns = [u'块总收入', u'块手续费收入', u'出块数量',u'支付总数',u'全网出块数量',u'净利润']
        df_month_group.to_excel(writer, sheet_name=u'汇总结果')
        df_detail.to_excel(writer, sheet_name=u'流水明细表')
        writer.save()

        return df_month, df_detail


# def save_tx(tx_list):
#     wb = Workbook()
#     # 获取当前活跃的worksheet,默认就是第一个worksheet
#     ws = wb.active
#     title = ['time', 'is_coinbase', 'block_revenue', 'fee']
#     ws.append(title)
#     for tx in tx_list:
#         ws.append(tx)
#         print(tx)
#     wb.save(filename="1hash_tx2.xlsx")


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













