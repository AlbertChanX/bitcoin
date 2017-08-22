# coding:utf-8
import urllib.request as request
import asyncio, async_timeout
import aiohttp
import time, json
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import re
import logger


logger.initialize('DEBUG', 'INFO', 'log/coin.log')
log = logger.get_logger('alarm.py')
desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
     '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
desired_capabilities['phantomjs.page.settings.userAgent'] = ua
i_headers = {'Accept-Charset': 'GBK,UTF-8;q=0.7,*;q=0.3',
                 'User-Agent' :  'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US)'
                                  'AppleWebKit/534.16 (KHTML, like Gecko)'
                                  'Chrome/38.0.2125.111 Safari/537.36',
                'Host':'k.sosobtc.com' }

# driver = webdriver.Chrome('/Users/cyc/Downloads/chromedriver')

def get_coins(step=24*60*60):
    driver = webdriver.PhantomJS()
    main_url = 'https://www.sosobtc.com/currencies'
    url = 'https://k.sosobtc.com/data/period?symbol={}&step={}'
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
            urls.append(url.format(c['market']+c['lowerName']+'cny', step))
    driver.close()
    log.critical('got {} urls'.format(len(urls)))
    return urls

@asyncio.coroutine
async def getpage(url, res_list):
    # conn = aiohttp.ProxyConnector(proxy="http://127.0.0.1:8087")
    conn = aiohttp.TCPConnector(verify_ssl=False)
    async with aiohttp.ClientSession(connector=conn) as session:
        with async_timeout.timeout(60):
            async with session.get(url, headers=i_headers) as resp:
                log.info(resp.status)
                assert resp.status == 200
                log.info(url)
                res_list.append(await (resp.text()))


loop = asyncio.get_event_loop()

l = []

# urls = ['http://www.jubi.com/api/v1/allticker/', 'http://www.jubi.com/api/v1/orders/btc']

tasks = [getpage(url, l) for url in get_coins()]
print('start', time.time())
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
print('end', time.time())


# https://yunbi.com/swagger/#/
# * https://www.sosobtc.com/currencies   all coins

# from https://k.sosobtc.com/etc_yunbi.html
# api: https://k.sosobtc.com/data/period?symbol=yunbietccny&step=86400  ts :8:00
# params jubi/yunbi/huobi/okcoin/bter/cnbtc       step: 24*60*60
# like [1469664000,10.0,15.1,9.45,11.5,795771.9885] [open,high,low,close,vol]
# print(json.loads(l[0])['ans'])
