# coding:utf-8

from txzmq import ZmqEndpoint, ZmqFactory, ZmqPubConnection, ZmqSubConnection
from twisted.internet import reactor

zf = ZmqFactory()
e = ZmqEndpoint('connect', 'tcp://127.0.0.1:8881')  #

s = ZmqSubConnection(zf, e)
s.subscribe("btc")


def doPrint(*args):   # gotMessage(self, message, tag):
    print "message received: %r" % (args, )
s.gotMessage = doPrint

reactor.run()