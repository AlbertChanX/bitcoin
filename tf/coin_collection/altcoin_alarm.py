# coding:utf-8
import urllib.request as request
import asyncio, async_timeout
import aiohttp
import pandas as pd
import time, json
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import re
import logger, requests, gevent
from Hdf5helper import Hdf5helper

logger.initialize('DEBUG', 'INFO', 'log/coin.log')
log = logger.get_logger('alarm.py')
desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
     '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

i_headers = {'Accept-Charset': 'GBK,UTF-8;q=0.7,*;q=0.3',
             'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US)'
                                'AppleWebKit/534.16 (KHTML, like Gecko)'
                                'Chrome/38.0.2125.111 Safari/537.36',
             'Host': 'k.sosobtc.com',
             'Content_Length': 'null'}

desired_capabilities['phantomjs.page.settings.userAgent'] = ua
# driver = webdriver.Chrome('/Users/cyc/Downloads/chromedriver')


def get_coins():
    driver = webdriver.PhantomJS()
    main_url = 'https://www.sosobtc.com/currencies'

    driver.get(main_url)
    # driver.save_screenshot('screen.png')
    # js = 'return window.__data;'
    # coins = driver.execute_script(js)
    text = driver.page_source
    dic = re.findall(r'window.__data=(.*?);</script>', text)
    markets = ['okcoin','yunbi','viabtc','btc38','btc9','bter','jubi','btcchina']
    urls = []
    for c in json.loads(dic[0])['currencyState']['currency']:
        if c['market'] in markets:
            urls.append(c['market']+c['lowerName']+'cny')
    driver.close()
    log.critical('got {} urls'.format(len(urls)))
    return urls


def getdata(coin, step=24*60*60):
    url = 'https://k.sosobtc.com/data/period?symbol={}&step={}'.format(coin, step)
    result = requests.get(url, headers=i_headers, timeout=60)
    result.raise_for_status()
    print(result.status_code)
    result = result.json()
    df = pd.DataFrame(result)
    df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
    df['name'] = coin
    Hdf5helper().put_df('coins/{}'.format(coin), df)
    log.critical('insert into coins/{} {} rows'.format(coin, df.shape))
    return result

t = time.time()
tasks = []
coins = get_coins()
log.critical('get {} coins now'.format(len(coins)))
for url in coins:
    tasks.append(gevent.spawn(getdata, url))

gevent.joinall(tasks)
print(': %s ' % (time.time()-t))

# async def fetch(url, session):
#     async with session.get(url, headers=i_headers) as response:
#         print(response.status)
#         if response.status == 200:
#             html = await response.text()
#             return {'error': '', 'html': html}
#         else:
#             return {'error': response.status, 'html': ''}
#         # return await response.read()
#
#
# async def bound_fetch(sem, url, session):
#     # Getter function with semaphore.
#     async with sem:
#         await fetch(url, session)
#
# @asyncio.coroutine
# async def getpage(urls):
#     # conn = aiohttp.ProxyConnector(proxy="http://127.0.0.1:8087")
#     tasks = []
#     # create instance of Semaphore
#     sem = asyncio.Semaphore(1000)
#     conn = aiohttp.TCPConnector(verify_ssl=False)
#     async with aiohttp.ClientSession(connector=conn) as session:
#         with async_timeout.timeout(60):
#             # async with session.get(url, headers=i_headers) as resp:
#                 # assert resp.status == 200
#                 for url in urls:
#                     print(url)
#                     # pass Semaphore and session to every GET request
#                     task = asyncio.ensure_future(bound_fetch(sem, url, session))
#                     tasks.append(task)
#                 responses = asyncio.gather(*tasks)
#                 return await responses
#
# loop = asyncio.get_event_loop()
#
# l = []
#
# urls = ['http://www.jubi.com/api/v1/allticker/', 'http://www.jubi.com/api/v1/orders/btc']
#
# tasks = [getpage(url, l) for url in get_coins()]
# t = time.time()
# print('start', t)
# future = asyncio.ensure_future(getpage(get_coins()))
# loop.run_until_complete(future)
# loop.close()
# print('interval', time.time()-t)
# print(len(l))
# print(l)




# https://yunbi.com/swagger/#/
# * https://www.sosobtc.com/currencies   all coins

# from https://k.sosobtc.com/etc_yunbi.html
# api: https://k.sosobtc.com/data/period?symbol=yunbietccny&step=86400  ts :8:00
# params jubi/yunbi/huobi/okcoin/bter/cnbtc       step: 24*60*60
# like [1469664000,10.0,15.1,9.45,11.5,795771.9885] [open,high,low,close,vol]
# print(json.loads(l[0])['ans'])
