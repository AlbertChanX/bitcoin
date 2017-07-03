# coding:utf-8
# 变成generator的函数，在首次调用的时候执行，
# 遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行


def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'


def produce(c):
    print('c is a ', type(c))
    c.send(None)   # 首次调用
    print('first called send')
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

c = consumer()  # 并不会启动生成器, 只是将c变为一个生成器
produce(c)