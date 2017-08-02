# coding:utf-8
import requests
import time
from lxml import etree
import urllib
import codecs
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def my_req(url):
    result = ''
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
    except requests.RequestException as e:
        print(e)
    else:
        # time.sleep(0.5)
        result = r.content
        # print(result)
    return result


if __name__ == "__main__":
    bh_dic = {}
    bs_dic = {}
    with open('chinese_simplified.txt', 'r') as f:
        lines = f.readlines()
        num = len(lines)
        for line in lines:
            num -= 1
            print('remain: %s' %num)
            line = line.strip()
            url = 'http://hanyu.baidu.com/s?wd=%s&ptype=zici' \
                  % urllib.quote(line)
            # urllib.request.urlretrieve(url, path + filename)
            result = my_req(url)
            html = etree.HTML(result)
            print(url)
            try:
                bh = html.xpath('//li[@id="stroke_count"]/span')[0].text
            except IndexError:
                bh = ''
            bs = html.xpath('//li[@id="radical"]/span')[0].text
            print(bs)
            print(bh)
            bh_dic[line] = bh

            if bs in bs_dic.keys():
                bs_dic[bs].append(line)
            else:
                bs_dic[bs] = [line]
            # print(bs_dic)
            # for k, v in bs_dic.items():
            #     print(type(v))
            #     for i in v:
            #         print('eg', type(v))

            # print(bs_dic.values()[0])
            # print(bh_dic.keys()[0])
            # if i == 6:
            #     break


with open('stroke_count.csv', 'wb') as f:
    f.write(codecs.BOM_UTF8)
    writer = csv.writer(f, dialect='excel')
    for k, v in bh_dic.items():
        print(k, v)
        writer.writerow([k, v])

# bs

with open('radical.csv', 'wb') as f:
    f.write(codecs.BOM_UTF8)
    writer = csv.writer(f, dialect='excel')
    for k, v in bs_dic.items():
        s = ' '
        for word in v:
            s += word
        writer.writerow([k, s])
