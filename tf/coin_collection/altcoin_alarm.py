# coding:utf-8
import urllib.request as request
import asyncio, async_timeout
import aiohttp
import time, json


@asyncio.coroutine
async def getpage(url, res_list):
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'}
    # conn = aiohttp.ProxyConnector(proxy="http://127.0.0.1:8087")
    async with aiohttp.ClientSession() as session:
        with async_timeout.timeout(60):
            async with session.get(url, headers=headers) as resp:
                assert resp.status == 200
                res_list.append(await (resp.text()))

loop = asyncio.get_event_loop()

l = []

urls = ['http://www.jubi.com/api/v1/allticker/', 'http://www.jubi.com/api/v1/orders/btc']
tasks = [getpage(url, l) for url in urls]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

# https://yunbi.com/swagger/#/
# * https://www.sosobtc.com/currencies   all coins

# from https://k.sosobtc.com/etc_yunbi.html
# api: https://k.sosobtc.com/data/period?symbol=yunbietccny&step=86400
# params jubi/yunbi/huobi/okcoin/bter/cnbtc       step: 24*60*60
# like [1469664000,10.0,15.1,9.45,11.5,795771.9885] [open,high,low,close,vol]
# print(json.loads(l[0])['ans'])

print(len(l))
