# coding:utf-8
import sqlite3
import requests
import gevent
import time
import logger
import calendar, datetime
from timetools import months

log = logger.get_logger('data.py')


def my_req(url):
    result = ''
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()      # 如果响应状态码不是 200，就主动抛出异常
    except requests.RequestException as e:
        result = None
        log.error(e)
    else:
        time.sleep(0.8)
        result = r.json()
    finally:
        pass
    return result


def get_blockheight(t):
    # print (int(t[6:8]))
    dt = datetime.date(int(t[0:4]), int(t[4:6]), int(t[6:8]))
    # get last month/year
    t_last = months(dt, -1)   # the last month like '20161201'
    # print(t_last)
    t_last_year = t_last[0:4]
    t_last_month = t_last[4:6]   # str
    day_b = calendar.monthrange(int(t_last_year), int(t_last_month))    # (1,31)
    date = t_last_year + '-' + t_last_month + '-' + str(day_b[1])
    url = 'https://chain.api.btc.com/v3/block/date/%s' % date   # 2017-7-18
    print(url)
    data = my_req(url)['data']
    for i in data:
        h = i['height']  # 前一个月的最后一个块的高度
        m = time.strftime('%m', time.localtime(i['timestamp']))
        # print(m,t_last_month)
        if m == t_last_month:
            break
    return h


def get_block_num_monthly(dttime):   # 2017-6-30
    t = time.localtime(time.time())
    if time.strftime('%Y-%m-%d %H:%M:%S', t) > dttime:   # 7 > 6
        dttime = dttime.replace('-', '')
        # month = int(dttime[4:6])
        bom = get_blockheight(dttime)   # 2017-06-30
        print('bom ', bom)
        dt = datetime.date(int(dttime[0:4]), int(dttime[4:6]), int(dttime[6:8]))

        eom = get_blockheight(months(dt, +1))  # 2017-07-30
        print('eom, ', eom)
        num_monthly = eom - bom
        return num_monthly
    else:  # 返回当月
        month = t.tm_mon
        bom = get_blockheight(time.strftime('%Y%m%d', t))
        print('bom ', bom)
        blockh_recent = my_req('https://chain.api.btc.com/v3/block/'
                               'latest')['data']['height']
        num_monthly = blockh_recent - bom

        print('blockh_recent, ', blockh_recent)
        return num_monthly

if __name__ == "__main__":


    # gevent.joinall([
    #         gevent.spawn(f, 'https://www.python.org/'),
    #         gevent.spawn(f, 'https://www.yahoo.com/'),
    #         gevent.spawn(f, 'https://github.com/'),
    # ])


    def get_page(url):
        data = my_req(url)
        time.sleep(0.5)
        print('%d bytes received from %s.' % (len(data), url))


    t = time.time()
    tasks = []
    for i in range(40):
        url = 'https://chain.api.btc.com/v3/address' \
              '/1F1xcRt8H8Wa623KqmkEontwAAVqDSAWCV/tx?page=%s' % (i + 1)
        # get_page(url)
        tasks.append(gevent.spawn(get_page, url))

    # gevent.joinall(tasks)
    # print(': %s ' % (time.time()-t))

    get_block_num_monthly('2016-10-10')     # 2017-7

    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    te = time.localtime(time.time())
    if te.tm_mon < 8:
        print(t)

# conn = sqlite3.connect('tx.db')
# conn.execute('''CREATE TABLE income
#        (ID INT PRIMARY KEY     NOT NULL,
#        NAME           TEXT    NOT NULL,
#        AGE            INT     NOT NULL,
#        ADDRESS        CHAR(50),
#        SALARY         REAL);''')
# conn.close()

