# coding:utf-8

from txzmq import ZmqEndpoint, ZmqSubConnection
from twisted.internet import reactor
from ZmqFactory import ZmqFactory
import time

zf = ZmqFactory()
global sub
sub = ZmqSubConnection(zf, ZmqEndpoint('connect', 'tcp://127.0.0.1:8881'))
sub.subscribe("btc")


class Server(object):
      def __init__(self, sub):
          self.sub = sub

num = 0

def doPrint(*args):  # gotMessage(self, message, tag):
    global num
    num += 1
    print("the num of data: %d" % (num))
    print("message received: %r" % (args,))


def generate_s():
    for i in range(10000):
        print(i)
        s_list = []
        global sub
        sub = ZmqSubConnection(zf, ZmqEndpoint('connect', 'tcp://127.0.0.1:8881'))
        sub.subscribe("btc" % (i+1))
        sub.gotMessage = doPrint
        names = locals()
        names['server-%s' % i] = Server(sub)


def test():
    start = time.time()
    print('begin: ', start)
    for s in generate_s():
        s.receive()
    end = time.time()
    print('end: ', end)
    print('total time: %s' % (end-start))

if __name__ == "__main__":
    generate_s()
    reactor.run()
